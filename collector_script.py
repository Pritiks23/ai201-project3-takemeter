import praw
import pandas as pd
from tqdm import tqdm

# ---------- REDDIT AUTH ----------
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="nba-labeling-project"
)

subreddit = reddit.subreddit("nba")

def fetch_posts(limit=300):
    data = []

    for post in tqdm(subreddit.hot(limit=limit)):
        if post.selftext:
            text = post.title + " " + post.selftext
        else:
            text = post.title

        data.append({
            "text": text,
            "label": "",   # blank for now
            "notes": ""
        })

    return pd.DataFrame(data)

df = fetch_posts(300)
df.to_csv("raw_nba_dataset.csv", index=False)
print("Saved raw_nba_dataset.csv")
