from datetime import datetime, timedelta, timezone

import pytest

from aquarius.tools.reddit_fetch import fetch_reddit_posts


class MockRedditPost:
    def __init__(self, title, url, selftext, created_utc):
        self.title = title
        self.url = url
        self.selftext = selftext
        self.created_utc = created_utc


class MockSubreddit:
    def top(self, time_filter, limit):
        # Return a list of mock posts based on the limit
        now = datetime.now(timezone.utc)
        if time_filter == "week":
            return [
                MockRedditPost(
                    "Test Post 1",
                    "http://example.com/1",
                    "This is a test post 1",
                    (now - timedelta(days=1)).timestamp(),
                ),
                MockRedditPost(
                    "Test Post 2",
                    "http://example.com/2",
                    "This is a test post 2",
                    (now - timedelta(days=2)).timestamp(),
                ),
                MockRedditPost(
                    "Old Post",
                    "http://example.com/old",
                    "This is an old post",
                    (now - timedelta(days=8)).timestamp(),
                ),
            ][:limit]
        return []


class MockReddit:
    def subreddit(self, subreddit_name):
        return MockSubreddit()


@pytest.fixture
def mock_reddit(monkeypatch):
    def mock_reddit_instance(*args, **kwargs):
        return MockReddit()

    monkeypatch.setattr("aquarius.tools.reddit_fetch.praw.Reddit", mock_reddit_instance)


def test_fetch_reddit_posts(mock_reddit):
    posts = fetch_reddit_posts(subreddit_name="LocalLLaMA", time_filter="week", limit=2)

    # Assertions
    assert len(posts) == 2
    assert posts[0]["title"] == "Test Post 1"
    assert posts[0]["url"] == "http://example.com/1"
    assert posts[0]["content"] == "This is a test post 1"
    assert posts[1]["title"] == "Test Post 2"
    assert posts[1]["url"] == "http://example.com/2"
    assert posts[1]["content"] == "This is a test post 2"


def test_fetch_reddit_posts_no_recent_posts(mock_reddit):
    posts = fetch_reddit_posts(subreddit_name="LocalLLaMA", time_filter="week", limit=3)

    # Assertions
    assert len(posts) == 2
    assert posts[0]["title"] == "Test Post 1"
    assert posts[0]["url"] == "http://example.com/1"
    assert posts[0]["content"] == "This is a test post 1"
    assert posts[1]["title"] == "Test Post 2"
    assert posts[1]["url"] == "http://example.com/2"
    assert posts[1]["content"] == "This is a test post 2"
    # The third post is older than one week and should not be included
