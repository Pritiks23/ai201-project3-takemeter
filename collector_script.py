import praw
import pandas as pd
from tqdm import tqdm

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="nba-labeling-project"
)

subreddit = reddit.subreddit("nba")

def fetch_posts(limit=300):
    data = []

    for post in tqdm(subreddit.hot(limit=limit)):
        text = post.title + (" " + post.selftext if post.selftext else "")

        data.append({
            "text": text,
            "label": "",
            "notes": "",
            "ai_label": ""
        })

    return pd.DataFrame(data)

df = fetch_posts(300)
df.to_csv("raw_nba_dataset.csv", index=False)
