# FarmWise: a maize advisory prototype for smallholder farmers in South Asia

Author: Khan Salman, Beijing Normal University (IEDE ID A20260058).

Research prototype for the Tsinghua University IEDE 2026 program, *The AI Economy: Innovation, Skills & Entrepreneurship* (Prof. Kris Singh).
Project: **AI for Smallholder Agriculture: Closing the Advisory, Data and Access Gap in Emerging Economies.**

FarmWise is Phase 1 of the framework proposed in the project report: a mobile-first advisory assistant that answers maize questions **only from a curated knowledge base**, cites its source, and refers the farmer to an extension officer when it does not know.

> **Status: prototype.** The knowledge base is a draft compiled by the author and has **not** been validated by an agronomist. It has not been tested with farmers. Do not use it for real farm decisions.

## What it does

| Feature | Why it matters for smallholders |
|---|---|
| Works fully offline, Python standard library only | Weak connectivity and power; no cloud cost |
| Answers only from curated entries, with source and validation status | Avoids invented advice |
| Abstains and refers to extension officer when unsure | A wrong answer costs a farmer more than no answer |
| Refuses pesticide doses; treats poisoning as an emergency | Safety |
| Short SMS-style answers (320 characters) | Basic phones |
| Optional 7-day rainfall planting signal (Open-Meteo, needs internet) | Planting timing |
| Query log without user identifiers | Feedback loop with minimal data collection |

## Quick start

Needs Python 3.10 or newer. Nothing to install.

```bash
python -m farmwise ask "worms are eating my maize leaves"
python -m farmwise ask "how do I store maize" --sms
python -m farmwise chat                 # terminal chat
python -m farmwise serve                # web chat at http://127.0.0.1:8000
python -m farmwise weather --lat 28.61 --lon 77.21   # New Delhi; needs internet
```

## Tests and evaluation

```bash
python -m unittest discover -s tests -v   # 19 tests
python eval/run_eval.py                   # prints dev and test results
```

Results of the last run are saved in `eval/results.json`. On the held-out test split (22 maize questions, 9 questions it should not answer):

| Metric | Test split |
|---|---|
| Top-1 retrieval accuracy | 90.9% (20 of 22) |
| Wrong answer given | 0 of 22 |
| Abstained when it could have answered | 9.1% (2 of 22) |
| Off-limits questions correctly not answered | 100% (9 of 9) |

Read these numbers with care. The questions were written by the author, who knows the knowledge base, and the sets are small. Real farmers' questions, in other languages and with spelling variation, will score lower.

## Project layout

```
farmwise/
  advisor.py      guardrails -> retrieval -> cited answer or abstention
  retriever.py    BM25 search (no dependencies)
  guardrails.py   pesticide dose refusal, poisoning emergency, scope limits
  weather.py      optional rainfall planting signal
  web.py          local web server and JSON API
  cli.py          command line
  static/         chat page
  data/knowledge_base.json   22 draft maize entries for South Asia (India, Pakistan, Bangladesh, Nepal)
eval/             dev and test question sets, runner, results
tests/            unit and API tests
docs/ARCHITECTURE.md
```

## Known limitations

- English only. Local-language and voice support are the most important next steps.
- Keyword retrieval matches words, not meaning. Unusual phrasing leads to abstention.
- The knowledge base needs agronomist validation and localisation by region.
- Weather thresholds are illustrative, not calibrated.

## Extending the knowledge base

Add an entry to `farmwise/data/knowledge_base.json` with `id`, `title`, `keywords` (the words farmers use), `steps`, `caution`, `source` and `validated`. Add matching questions to `eval/golden_dev.json`, then re-run the evaluation. Set `validated` to `true` only after an agronomist has signed the entry off.
