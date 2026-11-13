"""The Advisor: guardrails -> retrieval -> grounded, cited answer (or honest abstention)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from . import guardrails
from .retriever import BM25, tokenize

DEFAULT_KB = Path(__file__).parent / "data" / "knowledge_base.json"

# Abstain unless the best match (a) scores enough, (b) covers enough of the question, and
# (c) shares at least one informative word with the entry's curated title or keywords.
# Rule (c) stops incidental matches in body text ("cooking", "country") from producing answers.
# All three were chosen on the dev split of eval/ (see docs/ARCHITECTURE.md), not on the test split.
MIN_SCORE = 2.0
MIN_COVERAGE = 0.30
MIN_KEY_IDF = 1.0  # words rarer than this count as informative ("maize" does not)

REFERRAL = (
    "I do not have reliable advice on that in my maize guide. Please contact your "
    "local extension officer. If you can, take a photo or a sample of the affected plant with you."
)
DISCLAIMER = "General guidance only. Confirm with your local extension officer."


@dataclass
class Answer:
    text: str
    status: str  # "answer" | "abstain" | "refuse" | "emergency" | "out_of_scope" | "empty"
    doc_ids: list[str] = field(default_factory=list)
    confidence: float = 0.0
    validated: bool = False

    def to_dict(self) -> dict:
        return self.__dict__.copy()


class Advisor:
    def __init__(self, kb_path: str | Path | None = None, min_score: float = MIN_SCORE, min_coverage: float = MIN_COVERAGE):
        data = json.loads(Path(kb_path or DEFAULT_KB).read_text(encoding="utf-8"))
        self.meta = data["meta"]
        self.entries = data["entries"]
        self.min_score, self.min_coverage = min_score, min_coverage
        docs = [self._index_text(e) for e in self.entries]
        self.index = BM25(docs)
        self._curated = [set(tokenize(e["title"] + " " + e["keywords"])) for e in self.entries]

    def _has_key_match(self, question: str, entry_index: int) -> bool:
        idf = self.index.idf
        return any(
            t in self._curated[entry_index] and idf.get(t, 0.0) >= MIN_KEY_IDF for t in set(tokenize(question))
        )

    @staticmethod
    def _index_text(e: dict) -> str:
        # Title and keywords are repeated so they weigh more than body text.
        return " ".join([e["title"]] * 2 + [e["keywords"]] * 2 + e["steps"])

    def retrieve(self, question: str, top_k: int = 3):
        return [(self.entries[h.index], h) for h in self.index.search(question, top_k)]

    def ask(self, question: str) -> Answer:
        decision = guardrails.check(question)
        if decision.action != "pass":
            return Answer(decision.message, decision.action)

        hits = self.retrieve(question, top_k=3)
        if (
            not hits
            or hits[0][1].score < self.min_score
            or hits[0][1].coverage < self.min_coverage
            or not self._has_key_match(question, hits[0][1].index)
        ):
            return Answer(REFERRAL, "abstain", confidence=hits[0][1].score if hits else 0.0)

        entry, hit = hits[0]
        return Answer(
            self._format(entry),
            "answer",
            doc_ids=[e["id"] for e, _ in hits],
            confidence=round(hit.score, 2),
            validated=bool(entry.get("validated")),
        )

    @staticmethod
    def _format(e: dict) -> str:
        lines = [e["title"], ""]
        lines += [f"{i}. {s}" for i, s in enumerate(e["steps"], 1)]
        lines += ["", f"Note: {e['caution']}", f"Source: {e['source']}"]
        if not e.get("validated"):
            lines.append("Status: not yet validated by an agronomist.")
        lines.append(DISCLAIMER)
        return "\n".join(lines)

    @staticmethod
    def format_sms(answer: Answer, limit: int = 320) -> str:
        """Compact version for SMS or USSD-style channels."""
        if answer.status != "answer":
            return answer.text[:limit]
        body = answer.text.split("\n")
        title = body[0]
        steps = [l for l in body if l[:2] in {"1.", "2."}]
        text = f"{title}: " + " ".join(steps) + " Confirm with extension officer."
        return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."
