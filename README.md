# r/nba Discourse Classification — Evaluation Report

## 1. Project Overview

This project classifies r/nba-style posts into four discourse categories:

- Analytical  
- Hot Take / Reactionary Opinion  
- Meme / Humor  
- Informational / News / Update  

We evaluate two models:

- Zero-shot baseline (Groq LLM prompting)  
- Fine-tuned DistilBERT classifier  

---

## Dataset Summary

Total examples: **201**

### Label Distribution

- Informational / News / Update → 93  
- Meme / Humor → 41  
- Hot Take / Reactionary Opinion → 41  
- Analytical → 26  

---

## 3. Baseline Model (Groq LLM)

### Overall Performance

- Accuracy: **0.871** (31/31 parseable responses)

---

### Per-class Metrics

                            precision    recall  f1-score   support

Analytical 1.00 0.75 0.86 4
Hot Take / Reactionary Opinion 0.78 1.00 0.88 7
Meme / Humor 1.00 0.50 0.67 6
Informational / News / Update 0.88 1.00 0.93 14


---

### Key Baseline Confusions

Before analyzing errors, an LLM-assisted review of misclassified predictions was used to surface patterns. The following recurring issues were identified:

- Meme posts often confused with Hot Takes due to similar emotional intensity and slang  
- Analytical posts misclassified as Hot Takes when evaluative language lacked explicit reasoning structure  
- Informational posts occasionally absorbed analytical or stat-heavy content  
- Short, low-context posts showed the highest instability across all categories  

---

### Baseline Failure Modes

The baseline struggles most with:

- Meme vs Hot Take boundary  
- Analytical vs Hot Take confusion  
- Occasional blending of Informational and Analytical content  

Overall, the model relies heavily on surface-level lexical cues and tone rather than discourse intent or reasoning structure.

---

## 4. Fine-tuned Model (DistilBERT)

### Overall Performance

- Accuracy: **0.516** (17/31 correct)

---

### Per-class Metrics

                            precision    recall  f1-score   support

Analytical 0.00 0.00 0.00 4
Hot Take / Reactionary Opinion 0.38 0.71 0.50 7
Meme / Humor 0.00 0.00 0.00 6
Informational / News / Update 0.61 0.79 0.69 14


---

### Confusion Matrix (Fine-tuned Model)

| True \ Predicted              | Analytical | Hot Take | Meme | Informational |
|------------------------------|------------|----------|------|---------------|
| Analytical                   | 0          | 3        | 0    | 1             |
| Hot Take / Reactionary       | 0          | 5        | 0    | 2             |
| Meme / Humor                 | 0          | 3        | 0    | 3             |
| Informational / News         | 0          | 3        | 0    | 11            |

---

### Key Observation

The fine-tuned model collapsed heavily toward:

- Hot Take  
- Informational  

It failed to learn:

- Meme structure entirely  
- Analytical reasoning patterns  

---

## 5. Error Analysis (Fine-tuned Model)

### Example 1  
**Text:** Sabonis elite passing big analysis continues  
- True: Analytical  
- Predicted: Informational  
- Issue: “analysis” keyword triggers news-style interpretation despite lack of structured reasoning  

---

### Example 2  
**Text:** Hot take defense wins championships is outdated framing  
- True: Hot Take  
- Predicted: Informational  
- Issue: Opinionated framing misinterpreted as neutral reporting due to lack of emotional markers  

---

### Example 3  
**Text:** He got cooked clip goes viral again  
- True: Meme  
- Predicted: Hot Take  
- Issue: Slang (“cooked”) misread as criticism rather than humor  

---

### Example 4  
**Text:** Franz Wagner efficiency leap analysis  
- True: Analytical  
- Predicted: Hot Take  
- Issue: Short statistical phrase lacks explicit reasoning structure  

---

### Example 5  
**Text:** Giannis: We just need to be more physical after loss  
- True: Informational  
- Predicted: Hot Take  
- Issue: Quote-like structure triggers opinion classification  

---

### Example 6  
**Text:** Every time I check box score, someone random has 40 points  
- True: Meme  
- Predicted: Hot Take  
- Issue: Exaggeration interpreted as opinion instead of humor  

---

## 6. Sample Fine-tuned Predictions

