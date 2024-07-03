import praw
from datetime import datetime, timezone, timedelta

# Define your Reddit API credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
USER_AGENT = 'your_user_agent'

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

def fetch_top_posts(subreddit_name, time_filter='week', limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(time_filter=time_filter, limit=limit)
    
    posts = []
    for post in top_posts:
        # We need to filter posts from the last week manually because praw's 'week' filter
        # includes posts from the last 7 days, which might not be exactly a week
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        if post.created_utc > one_week_ago.timestamp():
            posts.append({
                'title': post.title,
                'url': post.url,
                'content': post.selftext,
                'score': post.score,
                'created': datetime.fromtimestamp(post.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
            })
    
    return posts

# Example usage
if __name__ == '__main__':
    subreddit_name = 'news'
    posts = fetch_top_posts(subreddit_name)

    for post in posts:
        print(f"Title: {post['title']}")
        print(f"URL: {post['url']}")
        print(f"Content: {post['content']}")
        print(f"Score: {post['score']}")
        print(f"Created: {post['created']}")
        print('-' * 80)