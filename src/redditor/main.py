# https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
# https://praw.readthedocs.io/en/stable/getting_started/authentication.html#authenticating-via-oauth
import os
import dotenv
import logging # https://docs.python.org/3/howto/logging.html#basic-logging-tutorial 
from typing import Any, Optional
from pathlib import Path
from pprint import pprint
from datetime import datetime

# -- PRAW: https://github.com/praw-dev/praw?tab=readme-ov-file#quickstart | https://praw.readthedocs.io/en/stable/
from praw import Reddit
from praw.models.reddit.redditor import Redditor
from praw.models.reddit.subreddit import Subreddit

# -- Logging Setup
LOG_LEVEL = logging.INFO # logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL

LOG_FILE: Path = Path(__file__).parent.parent.parent / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure the logs directory exists
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, encoding='utf-8', format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger: logging.Logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(stream_handler)

# -- Enable DEBUG logging for praw and prawcore to console
for logger_name in ("praw", "prawcore"):
    praw_logger = logging.getLogger(logger_name)
    praw_logger.setLevel(LOG_LEVEL)
    praw_logger.addHandler(stream_handler)

# -- Environment Variables
DOTENV_FILE: Path = Path(__file__).parent.parent.parent / ".env" 
dotenv.load_dotenv(DOTENV_FILE, override=True) # Load environment variables from .env file

REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "")
REDDIT_USERNAME: str = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASSWORD: str = os.getenv("REDDIT_PASSWORD", "")

# 
def create_client() -> Reddit:
    """Create a Reddit client using the `praw` library."""
    try:
        reddit = Reddit(
            # Read-only
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            # OAuth2 
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD
        )

        #  Validate credentials
        logger.info("⚪ Authenticating Reddit client...")
        _: Optional[Redditor] = reddit.user.me()  # 🧪 raises if credentials are invalid
        logger.info("🟢 Reddit client authenticated as: %s", _.name) # type: ignore

        return reddit

    except Exception as e:
        logger.error("🔴 Failed to create Reddit client: %s", str(e), exc_info=True)
        raise

# 
def fetch_latest_posts(reddit: Reddit, subreddit_name: str, limit: int = 5) -> list[dict[str, str]]:
    """Fetch the latest `limit` posts from the specified subreddit. Returns a list of dictionaries containing post details."""
    try:
        subreddit: Subreddit = reddit.subreddit(subreddit_name)
        posts: list[Any] = []

        for submission in subreddit.new(limit=limit):
            post_info: dict[str, Any] = {
                "title": submission.title,
                "author": str(submission.author),
                "upvotes": submission.score
                }
            posts.append(post_info)

        logger.info(f"🟢 Fetched {len(posts)} latest posts from r/{subreddit_name}")
        return posts

    except Exception as e:
        logger.error(f"🔴 Failed to fetch posts from r/{subreddit_name}: {str(e)}", exc_info=True)
        return []


if __name__ == "__main__":
    reddit: Reddit = create_client()
    
    pprint(LOG_FILE.is_file()) # 🧪 check if LOG_FILE exists
    # pprint(DOTENV_FILE.is_file()) # .is_file() implies .exists() # 🧪 check if DOTENV_FILE exists
    # pprint(reddit.read_only) # 🧪 test read only access
    # for submission in reddit.subreddit("politics").hot(limit=5):
    #     pprint(submission.title)
    # subbreddit: Subreddit = reddit.subreddit("learnpython")
    # pprint(subbreddit.display_name)
    # pprint(reddit.user.me()) 

    subreddit_name: str = "learnpython"
    latest_posts: list[dict[str, str]] = fetch_latest_posts(reddit, subreddit_name)
    # logger.info("Latest posts from r/%s:", subreddit_name)
    pprint(f"Latest {len(latest_posts)} posts from r/{subreddit_name}: ")
    [pprint(i) for i in latest_posts]

    print("\n🐬")