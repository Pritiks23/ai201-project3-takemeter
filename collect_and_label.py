import requests
import pandas as pd
from groq import Groq
from tqdm import tqdm

client = Groq(api_key="YOUR_GROQ_API_KEY")

HEADERS = {"User-Agent": "nba-labeler"}

# ---------------- FETCH REAL r/nba DATA (NO AUTH) ----------------
import requests

def fetch(limit=200):
    url = f"https://old.reddit.com/r/nba/hot.json?limit={limit}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    }

    res = requests.get(url, headers=headers, timeout=10)

    if res.status_code != 200:
        print("HTTP ERROR:", res.status_code)
        print(res.text[:200])
        return []

    data = res.json()["data"]["children"]

    posts = []
    for p in data:
        d = p["data"]
        text = (d.get("title") or "") + " " + (d.get("selftext") or "")
        posts.append(text.strip())

    return posts
# ---------------- GROQ LABELING ----------------
def label(text):
    prompt = f"""
Classify this r/nba post into ONE label:

- Analytical Breakdown
- Hot Take / Reactionary Opinion
- Meme / Humor
- Informational / News

Return ONLY the label.

Text:
{text}
"""

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content.strip()

# ---------------- PIPELINE ----------------
posts = fetch(200)

rows = []
for p in tqdm(posts):
    rows.append({
        "text": p,
        "label": label(p),
        "notes": ""
    })

df = pd.DataFrame(rows)
df.to_csv("nba_labeled.csv", index=False)

print("Saved nba_labeled.csv")
