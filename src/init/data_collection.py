import praw
import config

class DataCollector:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            user_agent=config.REDDIT_USER_AGENT
        )

    def fetch_comments(self, subreddit, limit=100):
        comments = []
        for comment in self.reddit.subreddit(subreddit).comments(limit=limit):
            comments.append(comment.body)
        return comments
