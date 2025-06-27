"""Reddit Automation with PRAW"""

# OAuth2 Quickstart: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
# Authentication: https://praw.readthedocs.io/en/stable/getting_started/authentication.html#authenticating-via-oauth

# -- Imports, with help links
import os # https://www.digitalocean.com/community/tutorials/python-os-module#python-os-module
import time # https://www.programiz.com/python-programming/time
import dotenv # https://www.geeksforgeeks.org/using-python-environment-variables-with-python-dotenv/
import logging # https://docs.python.org/3/howto/logging.html#basic-logging-tutorial 
from typing import Any, Optional # https://www.digitalocean.com/community/tutorials/python-typing-module
from pathlib import Path # https://realpython.com/python-pathlib/#path-instantiation-with-pythons-pathlib
from pprint import pprint # https://realpython.com/python-pretty-print/#working-with-pprint
from datetime import datetime # https://www.programiz.com/python-programming/datetime

# -- PRAW: https://github.com/praw-dev/praw?tab=readme-ov-file#quickstart | https://praw.readthedocs.io/en/stable/
from praw import Reddit
from praw.models.reddit.redditor import Redditor
from praw.models.reddit.subreddit import Subreddit
from prawcore.exceptions import (
    OAuthException, Redirect, RequestException,
    ResponseException, ServerError, Forbidden,
    NotFound, TooManyRequests
    )

from redditor.ai import expound_title

# --------------------------------------------------------------------------------------------------------------------------
# --- Logging
LOG_LEVEL = logging.INFO # logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL

LOG_FILE: Path = Path(__file__).parent.parent.parent / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure the logs directory exists
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, encoding='utf-8', format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger: logging.Logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(stream_handler)
for logger_name in ("praw", "prawcore"):
    praw_logger: logging.Logger = logging.getLogger(logger_name)
    praw_logger.setLevel(LOG_LEVEL)
    praw_logger.addHandler(stream_handler)

# --------------------------------------------------------------------------------------------------------------------------

# -- Environment Variables
DOTENV_FILE: Path = Path(__file__).parent.parent.parent / ".env" 
dotenv.load_dotenv(DOTENV_FILE, override=True) # Load environment variables from .env file

REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "")
REDDIT_USERNAME: str = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASSWORD: str = os.getenv("REDDIT_PASSWORD", "")

# --------------------------------------------------------------------------------------------------------------------------

# Reddit Client, via PRAW 
def create_client() -> Reddit:
    """Create a Reddit client using the `praw` library."""
    attempts = 0

    retries = 3 # Set the number of retries
    delay = 2  # seconds

    while attempts < retries:
        try:
            reddit = Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT,
                username=REDDIT_USERNAME,
                password=REDDIT_PASSWORD
            )

            logger.info("⚪ Authenticating Reddit client...")
            user: Optional[Redditor] = reddit.user.me()  # Raises on failure
            logger.info(f"🟢 Reddit client authenticated as: {user.name}")  # type: ignore

            return reddit

        except OAuthException as e:
            logger.error(f"🔴 Invalid credentials: {e}", exc_info=True)
            break  # Don't retry on bad creds

        except (RequestException, ResponseException, ServerError, TooManyRequests) as e:
            logger.warning(f"🟡 Network/API error on attempt {attempts+1}/{retries}: {str(e)}")
            time.sleep(delay * (attempts + 1))
            attempts += 1

        except Forbidden as e: # type: ignore
            logger.error("🔴 Access forbidden when authenticating: %s", str(e), exc_info=True)
            break

        except Exception as e:
            logger.error("🔴 Unexpected error during client creation: %s", str(e), exc_info=True)
            break

    logger.error("🔴 Failed to authenticate Reddit client after %d attempts.", retries)
    raise RuntimeError("Reddit client authentication failed.")

# PRAW API Rate Limits: https://praw.readthedocs.io/en/stable/getting_started/rate_limits.html
def fetch_latest_posts(reddit: Reddit = create_client(), subreddit_name: str = "politics", limit: int = 5) -> list[dict[str, str]]:
    """Fetch the latest `limit` posts from the specified subreddit. Returns a list of dictionaries containing post details."""
    attempts = 0
    retries = 3
    delay = 2  # seconds

    while attempts < retries:
        try:
            subreddit: Subreddit = reddit.subreddit(subreddit_name)
            subreddit._fetch()  # Detect redirect (invalid subreddit name), Raises prawcore.exceptions.Redirect if invalid

            logger.info(f"⚪ Fetching latest posts from r/{subreddit_name}...")
            posts: list[dict[str, str]] = []
            for submission in subreddit.new(limit=limit):
                posts.append({
                    "title": submission.title,
                    "author": str(submission.author),
                    "upvotes": submission.score,
                    "expounded": expound_title(submission.title) if submission.title else "No title provided",
                })

            logger.info(f"🟢 Fetched {len(posts)} latest posts from r/{subreddit_name}")
            return posts

        except Redirect:
            logger.error(f"🔴 Subreddit r/{subreddit_name} does not exist (redirected).")
            break

        except (RequestException, ResponseException, ServerError, TooManyRequests) as e:
            logger.warning(f"🟡 Network/API error on attempt {attempts + 1}/{retries}: {e}")
            time.sleep(delay * (attempts + 1))
            attempts += 1

        except (Forbidden, NotFound) as e: # type: ignore
            logger.error(f"🔴 Access issue: r/{subreddit_name} - {e}")
            break

        except Exception as e:
            logger.error(f"🔴 Unexpected error fetching posts: {e}", exc_info=True)
            break

    logger.error(f"🔴 Failed to fetch posts from r/{subreddit_name} after {retries} retries.")
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

    subreddit_name: str = input("Enter subreddit name (default: politics): ") or "politics"
    latest_posts: list[dict[str, str]] = fetch_latest_posts(reddit, subreddit_name)
    # logger.info("Latest posts from r/%s:", subreddit_name)
    pprint(f"Latest {len(latest_posts)} posts from r/{subreddit_name}: ")
    [pprint(i) for i in latest_posts]

    print("\n🐬")