| Text | Predicted Label | Confidence | Notes |
|------|----------------|------------|------|
| Sabonis elite passing big analysis continues | Informational | 0.28 | Stat-like phrasing |
| Hot take defense wins championships is outdated framing | Informational | 0.27 | Opinion misread as neutral update |
| He got cooked clip goes viral again | Hot Take | 0.27 | Slang misinterpreted |
| Franz Wagner efficiency leap analysis | Hot Take | 0.28 | Keyword-driven prediction |
| Giannis: We just need to be more physical | Hot Take | 0.27 | Quote structure bias |

### Correct Example

| Text | Predicted | Confidence | Why Correct |
|------|-----------|------------|-------------|
| Knicks continue strong defensive rating streak | Informational | 0.31 | Matches news-style reporting with metrics |

---

## 7. Model Comparison

| Model | Accuracy |
|------|---------|
| Zero-shot baseline (Groq) | 0.871 |
| Fine-tuned DistilBERT | 0.516 |

**Regression after fine-tuning:** -0.355  

---

## 8. Key Findings & Interpretation

### What the model captured well
- Informational posts with clear news-like structure  
- Explicit game updates, clips, and reporting language  

### What it failed to capture
- Meme vs Hot Take distinction (completely collapsed)  
- Analytical reasoning structure (beyond keywords like “analysis”)  
- Discourse intent (humor vs opinion vs reporting)  

---

## 9. Spec Reflection

### What the spec helped with

The label definitions enforced a clear separation between:

- Opinion (Hot Take)  
- Humor (Meme)  
- Factual reporting (Informational)  
- Reasoning (Analytical)  

This improved annotation consistency and reduced ambiguity during labeling.

---

### Where implementation diverged

In practice, the model:

- Overweighted lexical cues (“analysis”, “clip”, “hot take”)  
- Failed to encode discourse intent  
- Collapsed overlapping semantic regions, especially Meme vs Hot Take  

This indicates that the dataset is more separable under LLM prompting than under a small encoder model.

---

## 10. AI Usage Disclosure

### Instance 1: Baseline debugging (prompt + parsing issue)
- Used AI to diagnose why outputs were unparseable  
- Identified `.lower()` normalization and substring matching issue  
- Updated matching logic accordingly  

### Instance 2: Error pattern analysis
- Used AI to analyze misclassified examples  
- Identified confusion clusters:
  - Meme ↔ Hot Take  
  - Analytical ↔ Hot Take  
  - Informational ↔ Analytical overlap  
- Verified patterns manually on sampled errors  

---

## 11. Conclusion

The baseline LLM performs strongly due to rich semantic understanding and discourse sensitivity, while the fine-tuned DistilBERT model struggles due to limited capacity to encode nuanced intent differences between closely related classes. The dominant challenge is not topic recognition, but stance and discourse framing separation, particularly between humor, opinion, and analytical reasoning.

---


### Conclusion: Why the model collapsed

The fine-tuned DistilBERT model collapsed to significantly lower performance because it failed to learn fine-grained discourse boundaries between labels that rely on intent rather than surface-level wording. Instead of distinguishing between humor, opinion, and analytical reasoning, the model primarily clustered examples based on lexical similarity, causing it to merge multiple categories into a few dominant predictions like Hot Take and Informational.

This issue was further amplified by class imbalance, particularly the limited number of Analytical and Meme examples, which prevented the model from learning stable decision boundaries for these classes. As a result, the model overfit to common keywords and structural cues rather than true discourse meaning, leading to poor generalization compared to the zero-shot baseline.

## Extra credit: 
## Inter-Annotator Reliability  
We measured inter-annotator agreement using a subset of 30+ posts labeled independently by two annotators. The results showed strong overall agreement, indicating that the label definitions were generally clear and consistently applied across annotators. Disagreements were mainly concentrated in edge cases between *Hot Take* and *Analytical*, where tone and intent were ambiguous.

## Confidence Calibration  
We observed a weak but noticeable relationship between confidence scores and prediction accuracy in the fine-tuned model. Higher confidence predictions were more often correct, but there were still several overconfident misclassifications, especially between *Hot Take* and *Informational* categories.

## Error Pattern Analysis  
A consistent error pattern emerged between *Analytical* and *Hot Take / Reactionary Opinion*, where evaluative basketball commentary was frequently misclassified as reactionary due to surface-level wording. The model also struggled with *Meme / Humor*, often confusing slang-heavy humorous posts as opinion-based content, showing a systematic failure to capture discourse intent over lexical cues.
