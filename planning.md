# planning.md

## Chosen Community
r/nba

I conceptually sampled a mix of recent r/nba-style discourse (game threads, postgame reactions, trade rumor threads, highlight posts, and statistical debates). Across these spaces, the key observable variation is not topic—it’s intent: whether a comment is trying to explain basketball, emotionally react to it, entertain, or speculate.

---

## Label Set

### 1) Analytical Breakdown

**Definition (1 sentence):**  
Posts that use film context, statistics, or schematic reasoning to explain why something happened in a game or player performance.

**Examples:**
- “The Bucks kept getting punished in drop coverage because the weak-side tag was late every possession; you can see the rotation is one beat behind on every high PnR.”
- “SGA’s efficiency isn’t just scoring volume—his shot profile shifted to 10–16 ft pull-ups this season, which is why his TS% jumped despite similar usage.”

**Uncertain case (boundary test):**
- “Jokic looked tired in the 4th, Denver should’ve staggered Murray more.”  
  → Is this analysis (rotation critique) or just opinionated reaction without evidence?

---

### 2) Hot Take / Reactionary Opinion

**Definition (1 sentence):**  
Strongly framed judgments about players/teams that prioritize emotional certainty or ranking over evidence or explanation.

**Examples:**
- “Luka is already better than prime Harden and it’s not close anymore.”
- “The Celtics are frauds every time they face a real defense, nothing has changed since last year.”

**Uncertain case (boundary test):**
- “LeBron is still top 5 in the league when healthy.”  
  → Is this a measured ranking or a hot take depending on context/justification?

---

### 3) Meme / Humor

**Definition (1 sentence):**  
Content whose primary goal is entertainment through irony, exaggeration, jokes, or format memes rather than basketball explanation.

**Examples:**
- “I, for one, welcome our new Nikola Jokic basketball overlord.”
- “NBA refs when they see a clean block: 🚨🚨🚨 personal foul, automatic execution”

**Uncertain case (boundary test):**
- “The Timberwolves are legally required to lose in 6 games.”  
  → Could be humor or disguised criticism depending on thread context.

---

### 4) Informational / News / Transaction Update

**Definition (1 sentence):**  
Posts that relay factual updates such as injuries, trades, signings, or schedule/game result information without interpretation.

**Examples:**
- “The Lakers have listed Anthony Davis as questionable with a right ankle sprain for tonight’s game.”
- “Breaking: The Nets are reportedly trading two second-round picks for a protected first-rounder.”

**Uncertain case (boundary test):**
- “Woj says the deal is ‘close,’ sources indicate final details pending.”  
  → Is this pure reporting or speculative framing?

---

## Mutual Exclusivity Check

These labels are mostly separable by intent, not content:

- If a post explains mechanisms → **Analytical**
- If it asserts rankings/strength without reasoning → **Hot Take**
- If it prioritizes humor/irony → **Meme**
- If it transmits factual updates → **News/Informational**

**Edge overlap exists between:**
- Hot Take vs Analytical (when minimal reasoning is attached)
- Meme vs Hot Take (when sarcasm mimics opinion)
- News vs Analytical (when reporting includes interpretation)

To maintain exclusivity in annotation, the primary rule is:  
**Classify by dominant communicative intent, not surface meaning.**

---

## Data Collection Plan

**Where examples will be collected:**
- r/nba:
  - Game threads (live reactions, short-form takes)
  - Post-game discussion threads (analysis vs emotional reaction separation is strongest here)
  - Trade rumor / breaking news threads (News vs Hot Take boundary)
  - Highlight/video posts with comment sections (meme + reaction density)
  - Top weekly posts (higher-signal analytical breakdowns tend to surface here)

**Sampling strategy:**
- Stratified sampling across:
  - High engagement posts (top 1–10% upvoted)
  - Mid-tier posts (moderate engagement, more noise)
  - Low visibility posts (to capture underrepresented analytical content)

**Target per label (initial goal):**
- Analytical Breakdown: 60 examples  
- Hot Take / Reactionary Opinion: 60 examples  
- Meme / Humor: 60 examples  
- Informational / News: 60 examples  
**Total initial dataset: ~240 examples**

**If a label is underrepresented after 200 examples:**
- Rebalance sampling explicitly:
  - Increase search in niche threads (e.g., post-game film breakdown posts for Analytical)
  - Use keyword filters (“film”, “rotation”, “TS%”, “trade”, “breaking”) to surface rare classes
- If still underrepresented:
  - Relax sampling constraints but preserve label definition integrity (do not broaden definitions)
  - Log imbalance as a dataset limitation rather than inflating synthetic examples
  - Optionally merge borderline cases into “Hybrid” only if analytically justified (not default)

