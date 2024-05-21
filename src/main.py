import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trade.assets import getAsset
from clients.reddit_client import createRedditClient, fetchSubredditComments
from src.styles import GREEN, RED, BLUE, YELLOW, RESET

print("Contrabot V1.0.0")
print("An inverse sentiment trading bot")
print("------------")
print("Command list")
print("------------")
print("Specify Reddit Search: !reddit")
print("Advanced Search Settings: !comLimit, !recency, !sortBy, !minUpvote, !minKarma")
print("Orders: !closeOrder, !getOrder, !modOrder, !sendOrder")
print("Assets: !getAsset")
print("Positions: !closeAllPos, !closePos, !getAllPos, !getPos")
print("Full Docs: !docs")

def main():
    while True:
        print(f"Enter command: {YELLOW}", end="")
        command = input().strip()
        print(f"{RESET}", end="")  

        if command == "!reddit":
            reddit = createRedditClient()
            if reddit:
                subreddit_name = input("Enter subreddit name: ").strip()
                try:
                    com_limit = int(input("Enter number of comments to analyze: ").strip())
                    comments = fetchSubredditComments(reddit, subreddit_name, com_limit)
                    for i, comment in enumerate(comments, start=1):
                        print(f"{BLUE}COMMENT {i}{RESET}: {comment}")
                except ValueError:
                    print(f"{RED}Invalid input for number of comments{RESET}")
            else:
                print(f"{RED}Failed to create Reddit client{RESET}")
        
        elif command == "!getAsset":
            while True:
                asset_id = input("Enter asset ID or symbol: ").strip()
                if asset_id.isalpha(): #verify input before making call
                    break
                else:
                    print(f"{RED}Invalid input. Please enter only alphabetic characters.{RESET}")
            try:
                result = getAsset(asset_id)
                print(f"{BLUE}Asset Information{RESET}:", result)
            except Exception as e:
                print(f"Error: {RED}{e}{RESET}")
        
        elif command == "!quit":
            print(f"{GREEN}Exiting program{RESET}")
            break
        
        else:
            print(f"{RED}Unknown command. Available commands: !reddit, !getAsset, !quit{RESET}")

if __name__ == "__main__":
    main()
