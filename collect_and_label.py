import pandas as pd
from groq import Groq
from tqdm import tqdm

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

LABELS = [
    "Analytical Breakdown",
    "Hot Take / Reactionary Opinion",
    "Meme / Humor",
    "Informational / News"
]

def generate_dataset(n=220):
    prompt = f"""
Generate {n} realistic Reddit r/nba posts/comments.

Include:
- game analysis
- emotional reactions
- memes
- trade/news updates
- player debates

Make them look like real Reddit content.

Return as a numbered list.
"""

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return [
        x.strip("- ").strip()
        for x in res.choices[0].message.content.split("\n")
        if x.strip()
    ]

def label(text):
    prompt = f"""
Classify into ONE:

- Analytical Breakdown
- Hot Take / Reactionary Opinion
- Meme / Humor
- Informational / News

Return only label.

Text:
{text}
"""

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content.strip()

posts = generate_dataset(220)

rows = []
for p in tqdm(posts):
    rows.append({
        "text": p,
        "label": label(p),
        "notes": ""
    })

pd.DataFrame(rows).to_csv("nba_labeled.csv", index=False)

print("Saved nba_labeled.csv")
