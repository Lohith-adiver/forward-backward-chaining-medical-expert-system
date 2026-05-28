#!/usr/bin/env python

import sys
from utils import parse_input, pretty_print, section_header, color_text, format_symptom_list
from forward_chaining import find_candidates
from backward_chaining import verify, verify_silent


def format_disease_name(name: str) -> str:
    return name.replace("_", " ").title()


def prompt_yes_no(message: str) -> bool:
    while True:
        choice = input(message).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def show_forward_candidates(user_symptoms, candidates):
    section_header("Forward Chaining — Candidate Generation")
    if not candidates:
        print(color_text("  No strong forward candidates could be generated from the symptoms provided.", "red"))
        return

    for rank, (disease, confidence, final_score, priority, matched_count, matched_set, total_syms, severity) in enumerate(candidates, 1):
        print(color_text(f"  {rank}. {format_disease_name(disease)} [{severity}]", "bold"))
        print(f"      Matched: {format_symptom_list(matched_set)}")
        print(f"      Coverage: {matched_count}/{total_syms} symptoms ({confidence}%)")
        if priority:
            print(f"      Priority bonus: {priority}  → Final score: {final_score}%")
        print()

    if candidates[0][1] < 40:
        print(color_text("  Note: The candidate list is based on low symptom coverage. Add more symptoms for better accuracy.", "yellow"))
    else:
        top_name = format_disease_name(candidates[0][0])
        print(color_text(f"  Most likely candidate: {top_name}", "cyan"))


def show_candidate_overview(candidates, top_n=4):
    section_header("Top Likely Diseases (Not Confirmed)")
    if not candidates:
        print(color_text("  No candidates to summarize.", "red"))
        return

    for rank, (disease, confidence, final_score, priority, matched_count, matched_set, total_syms, severity) in enumerate(candidates[:top_n], 1):
        print(color_text(f"  {rank}. {format_disease_name(disease)} [{severity}]", "bold"))
        print(f"      Confidence: {confidence}%")
        if priority:
            print(f"      Priority bonus: {priority}  → Final score: {final_score}%")
        print(f"      Matched: {format_symptom_list(matched_set)}\n")


def show_backward_summary(user_symptoms, candidates):
    section_header("Backward Chaining — Silent Verification")
    if not candidates:
        print(color_text("  No candidates available for backward chaining.", "red"))
        return []

    summary = []
    for disease, _, final_score, priority, _, matched_set, total_symptoms, severity in candidates:
        confirmed, confidence = verify_silent(disease, user_symptoms)
        summary.append((disease, confidence, final_score, priority, matched_set, total_symptoms, severity, confirmed))

    summary.sort(key=lambda item: (-item[2], -item[1], item[0]))

    for rank, (disease, confidence, final_score, priority, matched_set, total_symptoms, severity, confirmed) in enumerate(summary, 1):
        status = color_text("CONFIRMED", "green") if confirmed else color_text("PENDING", "yellow")
        print(color_text(f"  {rank}. {format_disease_name(disease)} [{severity}]", "bold"))
        print(f"      Backward confidence: {confidence}%")
        if priority:
            print(f"      Priority bonus: {priority}  → Final score: {final_score}%")
        print(f"      Status: {status}")
        print(f"      Known symptoms: {format_symptom_list(matched_set)}\n")

    return [
        (disease, confidence, final_score, priority, matched_set, total_symptoms, severity)
        for disease, confidence, final_score, priority, matched_set, total_symptoms, severity, confirmed in summary
        if confirmed
    ]


def interactive_backward_verify(user_symptoms, candidates):
    section_header("Backward Chaining — Interactive Verification")
    if not candidates:
        print(color_text("  No candidates available for interactive backward chaining.", "red"))
        return []

    confirmed_results = []
    for disease, _, final_score, priority, _, _, total_syms, severity in candidates[:3]:
        confirmed, confidence, evidence = verify(disease, user_symptoms, interactive=True)
        print(color_text(f"\n  Hypothesis: {format_disease_name(disease)}", "bold"))
        print(f"    Confirmed: {'Yes' if confirmed else 'No'}")
        print(f"    Confidence: {confidence}%")
        print(f"    Already matched: {format_symptom_list(evidence['matched']) or 'None'}")
        print(f"    Additional yes answers: {format_symptom_list(evidence['asked_yes']) or 'None'}")
        print(f"    Additional no answers: {format_symptom_list(evidence['asked_no']) or 'None'}")

        if confirmed:
            matched_symptoms = evidence['matched'] | evidence['asked_yes']
            confirmed_results.append((disease, confidence, final_score, priority, matched_symptoms, total_syms, severity))

    return confirmed_results


def main():
    section_header("AI MEDICAL EXPERT SYSTEM")
    user_input = input("Enter symptoms separated by commas: ")
    user_symptoms = parse_input(user_input)
    if not user_symptoms:
        print(color_text("No symptoms entered. Exiting.", "red"))
        sys.exit(0)

    candidates = find_candidates(user_symptoms)
    show_forward_candidates(user_symptoms, candidates)

    silent_confirmed_results = show_backward_summary(user_symptoms, candidates)

    interactive_confirmed_results = []
    if candidates and prompt_yes_no("\nWould you like to demonstrate interactive backward chaining for the top candidates? (y/n): "):
        interactive_confirmed_results = interactive_backward_verify(user_symptoms, candidates)

    if interactive_confirmed_results:
        section_header("Final Confirmed Diagnoses")
        pretty_print(interactive_confirmed_results, user_symptoms, title="Most Likely Disease")
    elif silent_confirmed_results:
        section_header("Final Confirmed Diagnoses")
        pretty_print(silent_confirmed_results, user_symptoms, title="Most Likely Disease")
    else:
        print(color_text("\nNo disease reached the confirmation threshold after backward chaining.", "yellow"))
        show_candidate_overview(candidates)


if __name__ == "__main__":
    main()
