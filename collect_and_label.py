import praw
import pandas as pd
from tqdm import tqdm
from groq import Groq

# ---------------- CONFIG ----------------
REDDIT_LIMIT = 300
OUTPUT_FILE = "nba_labeled.csv"

client = Groq(api_key="YOUR_GROQ_API_KEY")

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="nba-labeling"
)

LABELS = [
    "Analytical Breakdown",
    "Hot Take / Reactionary Opinion",
    "Meme / Humor",
    "Informational / News"
]

# ---------------- DATA COLLECTION ----------------
def collect():
    data = []
    for post in reddit.subreddit("nba").hot(limit=REDDIT_LIMIT):
        text = post.title + (" " + post.selftext if post.selftext else "")
        data.append({"text": text})
    return pd.DataFrame(data)

# ---------------- GROQ LABELING ----------------
def label(text):
    prompt = f"""
Label this r/nba post with ONE of:
- Analytical Breakdown
- Hot Take / Reactionary Opinion
- Meme / Humor
- Informational / News

Return only the label.

Text:
{text}
"""

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content.strip()

# ---------------- MAIN ----------------
df = collect()

df["ai_label"] = [label(t) for t in tqdm(df["text"])]
df["label"] = ""   # human fill later
df["notes"] = ""

df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
