# https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
# https://praw.readthedocs.io/en/stable/getting_started/authentication.html#authenticating-via-oauth
import os
import dotenv
import logging
from typing import Any, Optional
from pathlib import Path

from praw import Reddit
from praw.models.reddit.redditor import Redditor
from praw.models.reddit.subreddit import Subreddit

# -- Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger: logging.Logger = logging.getLogger(__name__)    

# -- Environment Variables
DOTENV_FILE: Path = Path(__file__).parent.parent.parent / ".env" 
dotenv.load_dotenv(DOTENV_FILE, override=True) # Load environment variables from .env file

REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "")
REDDIT_USERNAME: str = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASSWORD: str = os.getenv("REDDIT_PASSWORD", "")


def create_client() -> Reddit:
    """
    Create a Reddit client using the praw library.
    """
    try:
        reddit = Reddit(
            # Read-only and OAuth2 access
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD
        )

        # Simple test to validate credentials
        logger.info("⚪ Authenticating Reddit client...")
        _: Optional[Redditor] = reddit.user.me()  # raises if credentials are invalid
        logger.info("🟢 Reddit client authenticated as: %s", _.name) # type: ignore

        return reddit

    except Exception as e:
        logger.error("🔴 Failed to create Reddit client: %s", str(e), exc_info=True)
        raise


def fetch_latest_posts(reddit: Reddit, subreddit_name: str, limit: int = 5) -> list[dict[str, str]]:
    """
    Fetch the latest 'limit' posts from the specified subreddit.
    Returns a list of dictionaries containing post details.
    """
    subreddit: Subreddit = reddit.subreddit(subreddit_name)
    posts: list[Any] = []
    for submission in subreddit.new(limit=limit):
        post_info = {
            "title": submission.title,
            "author": str(submission.author),
            "upvotes": submission.score
        }
        posts.append(post_info)
    return posts

if __name__ == "__main__":
    # print(DOTENV_FILE.is_file()) # .is_file() implies .exists() # 🧪 check if DOTENV_FILE exists
    # print(reddit.read_only) # 🧪 test read only access
    # for submission in reddit.subreddit("politics").hot(limit=5):
    #     print(submission.title)
    # subbreddit: Subreddit = reddit.subreddit("learnpython")
    # print(subbreddit.display_name)
    # print(reddit.user.me()) 

    client: Reddit = create_client()
    subreddit_name: str = "learnpython"
    latest_posts: list[dict[str, str]] = fetch_latest_posts(client, subreddit_name)
    # logger.info("Latest posts from r/%s:", subreddit_name)
    print(f"Latest {len(latest_posts)} posts from r/{subreddit_name}: ")
    [print(i) for i in latest_posts]

    print("\n🐬")