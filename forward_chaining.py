"""
Forward Chaining — derive candidate diseases from user symptoms.

Improved strategy:
  - Compare user symptoms against every disease rule
  - Score candidates by percentage of matched requirements
  - Ignore very low-confidence matches
  - Return a capped top candidate list for presentation
"""

from typing import Set, List, Tuple
from knowledge_base import KNOWLEDGE_BASE, DISEASE_RULES, DISEASE_DISTINCTIVE

MIN_FORWARD_CONFIDENCE = 20.0
MAX_FORWARD_CANDIDATES = 8
FALLBACK_MIN_MATCH = 1


def score_match(matched: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round(matched / total * 100, 1)


def find_candidates(user_symptoms: Set[str], min_confidence: float = MIN_FORWARD_CONFIDENCE, top_n: int = MAX_FORWARD_CANDIDATES) -> List[Tuple[str, float, int, Set[str], int, str]]:
    """Return top candidate diseases ranked by forward match percentage."""
    strong_candidates = []
    fallback_candidates = []

    for disease, required_symptoms in KNOWLEDGE_BASE.items():
        distinctive = DISEASE_DISTINCTIVE.get(disease, [])
        if distinctive and not any(symptom in user_symptoms for symptom in distinctive):
            continue

        matched = required_symptoms & user_symptoms
        if len(matched) < FALLBACK_MIN_MATCH:
            continue

        confidence = score_match(len(matched), len(required_symptoms))
        priority = DISEASE_RULES.get(disease, {}).get("priority", 0)
        final_score = round(confidence + priority, 1)
        severity = DISEASE_RULES.get(disease, {}).get("severity", "MEDIUM")
        entry = (
            disease,
            confidence,
            final_score,
            priority,
            len(matched),
            matched,
            len(required_symptoms),
            severity,
        )

        if confidence >= min_confidence:
            strong_candidates.append(entry)
        else:
            fallback_candidates.append(entry)

    strong_candidates.sort(key=lambda item: (-item[2], -item[1], -item[4], item[0]))
    if strong_candidates:
        return strong_candidates[:top_n]

    fallback_candidates.sort(key=lambda item: (-item[2], -item[1], -item[4], item[0]))
    return fallback_candidates[:top_n]
