"""FastAPI server"""
# ⚠️ Recommended: Use Async PRAW for asynchronous implementation: https://asyncpraw.readthedocs.io/en/stable/
import io
from contextlib import asynccontextmanager
import logging
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.datastructures import FormData
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse as TemplateResponse

import os
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append("/app/src")  # If /app/src is your mounted path in Docker


# from ..main import create_client, fetch_latest_posts  # uncomment to use in Docker
from redditor.main import create_client, fetch_latest_posts  # uncomment to use in standalone mode

# -- Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
LOG_FILE: Path = Path(__file__).parent.parent.parent / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure the logs directory exists
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, encoding='utf-8', format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger: logging.Logger = logging.getLogger(__name__)


# -- Lifecycle events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for the FastAPI app."""
    logger.info("🛫 Starting up...")
    yield
    logger.info("🛬 Shutting down...")

app = FastAPI(title="Redditor Demo", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for CORS
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# -- Static files and templates
app.mount("/static", StaticFiles(directory="src/redditor/server/static"), name="static")
templates = Jinja2Templates(directory="src/redditor/server/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request, "posts": []})

@app.post("/fetch_posts/", response_class=HTMLResponse)
async def fetch_posts(request: Request, subreddit: str = Form(...), n: int = Form(5)):
    # Set up in-memory log capture
    # log_stream = io.StringIO()
    # stream_handler = logging.StreamHandler(log_stream)
    # stream_handler.setLevel(logging.INFO)
    # logger.addHandler(stream_handler)

    # Fetch posts
    posts: list[dict[str, str]] = fetch_latest_posts(subreddit_name=subreddit, limit=n)

    # Detach handler and extract lines
    # logger.removeHandler(stream_handler)
    # logs: list[str] = log_stream.getvalue().strip().splitlines()

    # return templates.TemplateResponse("index.html", context={"request": request, "posts": posts, "logs": logs})
    return templates.TemplateResponse("index.html", context={"request": request, "posts": posts})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="localhost", port=8045, log_level="info")

    print("\n🐬")