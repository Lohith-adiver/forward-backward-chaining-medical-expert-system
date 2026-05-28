"""
Backward Chaining — Goal-Driven Reasoning
==========================================
Given a hypothesis (candidate disease), backward chaining works by:
  1. Looking at what symptoms ARE REQUIRED to confirm the disease
  2. Checking which required symptoms the user ALREADY provided
  3. Asking the most informative missing symptoms first
  4. Confirming or rejecting the hypothesis based on a confidence threshold

This is the opposite of forward chaining:
  - Forward:  symptoms  → what diseases are possible?
  - Backward: disease   → do the symptoms confirm this disease?
"""

from typing import Set, Tuple
from knowledge_base import KNOWLEDGE_BASE, SYMPTOM_FREQUENCY

VERIFICATION_CONFIDENCE_THRESHOLD = 70.0


def _normalize_symptom(symptom: str) -> str:
    return symptom.replace("_", " ")


def _symptom_priority(symptom: str) -> Tuple[float, str]:
    frequency = SYMPTOM_FREQUENCY.get(symptom, 0)
    return (frequency, symptom)


def _ask_question(symptom: str) -> bool:
    prompt = f"    Do you have '{_normalize_symptom(symptom)}'? (y/n): "
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("    Please enter 'y' or 'n'.")


def _verify_symptom(symptom: str, user_symptoms: Set[str], evidence: dict, interactive: bool) -> bool:
    if symptom in user_symptoms or symptom in evidence["asked_yes"]:
        return True
    if symptom in evidence["asked_no"]:
        return False
    if not interactive:
        return False

    if _ask_question(symptom):
        evidence["asked_yes"].add(symptom)
        return True

    evidence["asked_no"].add(symptom)
    return False


def verify(disease: str, user_symptoms: Set[str], interactive: bool = True) -> Tuple[bool, float, dict]:
    required_symptoms = set(KNOWLEDGE_BASE.get(disease, []))
    if not required_symptoms:
        return False, 0.0, {}

    already_matched = required_symptoms & user_symptoms
    missing = required_symptoms - user_symptoms

    evidence = {
        "matched": already_matched,
        "asked_yes": set(),
        "asked_no": set()
    }

    if interactive and missing:
        disease_name = disease.replace("_", " ").title()
        print(f"\n  [Backward Chaining] Verifying hypothesis: '{disease_name}'")
        print("  I will ask the most distinctive missing symptoms first:\n")

        confirmed_symptoms = set(already_matched)
        ordered_missing = sorted(missing, key=_symptom_priority)
        total_required = len(required_symptoms)

        for index, symptom in enumerate(ordered_missing):
            current_confidence = round(len(confirmed_symptoms) / total_required * 100, 1)
            remaining = len(ordered_missing) - index
            max_possible = len(confirmed_symptoms) + remaining
            max_confidence = round(max_possible / total_required * 100, 1)

            if current_confidence >= VERIFICATION_CONFIDENCE_THRESHOLD:
                break
            if max_confidence < VERIFICATION_CONFIDENCE_THRESHOLD:
                break

            if _verify_symptom(symptom, user_symptoms, evidence, interactive):
                confirmed_symptoms.add(symptom)

        confirmed_symptoms = set(already_matched) | evidence["asked_yes"]
    else:
        confirmed_symptoms = set(already_matched)

    confidence = round(len(confirmed_symptoms) / len(required_symptoms) * 100, 1)
    confirmed = confidence >= VERIFICATION_CONFIDENCE_THRESHOLD

    return confirmed, confidence, evidence


def verify_silent(disease: str, user_symptoms: Set[str]) -> Tuple[bool, float]:
    required_symptoms = set(KNOWLEDGE_BASE.get(disease, []))
    if not required_symptoms:
        return False, 0.0

    matched = required_symptoms & user_symptoms
    confidence = round(len(matched) / len(required_symptoms) * 100, 1)
    confirmed = confidence >= VERIFICATION_CONFIDENCE_THRESHOLD
    return confirmed, confidence
