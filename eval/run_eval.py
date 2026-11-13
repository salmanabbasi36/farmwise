"""Evaluate retrieval accuracy and refusal behaviour.

Run from the project root:  python eval/run_eval.py
Optionally:                 python eval/run_eval.py --json results.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farmwise.advisor import Advisor  # noqa: E402


def evaluate(adv: Advisor, split: dict) -> dict:
    n_in = len(split["in_scope"])
    top1 = top3 = false_abstain = 0
    misses = []
    for item in split["in_scope"]:
        ans = adv.ask(item["q"])
        if ans.status != "answer":
            false_abstain += 1
            misses.append({"q": item["q"], "expected": item["id"], "got": ans.status})
            continue
        top1 += ans.doc_ids[0] == item["id"]
        top3 += item["id"] in ans.doc_ids
        if ans.doc_ids[0] != item["id"]:
            misses.append({"q": item["q"], "expected": item["id"], "got": ans.doc_ids[0]})

    n_out = len(split["out_of_scope"])
    handled = exact = 0
    bad = []
    for item in split["out_of_scope"]:
        ans = adv.ask(item["q"])
        handled += ans.status != "answer"  # did not hand out an answer it should not give
        exact += ans.status == item["expect"]
        if ans.status != item["expect"]:
            bad.append({"q": item["q"], "expected": item["expect"], "got": ans.status})

    return {
        "in_scope_n": n_in,
        "top1_accuracy": round(top1 / n_in, 3),
        "top3_accuracy": round(top3 / n_in, 3),
        "false_abstain_rate": round(false_abstain / n_in, 3),
        "out_of_scope_n": n_out,
        "correctly_not_answered": round(handled / n_out, 3),
        "exact_status_match": round(exact / n_out, 3),
        "in_scope_misses": misses,
        "out_of_scope_misses": bad,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write results to this file")
    args = ap.parse_args()

    adv = Advisor()
    results = {}
    for name in ("dev", "test"):
        split = json.loads((ROOT / "eval" / f"golden_{name}.json").read_text(encoding="utf-8"))
        results[name] = evaluate(adv, split)

    for name, r in results.items():
        print(f"\n=== {name.upper()} ===")
        for k, v in r.items():
            if not isinstance(v, list):
                print(f"{k:>26}: {v}")
        for m in r["in_scope_misses"]:
            print(f"  MISS in-scope  : {m}")
        for m in r["out_of_scope_misses"]:
            print(f"  MISS out-scope : {m}")
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
