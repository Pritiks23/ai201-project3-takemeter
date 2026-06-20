import requests
import pandas as pd
from groq import Groq
from tqdm import tqdm

client = Groq(api_key="YOUR_GROQ_API_KEY")

HEADERS = {"User-Agent": "nba-labeler"}

# ---------------- FETCH REAL r/nba DATA (NO AUTH) ----------------
def fetch(limit=200):
    url = f"https://www.reddit.com/r/nba/hot.json?limit={limit}"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; nba-labeler/1.0)"
    }

    res = requests.get(url, headers=headers)

    # 🚨 debug safety check
    if res.status_code != 200:
        print("HTTP ERROR:", res.status_code)
        print(res.text[:300])
        return []

    try:
        json_data = res.json()
    except Exception:
        print("NOT JSON RESPONSE:")
        print(res.text[:300])
        return []

    posts = []
    for p in json_data["data"]["children"]:
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
