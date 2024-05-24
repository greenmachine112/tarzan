import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trade.assets import getAsset
from clients.reddit_client import createRedditClient, fetchSubredditComments
from src.styles import GREEN, RED, BLUE, CYAN, PURPLE, YELLOW, RESET
from clients.news_client import fetchNews

print("Contrabot V1.0.0")
print("An inverse sentiment trading bot")
print("------------")
print("Command list")
print("------------")
print("Specify Reddit Search: !searchReddit")
print("Advanced Search Settings: !recency <days>, !minUpvote <upvotes>, !minKarma <karma>")
#print("Orders: !closeOrder, !getOrder, !modOrder, !sendOrder")
print("Assets: !getAsset <ticker>")
#print("Positions: !closeAllPos, !closePos, !getAllPos, !getPos")
#print("Full Docs: !docs")
print("Fetch News: !fetchNews <ticker> <sortMethod> <fromTime> <toTime>")
print("Terminate Program: !quit")

# Default params
recency = 1  # day(s)
minUpvotes = 0
minKarma = 0

def main():
    global recency, minUpvotes, minKarma
    while True:
        print("------------")
        print(f"Enter command: {BLUE}", end="")
        command = input().strip()
        print(f"{RESET}", end="")

        if command.startswith("!searchReddit"):
            reddit = createRedditClient()
            if reddit:
                handleRedditCommand(reddit)
            else:
                print(f"{RED}Failed to create Reddit client{RESET}")

        elif command.startswith("!getAsset"):
            assetId = command.split()[1].strip('$')
    
            if assetId.isalpha():
                try:
                    result = getAsset(assetId)
                    print(f"{BLUE}Asset Information{RESET}:", result)
                except Exception as e:
                    print(f"Error: {RED}{e}{RESET}")
            else:
                print(f"{RED}Invalid input. Only alphabetic characters are allowed.{RESET}")

        elif command.startswith("!recency"):
            try:
                recency = int(command.split()[1].strip())
                if recency > 0:
                    print(f"{GREEN}Recency set to {recency} days{RESET}")
                else:
                    print(f"{RED}Recency must be greater than 0.{RESET}")
            except (ValueError, IndexError):
                print(f"{RED}Invalid input for recency. Usage: !recency <days>{RESET}")

        elif command.startswith("!minUpvote"):
            try:
                minUpvotes = int(command.split()[1].strip())
                if minUpvotes >= 0:
                    print(f"{GREEN}Minimum upvotes set to {minUpvotes}{RESET}")
                else:
                    print(f"{RED}Minimum upvotes must be 0 or greater.{RESET}")
            except (ValueError, IndexError):
                print(f"{RED}Invalid input for minimum upvotes. Usage: !minUpvote <upvotes>{RESET}")

        elif command.startswith("!minKarma"):
            try:
                minKarma = int(command.split()[1].strip())
                if minKarma >= 0:
                    print(f"{GREEN}Minimum author karma set to {minKarma}{RESET}")
                else:
                    print(f"{RED}Minimum author karma must be 0 or greater.{RESET}")
            except (ValueError, IndexError):
                print(f"{RED}Invalid input for minimum author karma. Usage: !minKarma <karma>{RESET}")

        elif command.startswith("!fetchNews"):
            try:
                _, ticker, sortMethod, fromTime, toTime = command.split()
                fetchNews(ticker, sortMethod, fromTime, toTime)
            except ValueError:
                print(f"{RED}Invalid input for fetching news. Usage: !fetchNews <ticker> <sortMethod> <fromTime> <toTime> <outputPath>{RESET}")

        elif command == "!quit":
            print(f"{GREEN}Exiting program{RESET}")
            break

        else:
            print(f"{RED}Unknown command. Available commands: !searchReddit, !getAsset, !recency <days>, !minUpvote <upvotes>, !minKarma <karma>, !getSecForms <ticker>, !fetchNews <ticker> <sortMethod> <fromTime> <toTime> <outputPath>, !quit{RESET}")

def handleRedditCommand(reddit):
    print(f"Enter subreddit name: {BLUE}", end="")
    subredditName = input().strip()
    print(f"{RESET}", end="")
    
    print(f"Enter a stock ticker (e.g., $AAPL): {BLUE}", end="")
    ticker = input()
    print(f"{RESET}", end="")
    if not ticker.startswith("$"):
        print(f"{RED}Invalid ticker format. Preceed all tickers with '$'{RESET}")
        return

    variations = []
    addVariations = input("Do you want to add variations? (yes/no): ").lower() #case insensitive
    if addVariations == 'yes':
        print(f"Enter each variation on a new line. '/n' to submit{BLUE}")
        while True:
            variation = input()
            if variation.lower() == '/n':
                break
            variations.append(variation)

    print(f"{GREEN}Searching Reddit for {ticker} and variations: {variations} in subreddit: {subredditName}{RESET}")
    try:
        comLimit = int(input("Enter number of comments to analyze: ").strip())
        comments = fetchSubredditComments(reddit, subredditName, ticker, variations, comLimit, recency, minUpvotes, minKarma)
        if comments:
            with open('datasets/reddit.json', 'w') as file:
                json.dump(comments, file, indent=4)
            print(f"{GREEN}Comments saved to reddit.json{RESET}")
        else:
            print(f"{RED}No comments found matching the criteria{RESET}")
    except ValueError:
        print(f"{RED}Invalid input for number of comments{RESET}")

if __name__ == "__main__":
    main()
