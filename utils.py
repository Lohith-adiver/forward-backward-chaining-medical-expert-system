"""
Utility functions for the Medical Expert System.
- Input parsing with alias resolution
- Confidence scoring
- Clean terminal formatting
"""

from typing import Iterable
from knowledge_base import SYMPTOM_ALIASES, ALL_SYMPTOMS

COLOR_CODES = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "reset": "\033[0m",
}

DISPLAY_SYMPTOM_NAMES = {
    "shortness_of_breath": "Shortness of Breath",
    "chest_pain": "Chest Pain",
    "high_fever": "High Fever",
    "low_blood_pressure": "Low Blood Pressure",
    "rapid_heartbeat": "Rapid Heartbeat",
    "breathing_difficulty": "Breathing Difficulty",
    "runny_nose": "Runny Nose",
    "sore_throat": "Sore Throat",
    "loss_of_taste": "Loss of Taste",
    "loss_of_smell": "Loss of Smell",
    "body_ache": "Body Ache",
    "skin_rash": "Skin Rash",
    "joint_pain": "Joint Pain",
    "muscle_pain": "Muscle Pain",
    "mild_fever": "Mild Fever",
    "high_body_temperature": "High Body Temperature",
}


def color_text(text: str, color: str) -> str:
    code = COLOR_CODES.get(color, "")
    reset = COLOR_CODES["reset"]
    return f"{code}{text}{reset}" if code else text


def section_header(title: str, width: int = 68) -> None:
    print(color_text("\n" + "=" * width, "bold"))
    print(color_text(f"  {title}", "bold"))
    print(color_text("=" * width, "bold"))


def parse_input(text: str) -> set:
    """Parse comma-separated symptom string into a set of canonical symptom names."""
    raw = {s.strip().lower().replace(" ", "_") for s in text.split(",") if s.strip()}
    resolved = set()
    for sym in raw:
        canonical = SYMPTOM_ALIASES.get(sym, sym)
        resolved.add(canonical)
    return resolved


def format_symptom_name(symptom: str) -> str:
    return DISPLAY_SYMPTOM_NAMES.get(symptom, symptom.replace("_", " ").title())


def format_symptom_list(symptoms: Iterable[str]) -> str:
    return ", ".join(sorted(format_symptom_name(symptom) for symptom in symptoms))


def suggest_symptoms(partial: str) -> list:
    partial = partial.strip().lower().replace(" ", "_")
    return sorted([s for s in ALL_SYMPTOMS if partial in s])


def score(matches: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round(matches / total * 100, 1)


def pretty_print(results, user_symptoms, title: str = "DIAGNOSIS RESULTS"):
    if not results:
        print(color_text("\n  No matching diseases found for your symptoms.", "red"))
        return

    section_header(title)
    print(color_text(f"  Your symptoms: {format_symptom_list(user_symptoms)}\n", "dim"))

    for rank, item in enumerate(results, 1):
        if len(item) == 8:
            disease, confidence, _, priority, matched, _, total_syms, severity = item
        elif len(item) == 7:
            disease, confidence, _, priority, matched, total_syms, severity = item
        elif len(item) == 6:
            disease, confidence, matched, total_syms, severity = item
            priority = 0
        else:
            disease, confidence, matched, total_syms = item
            severity = None
            priority = 0

        if confidence >= 70:
            colour = "green"
            bar_char = "█"
        elif confidence >= 40:
            colour = "yellow"
            bar_char = "▓"
        else:
            colour = "red"
            bar_char = "░"

        filled = int(confidence / 100 * 20)
        bar = bar_char * filled + "·" * (20 - filled)
        name = disease.replace("_", " ").title()

        severity_label = f" [{severity}]" if severity else ""
        priority_label = f"  (Priority: {priority})" if priority else ""
        print(color_text(f"  {rank:>2}. {name}{severity_label}", "bold"))
        print(color_text(f"      [{bar}] {confidence}%", colour) + f"  ({len(matched)}/{total_syms} symptoms matched){priority_label}")
        print(color_text(f"      Matched: {format_symptom_list(matched)}", "cyan"))
        print()

    print(color_text("=" * 68, "bold"))
    print(color_text("  Disclaimer: This is for educational purposes only. Always consult a medical professional.", "dim"))
    print(color_text("=" * 68, "bold"))
