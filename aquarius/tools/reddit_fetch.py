import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal

import praw
from dotenv import load_dotenv

load_dotenv()

# Define your Reddit API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SCRAPER_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT
)


def fetch_top_posts(
    subreddit_name: str,
    time_filter: Literal["hour", "day", "week", "month", "year", "all"] = "week",
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Fetch the top posts from a specified subreddit within a given time filter.

    Attributes:
        subreddit_name (str): The name of the subreddit.
        time_filter (Literal["hour", "day", "week", "month", "year", "all"], optional): The time filter to apply
            when fetching top posts. Defaults to "week".
        limit (int, optional): The maximum number of posts to fetch. Default 10.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing details of a top post:
            - 'title' (str): The title of the post.
            - 'url' (str): The URL of the post.
            - 'content' (str): The selftext content of the post.
            - 'score' (int): The score of the post.
            - 'created' (str): The creation time of the post in the format "YYYY-MM-DD HH:MM:SS TZ".
    """
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(time_filter=time_filter, limit=limit)

    posts = []
    for post in top_posts:
        # We need to filter posts from the last week manually because praw's 'week' filter
        # includes posts from the last 7 days, which might not be exactly a week
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        if post.created_utc > one_week_ago.timestamp():
            posts.append(
                {
                    "title": post.title,
                    "url": post.url,
                    "content": post.selftext,
                    "score": post.score,
                    "created": datetime.fromtimestamp(
                        post.created_utc, tz=timezone.utc
                    ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                }
            )

    return posts
