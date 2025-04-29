# https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
# https://praw.readthedocs.io/en/stable/getting_started/authentication.html#authenticating-via-oauth
import os
import dotenv
import praw
import pathlib

from praw.models.reddit.subreddit import Subreddit

# -- Environment Variables
DOTENV_FILE: pathlib.Path = pathlib.Path(__file__).parent.parent.parent / ".env" 
dotenv.load_dotenv(DOTENV_FILE, override=True) # Load environment variables from .env file

REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "")
REDDIT_USERNAME: str = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASSWORD: str = os.getenv("REDDIT_PASSWORD", "")

# -- Reddit Client
reddit = praw.Reddit(
    # Read-only access
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    # OAuth2 access
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
    )


if __name__ == "__main__":
    # print(DOTENV_FILE.is_file()) # .is_file() implies .exists() # 🧪 check if DOTENV_FILE exists
    # print(reddit.read_only) # 🧪 test read only access
    # for submission in reddit.subreddit("politics").hot(limit=5):
    #     print(submission.title)
    # subbreddit: Subreddit = reddit.subreddit("learnpython")
    # print(subbreddit.display_name)
    # print(reddit.user.me()) 

    print("\n🐬")