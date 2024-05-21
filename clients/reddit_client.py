import praw
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.styles import GREEN, RED, RESET
from src.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

def createRedditClient():
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        # verify client creation
        print(f"{GREEN}Reddit client created successfully{RESET}")
        return reddit
    except Exception as e:
        print(f"Failed to create Reddit client: {RED}{e}{RESET}")
        return None

def fetchSubredditComments(reddit, subreddit_name, com_limit):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        comments = []
        bot_identifier = "*I am a bot, and this action"

        for submission in subreddit.new(limit=com_limit):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                if bot_identifier not in comment.body:
                    comments.append(comment.body)
                if len(comments) >= com_limit:
                    return comments

        return comments
    except Exception as e:
        print(f"{RED}Failed{RESET} to fetch comments from '{subreddit_name}': {RED}{e}{RESET}")
        return []
