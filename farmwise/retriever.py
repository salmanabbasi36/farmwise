"""BM25 retrieval over the knowledge base, using only the standard library.

Why BM25 and not embeddings: it runs offline on a cheap laptop or phone-class
device, needs no model download, and is easy to explain and audit. The trade-off
is that it matches words, not meaning, so the knowledge base carries a
`keywords` field with the words farmers actually use.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

STOPWORDS = frozenset(
    """a an the is are was were be been of to in on at for and or but with by from my i we you
    it this that these those do does did how what when why where which can should would could
    about as if so not no me our your their his her its into than then there here have has had
    will just very also any some more most""".split()
)

_TOKEN = re.compile(r"[a-z0-9]+")


def stem(word: str) -> str:
    """Very light suffix stripping (worms -> worm, yellowing -> yellow)."""
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def tokenize(text: str) -> list[str]:
    return [stem(t) for t in _TOKEN.findall(text.lower()) if t not in STOPWORDS]


@dataclass
class Hit:
    index: int
    score: float
    coverage: float  # share of distinct query terms found in the document


class BM25:
    def __init__(self, documents: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tokens = [tokenize(d) for d in documents]
        self.tf = [Counter(t) for t in self.tokens]
        self.lengths = [len(t) for t in self.tokens]
        self.avg_len = (sum(self.lengths) / len(self.lengths)) if self.lengths else 0.0
        df: Counter = Counter()
        for tf in self.tf:
            df.update(tf.keys())
        n = len(documents)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def search(self, query: str, top_k: int = 3) -> list[Hit]:
        q_terms = tokenize(query)
        unique = set(q_terms)
        if not unique:
            return []
        hits = []
        for i, tf in enumerate(self.tf):
            score = 0.0
            for t in q_terms:
                f = tf.get(t, 0)
                if not f:
                    continue
                denom = f + self.k1 * (1 - self.b + self.b * self.lengths[i] / (self.avg_len or 1))
                score += self.idf.get(t, 0.0) * f * (self.k1 + 1) / denom
            if score > 0:
                coverage = sum(1 for t in unique if t in tf) / len(unique)
                hits.append(Hit(i, score, coverage))
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:top_k]