---

## Evaluation Metrics

Accuracy alone is insufficient because:
- Class distribution is likely imbalanced
- Two labels (Analytical vs Hot Take, Meme vs Hot Take) are semantically close
- Misclassification cost is asymmetric in downstream use (e.g., mislabeling News is more harmful than mislabeling Meme)

**Primary metrics:**
- Macro F1 score  
  → Ensures performance across all labels is equally weighted, preventing majority-class dominance.

- Per-class Precision and Recall  
  → Critical for understanding whether the model over-generates certain discourse types (e.g., labeling too many Hot Takes as Analytical).

- Confusion Matrix  
  → Needed to diagnose systematic boundary failures (especially:
  Analytical ↔ Hot Take,
  Meme ↔ Hot Take).

**Secondary metric:**
- Cohen’s Kappa (optional)  
  → Measures agreement beyond chance; useful for evaluating consistency if multiple annotators or LLM-assisted labeling is used.

---

## Definition of Success

The classifier is considered useful if:

- Macro F1 ≥ 0.80  
- No single class has F1 < 0.75  
- News/Informational precision ≥ 0.90 (high trust requirement)
- Analytical vs Hot Take confusion rate ≤ 15% of those classes combined

**Operational usefulness criteria:**
- A human moderator reviewing outputs would agree with model labels ≥ 85% of the time in a random sample of 100 predictions.
- The model must correctly separate:
  - at least 8/10 News posts from non-News content
  - at least 7/10 Analytical posts from Hot Takes in mixed threads

**Success definition clarity check:**
Yes—criteria are now:
- Quantified (F1 thresholds, precision thresholds, confusion limits)
- Per-class constrained (not just global accuracy)
- Tied to real moderation utility (not just offline score)
This allows an objective pass/fail evaluation after annotation and training.

---

## AI Tool Plan

This project is annotation- and evaluation-driven rather than implementation-heavy, so AI tools are used for structured linguistic work rather than code generation.

### 1) Label Stress-Testing (Pre-Annotation Validation)

**Approach:**
- Provide label definitions and boundary cases to an LLM.
- Prompt it to generate 5–10 synthetic r/nba-style posts that lie explicitly at boundaries:
  - Analytical vs Hot Take
  - Meme vs Hot Take
  - News vs Analytical

**Purpose:**
- Identify ambiguity before dataset collection.
- If generated examples are hard to classify consistently, label definitions are revised immediately.

**Iteration rule:**
- If ≥30% of generated boundary examples are ambiguous to human judgment → refine definitions before collecting 200 examples.

---

### 2) Annotation Assistance

**Approach:**
- Use an LLM as a *pre-labeling assistant* for the first pass over collected examples.
- Human annotator (you) performs final verification and correction.

**Tool choice:**
- GPT-style model (or equivalent LLM classifier prompt pipeline)

**Tracking mechanism:**
- Each example stored with fields:
  - raw_text
  - model_prelabel
  - human_label
  - agreement_flag (0/1)

**Important constraint:**
- Pre-labels are explicitly treated as suggestions, not ground truth.

**Disclosure:**
- Maintain a log of:
  - percentage of examples pre-labeled by AI
  - override rate (how often human changes AI label)

---

### 3) Failure Analysis

**Approach:**
- After evaluation, extract:
  - false positives per class
  - false negatives per class
- Feed misclassified examples into an LLM with prompt:
  - “Identify patterns in errors across these misclassified examples.”

**What will be analyzed:**
- Systematic confusion pairs (e.g., Analytical → Hot Take drift)
- Lexical triggers (e.g., “fraud”, “washed”, “GOAT” causing Hot Take bias)
- Structural features (lack of statistics vs presence of named metrics)
- Context dependence (short comments vs multi-sentence reasoning)

**Verification strategy:**
- Manually inspect a random subset (at least 30% of flagged patterns)
- Confirm whether LLM-identified patterns hold statistically across the error set
- Reject any pattern not reproducible across multiple examples

---

## Community Description (for planning.md)

r/nba is a high-volume discourse community where basketball conversation ranges from rigorous statistical and tactical analysis to emotionally charged rankings, humor-driven meme content, and rapid-fire news updates. The distinctions matter because users actively evaluate credibility: “good analysis” is socially rewarded, while “hot takes” are often contested or satirized depending on context. These labels help separate explanatory reasoning from reaction, humor, and information reporting, which is essential for understanding how meaning and authority are constructed in NBA online discourse.

