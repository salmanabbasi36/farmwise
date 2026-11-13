# Architecture and design decisions

## Request flow

```
question
   |
   v
guardrails.check()  -- emergency / pesticide dose / out of scope / empty --> fixed safe message
   | pass
   v
BM25 retrieval over title + keywords + steps (top 3)
   |
   v
abstain test: score >= 2.0, coverage >= 0.30, and an informative
              word matches the entry's curated title or keywords
   | fail --> referral to extension officer
   | pass
   v
formatted answer: steps, caution, source, validation status, disclaimer
   |
   +--> optional: SMS shortening
```

## Mapping to the challenges in the report

| Challenge | Design response in this prototype |
|---|---|
| Power and connectivity | Runs offline; no model download; SMS-length output |
| Cost | No paid services needed; standard library only |
| Unsuitable models | Answers come from a local, editable knowledge base, not from a general model's memory |
| Language and skills | Keywords field holds farmers' own words; plain-language steps. Local languages are future work |
| Data governance | Query log stores question text and outcome only, no identifiers; logging can be switched off |
| Trust and scale | Every answer shows its source and that it is not yet validated; the system abstains when unsure; evaluation is reproducible |

## Why retrieval without a generative model

A generative model can produce fluent but wrong farming advice. For a prototype without agronomist oversight, returning curated text word for word is the safer design. Rephrasing answers in simpler words or other languages with a language model, constrained to the retrieved text, is left as future work.

## How the abstain rule was chosen

1. Questions were split into a dev set and a held-out test set before tuning.
2. A first version used a score threshold only. On the dev set it answered unrelated questions ("How do I grow tomatoes?") because incidental words in body text matched.
3. Raising the threshold fixed that but made the system refuse short, valid questions ("how do I store maize"). Short questions were then added to the dev set.
4. The final rule adds a curated-match requirement: at least one informative question word (inverse document frequency of 1.0 or more, which excludes "maize") must appear in the entry's title or keywords.
5. Two keyword lists were adjusted for dev-set ranking errors.
6. During step 2 a diagnostic printout also showed retrieval scores for the test split's out-of-scope questions. No threshold, rule or keyword was changed in response to test-split results, and the two test misses were left unfixed. Even so, the test split is not perfectly blind.

## Failure analysis (test split)

Both misses are abstentions, not wrong answers:

- "My neighbours already planted but I am not sure it is time yet, how do I decide?" Most words carry no topic signal, so coverage fell below 0.30.
- "No rain for two weeks and the maize is wilting." The best match was the weeding entry through the word "weeks"; the curated-match rule blocked that wrong answer and the system referred the farmer on. This shows the limit of keyword matching: "no rain" and "wilting" were not linked strongly enough to the drought entry.

Semantic retrieval with multilingual embeddings would likely help with both, at the cost of a model download and more compute.

## Next steps

1. Agronomist review of every entry; set `validated: true` per entry.
2. Local-language entries and voice input and output.
3. Collect real farmer questions (with consent) to replace the author-written evaluation sets.
4. Compare BM25 with a small multilingual embedding model on that data.
5. Calibrate the rainfall thresholds per region with historical data.
