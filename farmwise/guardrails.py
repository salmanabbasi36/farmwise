"""Safety rules applied BEFORE retrieval.

Three jobs:
1. Pesticide poisoning is an emergency: tell the user to get medical help now.
2. Never give pesticide doses or mixing rates. Those must come from the label or
   an extension officer. (Fertilizer rate questions are NOT blocked here; the
   knowledge base answers them by pointing to soil tests.)
3. Politely redirect topics outside the demo scope (livestock, human health,
   loans, live prices) instead of guessing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Decision:
    action: str  # "pass" | "refuse" | "emergency" | "out_of_scope" | "empty"
    message: str = ""


_PESTICIDE = r"\b(pesticide\w*|insecticide\w*|herbicide\w*|fungicide\w*|chemical\w*|spray\w*|pyrethroid\w*|cypermethrin|glyphosate)\b"
_DOSE = r"\b(dose|dosage|how much|how many|ml|millilit\w*|litre\w*|liter\w*|gram\w*|mix|mixing|ratio|concentration|per knapsack|per tank|per hectare|per acre)\b"
_POISONING = r"\b(swallow\w*|drank|drink\w*|ate|inhal\w*|breath\w*|splash\w*|spill\w*|fell sick|feel\w* sick|dizz\w*|vomit\w*|poison\w*)\b"

_OUT_OF_SCOPE = [
    (r"\b(cow|cows|cattle|goat|goats|sheep|chicken|chickens|poultry|pig|pigs|livestock|dairy)\b", "livestock"),
    (r"\b(fever|malaria|medicine|medication|cough|pregnan|my child|my baby|hospital|disease in humans)\b", "human health"),
    (r"\b(loan|credit|interest rate|mortgage|bank account|insurance claim)\b", "finance"),
    (r"\b(price today|current price|market price|prices today|how much is maize selling|selling price)\b", "live market prices"),
]

EMERGENCY_MESSAGE = (
    "This may be a poisoning emergency. Stop spraying, move the person to fresh air, "
    "remove contaminated clothing, rinse skin or eyes with clean water, and get to a "
    "health facility or call your local emergency or poison-control number NOW. "
    "Take the pesticide container or label with you. Do not induce vomiting unless a medical worker tells you to."
)

DOSE_MESSAGE = (
    "I cannot give pesticide doses or mixing rates. A wrong dose can harm people and crops. "
    "The correct amount is printed on the product label for that pest and crop, or your "
    "extension officer or a registered agro-dealer can tell you. Use only products registered "
    "for maize, and wear protective clothing."
)


def check(question: str) -> Decision:
    q = (question or "").strip().lower()
    if len(q) < 3:
        return Decision("empty", "Please type your question about maize, for example: 'worms are eating my maize leaves'.")

    if re.search(_PESTICIDE, q) and re.search(_POISONING, q):
        return Decision("emergency", EMERGENCY_MESSAGE)

    if re.search(_PESTICIDE, q) and re.search(_DOSE, q):
        return Decision("refuse", DOSE_MESSAGE)

    for pattern, topic in _OUT_OF_SCOPE:
        if re.search(pattern, q):
            return Decision(
                "out_of_scope",
                f"This demo only covers maize growing and storage, so I cannot help with {topic}. "
                "Please ask your extension officer, cooperative or a qualified professional.",
            )
    return Decision("pass")
