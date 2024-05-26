import praw
import os
import sys
from datetime import datetime, timedelta
import time
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.styles import GREEN, RED, CYAN, RESET
from src.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

def decodeUnicodeEscapes(inputString):
    import re

    def replaceEscape(match):
        if match.group(1):
            return chr(int(match.group(1), 16))  #\xXX
        elif match.group(2):
            return chr(int(match.group(2), 16))  #\uXXXX
        elif match.group(3):
            return chr(int(match.group(3), 16))  #\UXXXXXXXX
        elif match.group(4):
            return chr(int(match.group(4), 8))   #\ooo (octal)
        elif match.group(5) == 'n':
            return '\n'  #Newline
        elif match.group(5) == 't':
            return '\t'  #Tab
        elif match.group(5) == 'r':
            return '\r'  #Carriage return
        elif match.group(5) == '\\':
            return '\\'  #Backslash
        return match.group(0)  #Should not reach here

    #Regular expression to find escape sequences
    unicodeEscapePattern = re.compile(
        r'\\x([0-9a-fA-F]{2})|'  #\xXX
        r'\\u([0-9a-fA-F]{4})|'  #\uXXXX
        r'\\U([0-9a-fA-F]{8})|'  #\UXXXXXXXX
        r'\\([0-7]{1,3})|'       #\ooo
        r'\\(.)'                 #Special characters: \n, \t, \r, \\
    )

    #Replace all escape sequences in the input string
    decodedString = unicodeEscapePattern.sub(replaceEscape, inputString)
    return decodedString

def createRedditClient():
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        # Verify client creation
        print(f"{GREEN}Reddit client created successfully{RESET}")
        return reddit
    except Exception as e:
        print(f"Failed to create Reddit client: {RED}{e}{RESET}")
        return None

def fetchComments(reddit, subredditName, comLimit):
    comments = []
    try:
        for submission in tqdm(reddit.subreddit(subredditName).new(limit=None), desc="Fetching Comments"):
            submission.comments.replace_more(limit=0)
            submissionComments = submission.comments.list()
            comments.extend(submissionComments)
            if len(comments) >= comLimit:
                break
            # Sleep to avoid hitting rate limits
            time.sleep(1)
    except Exception as e:
        print(f"{RED}Error fetching comments: {e}{RESET}")
    return comments[:comLimit]

def filterComments(comments, searchTermsSet, timeLimit, minUpvotes, minKarma, botIdentifier, comLimit):
    filteredComments = []
    try:
        for comment in tqdm(comments, desc="Filtering Comments"):
            commentBodyLower = comment.body.lower()
            commentTime = datetime.utcfromtimestamp(comment.created_utc)
            # Check if the comment author has the comment_karma attribute
            authorKarma = getattr(comment.author, 'comment_karma', None)
            if (botIdentifier not in commentBodyLower and
                commentTime >= timeLimit and
                comment.score >= minUpvotes and
                comment.author and authorKarma is not None and
                authorKarma >= minKarma):
                if any(term in commentBodyLower for term in searchTermsSet):
                    commentData = {
                        "body": decodeUnicodeEscapes(comment.body),
                        "created_utc": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        "score": comment.score,
                        "karma": authorKarma
                    }
                    filteredComments.append(commentData)
                    if len(filteredComments) >= comLimit:
                        return filteredComments
    except Exception as e:
        print(f"{RED}Error filtering comments: {e}{RESET}")
    return filteredComments

def fetchSubredditComments(reddit, subredditName, ticker, variations, comLimit, recency, minUpvotes, minKarma):
    try:
        searchTerms = [ticker] + variations
        searchTermsSet = {term.lower() for term in searchTerms}
        botIdentifier = "*I am a bot, and this action"
        timeLimit = datetime.utcnow() - timedelta(days=recency)

        print(f"{GREEN}Fetching comments from subreddit '{subredditName}'...{RESET}")
        rawComments = fetchComments(reddit, subredditName, comLimit * len(searchTerms))

        print(f"{GREEN}Filtering comments...{RESET}")
        filteredComments = filterComments(rawComments, searchTermsSet, timeLimit, minUpvotes, minKarma, botIdentifier, comLimit)

        return filteredComments[:comLimit]
    except Exception as e:
        print(f"{RED}Failed to fetch comments: {e}{RESET}")
        return []

if __name__ == "__main__":
    reddit = createRedditClient()
    if reddit:
        subredditName = input("Enter subreddit name: ").strip()
        ticker = input("Enter a stock ticker (e.g., $AAPL): ")
        if not ticker.startswith("$"):
            print(f"{RED}Invalid ticker format. Precede all tickers with '$'{RESET}")
            sys.exit()

        variations = []
        addVariations = input("Do you want to add variations? (yes/no): ").lower()
        if addVariations == 'yes':
            print("Enter each variation on a new line. '/n' to submit")
            while True:
                variation = input()
                if variation.lower() == '/n':
                    break
                variations.append(variation)

        try:
            comLimit = int(input("Enter number of comments to analyze: ").strip())
            recency = int(input("Enter the number of days to consider for recency: ").strip())
            minUpvotes = int(input("Enter the minimum number of upvotes: ").strip())
            minKarma = int(input("Enter the minimum account karma: ").strip())
            comments = fetchSubredditComments(reddit, subredditName, ticker, variations, comLimit, recency, minUpvotes, minKarma)
            if comments:
                for i, comment in enumerate(comments, start=1):
                    print(f"{CYAN}COMMENT {i}{RESET}: {comment['body']}")
                    print(f"    {CYAN}Created: {comment['created_utc']}, Upvotes: {comment['score']}, Karma: {comment['karma']}{RESET}")
            else:
                print(f"{RED}No comments found matching the criteria{RESET}")
        except ValueError:
            print(f"{RED}Invalid input for number of comments{RESET}")
