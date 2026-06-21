 r/nba Discourse Classification — Evaluation Report
1. Project Overview

This project classifies r/nba-style posts into four discourse categories:

Analytical
Hot Take / Reactionary Opinion
Meme / Humor
Informational / News / Update

We evaluate two models:

Zero-shot baseline (Groq LLM prompting)
Fine-tuned DistilBERT classifier
Total examples: 201

Label distribution:
Informational / News / Update     93  
Meme / Humor                      41  
Hot Take / Reactionary Opinion    41  
Analytical                        26  

## 3. Baseline Model (Groq LLM)
Overall Performance
Accuracy: 0.871 (31/31 parseable responses)
Per-class Metrics
                                precision    recall  f1-score   support

Analytical                         1.00       0.75      0.86         4
Hot Take / Reactionary Opinion     0.78       1.00      0.88         7
Meme / Humor                       1.00       0.50      0.67         6
Informational / News / Update      0.88       1.00      0.93        14
Key Baseline Confusions

Before analyzing errors, we used an LLM-assisted review of misclassified predictions to surface patterns. The tool consistently highlighted:

Meme posts often being confused with Hot Takes due to similar emotional intensity and slang
Analytical posts misclassified as Hot Takes when evaluative language lacked explicit structure
Informational posts occasionally absorbing analytical/stat-heavy content
Short posts with low context being the most unstable across categories
Baseline Failure Modes

The baseline struggles most with:

Meme vs Hot Take boundary
Analytical vs Hot Take confusion
Occasional blending of Informational and Analytical content

The main hypothesis is that the model relies heavily on surface-level lexical cues and tone, rather than discourse intent or reasoning structure.
## 4. Fine-tuned Model (DistilBERT)
Overall Performance
Accuracy: 0.516 (17/31 correct)
Per-class Metrics
                                precision    recall  f1-score   support

Analytical                         0.00       0.00      0.00         4
Hot Take / Reactionary Opinion     0.38       0.71      0.50         7
Meme / Humor                       0.00       0.00      0.00         6
Informational / News / Update      0.61       0.79      0.69        14

Key Fine-tuned Model Confusions

The confusion matrix (text form):

True \ Predicted	Analytical	Hot Take	Meme	Informational
Analytical	0	3	0	1
Hot Take / Reactionary	0	5	0	2
Meme / Humor	0	3	0	3
Informational / News	0	3	0	11
Key Observation

The fine-tuned model collapsed heavily toward:

Hot Take
Informational

It failed to learn:

Meme structure entirely
Analytical reasoning patterns

## 5. Error Analysis (Fine-tuned Model)

Below are representative misclassified examples and analysis:

Example 1

Text: Sabonis elite passing big analysis continues
True: Analytical
Predicted: Informational

Issue: The word “analysis” appears but lacks structured reasoning, causing confusion with news-style summaries.

Example 2

Text: Hot take defense wins championships is outdated framing
True: Hot Take
Predicted: Informational

Issue: Contains explicit opinion framing but is misread as neutral reporting due to absence of emotional markers.
Example 3

Text: He got cooked clip goes viral again
True: Meme
Predicted: Hot Take

Issue: Informal slang (“cooked”) is interpreted as opinionated criticism rather than humor/meme context.

Example 4

Text: Franz Wagner efficiency leap analysis
True: Analytical
Predicted: Hot Take

Issue: Short phrase with statistical tone but no explicit reasoning structure → mistaken as evaluative opinion.

Example 5

Text: Giannis: We just need to be more physical after loss
True: Informational
Predicted: Hot Take

Issue: Quote-like structure triggers opinion classification even though it is factual reporting.

Example 6

Text: Every time I check box score, someone random has 40 points
True: Meme
Predicted: Hot Take

Issue: Generalized exaggeration interpreted as opinion instead of humorous commentary.

## 6. Sample Fine-tuned Predictions
Text	Predicted Label	Confidence	Notes
Sabonis elite passing big analysis continues	Informational	0.28	Reasonable due to stat-like phrasing
Hot take defense wins championships is outdated framing	Informational	0.27	Misread opinion framing as neutral update
He got cooked clip goes viral again	Hot Take	0.27	Slang misinterpreted as criticism
Franz Wagner efficiency leap analysis	Hot Take	0.28	“analysis” keyword dominated signal
Giannis: We just need to be more physical	Hot Take	0.27	Quote structure triggered opinion bias
Correct Example
Text	Predicted	Confidence	Why correct
Knicks continue strong defensive rating streak	Informational	0.31	Matches news-style reporting with metrics

## 7. Model Comparison
Model	Accuracy
Zero-shot baseline (Groq)	0.871
Fine-tuned DistilBERT	0.516

Regression after fine-tuning: -0.355

## 8. Key Findings & Interpretation
What the model captured well
Informational posts with clear “news-like” structure
Explicit mentions of games, clips, or updates (baseline especially)
What the model failed to capture
Meme vs Hot Take distinction (collapsed entirely in fine-tuned model)
Analytical reasoning structure (not just keywords like “analysis”)
Discourse intent (humor vs opinion vs reporting)
## 9. Spec Reflection
What the spec helped with

The label definitions forced a clear separation between:

opinion (Hot Take)
humor (Meme)
factual reporting (Informational)
reasoning (Analytical)

This helped structure annotation consistency and reduced ambiguity in labeling.

Where implementation diverged

In practice, the model:

Overweighted lexical cues (“analysis”, “clip”, “hot take”)
Failed to encode discourse intent
Collapsed overlapping semantic regions (especially Meme vs Hot Take)

This indicates that the dataset design is more separable for LLM prompting than for a small fine-tuned encoder model.

## 10. AI Usage Disclosure
Instance 1: Baseline debugging (prompt + parsing issue)
Prompted AI to diagnose why all outputs were unparseable
It identified .lower() normalization and substring matching as the issue
I modified matching logic accordingly
Instance 2: Error pattern analysis
Prompted AI to analyze misclassified examples
It identified confusion clusters:
Meme ↔ Hot Take
Analytical ↔ Hot Take
Informational ↔ Analytical overlap
I verified these patterns manually on sampled errors
## 11. Conclusion

The baseline LLM performs strongly due to rich semantic understanding and discourse sensitivity, while the fine-tuned DistilBERT model struggles due to limited capacity to encode nuanced intent differences between closely related classes. The dominant challenge in this task is not topic recognition, but stance and discourse framing separation, particularly between humor, opinion, and analytical reasoning.

Conclsuion
