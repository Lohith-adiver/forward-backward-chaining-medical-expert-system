# ──────────────────────────────────────────────────────────────
# KNOWLEDGE BASE — 100 diseases with 5-8 symptoms each
# Symptoms use lowercase, underscores for spaces.
# ──────────────────────────────────────────────────────────────

from collections import Counter

_RAW_KNOWLEDGE_BASE = {
    # ── Respiratory ───────────────────────────────────────────
    "common_cold": [
        "runny_nose", "sneezing", "sore_throat", "cough",
        "mild_fever", "headache", "congestion"
    ],
    "influenza": [
        "high_fever", "body_ache", "cough", "fatigue",
        "headache", "chills", "sore_throat"
    ],
    "covid_19": [
        "fever", "dry_cough", "fatigue", "loss_of_taste",
        "loss_of_smell", "breathing_difficulty", "body_ache"
    ],
    "pneumonia": [
        "high_fever", "cough", "chest_pain", "breathing_difficulty",
        "fatigue", "chills", "sweating"
    ],
    "tuberculosis": [
        "chronic_cough", "coughing_blood", "weight_loss", "night_sweats",
        "fever", "fatigue", "chest_pain"
    ],
    "bronchitis": [
        "cough", "mucus_production", "fatigue", "chest_discomfort",
        "shortness_of_breath", "mild_fever", "sore_throat"
    ],
    "asthma": [
        "wheezing", "shortness_of_breath", "chest_tightness",
        "cough", "breathing_difficulty", "fatigue"
    ],
    "sinusitis": [
        "facial_pain", "nasal_congestion", "headache", "runny_nose",
        "cough", "fatigue", "fever"
    ],
    "tonsillitis": [
        "sore_throat", "difficulty_swallowing", "fever", "swollen_tonsils",
        "headache", "neck_pain", "bad_breath"
    ],
    "laryngitis": [
        "hoarse_voice", "sore_throat", "dry_cough", "difficulty_speaking",
        "fever", "throat_irritation"
    ],
    "emphysema": [
        "shortness_of_breath", "chronic_cough", "wheezing",
        "fatigue", "weight_loss", "chest_tightness"
    ],
    "pleurisy": [
        "chest_pain", "cough", "fever", "shortness_of_breath",
        "sharp_chest_pain", "fatigue"
    ],
    "croup": [
        "barking_cough", "hoarse_voice", "fever", "breathing_difficulty",
        "stridor", "runny_nose"
    ],
    "whooping_cough": [
        "severe_cough", "vomiting_after_cough", "fever", "runny_nose",
        "fatigue", "breathing_difficulty"
    ],
    "lung_cancer": [
        "chronic_cough", "coughing_blood", "chest_pain", "weight_loss",
        "shortness_of_breath", "fatigue", "hoarse_voice"
    ],

    # ── Cardiovascular ────────────────────────────────────────
    "heart_attack": [
        "chest_pain", "sweating", "shortness_of_breath", "nausea",
        "arm_pain", "dizziness", "anxiety"
    ],
    "hypertension": [
        "headache", "dizziness", "blurred_vision", "chest_pain",
        "shortness_of_breath", "nosebleed"
    ],
    "hypotension": [
        "dizziness", "fainting", "weakness", "blurred_vision",
        "nausea", "fatigue", "cold_skin"
    ],
    "arrhythmia": [
        "palpitations", "dizziness", "chest_pain", "shortness_of_breath",
        "fainting", "fatigue"
    ],
    "coronary_artery_disease": [
        "chest_pain", "shortness_of_breath", "fatigue", "dizziness",
        "nausea", "sweating"
    ],
    "heart_failure": [
        "shortness_of_breath", "swelling_legs", "fatigue",
        "rapid_heartbeat", "persistent_cough", "weight_gain"
    ],
    "angina": [
        "chest_pain", "shortness_of_breath", "nausea", "sweating",
        "dizziness", "fatigue"
    ],
    "myocarditis": [
        "chest_pain", "fever", "fatigue", "shortness_of_breath",
        "rapid_heartbeat", "swelling_legs"
    ],
    "pericarditis": [
        "sharp_chest_pain", "fever", "weakness", "cough",
        "palpitations", "fatigue"
    ],
    "cardiomyopathy": [
        "fatigue", "swelling_legs", "shortness_of_breath",
        "dizziness", "palpitations", "bloating"
    ],
    "deep_vein_thrombosis": [
        "leg_swelling", "leg_pain", "redness", "warmth_in_leg",
        "skin_discoloration", "fatigue"
    ],
    "pulmonary_embolism": [
        "chest_pain", "shortness_of_breath", "coughing_blood",
        "rapid_heartbeat", "dizziness", "sweating"
    ],
    "stroke": [
        "sudden_numbness", "confusion", "speech_difficulty",
        "severe_headache", "vision_problems", "dizziness", "paralysis"
    ],
    "aortic_aneurysm": [
        "back_pain", "abdominal_pain", "dizziness", "nausea",
        "rapid_heartbeat", "shortness_of_breath"
    ],

    # ── Gastrointestinal ──────────────────────────────────────
    "gastritis": [
        "stomach_pain", "nausea", "bloating", "vomiting",
        "loss_of_appetite", "indigestion"
    ],
    "acid_reflux": [
        "heartburn", "chest_discomfort", "sore_throat", "difficulty_swallowing",
        "regurgitation", "bloating"
    ],
    "peptic_ulcer": [
        "stomach_burning", "nausea", "vomiting", "bloating",
        "loss_of_appetite", "weight_loss"
    ],
    "appendicitis": [
        "lower_right_abdominal_pain", "nausea", "vomiting", "fever",
        "loss_of_appetite", "bloating"
    ],
    "cholera": [
        "severe_diarrhea", "dehydration", "vomiting", "muscle_cramps",
        "low_blood_pressure", "rapid_heartbeat"
    ],
    "food_poisoning": [
        "vomiting", "diarrhea", "stomach_pain", "nausea",
        "fever", "weakness", "dehydration"
    ],
    "constipation": [
        "difficulty_passing_stool", "abdominal_pain", "bloating",
        "hard_stool", "straining", "loss_of_appetite"
    ],
    "irritable_bowel_syndrome": [
        "abdominal_cramps", "bloating", "diarrhea", "constipation",
        "gas", "mucus_in_stool"
    ],
    "pancreatitis": [
        "upper_abdominal_pain", "nausea", "vomiting", "fever",
        "rapid_heartbeat", "weight_loss"
    ],
    "gallstones": [
        "upper_right_abdominal_pain", "nausea", "vomiting",
        "jaundice", "fever", "indigestion"
    ],
    "hepatitis_a": [
        "jaundice", "fatigue", "nausea", "fever",
        "dark_urine", "loss_of_appetite", "abdominal_pain"
    ],
    "hepatitis_b": [
        "jaundice", "fatigue", "abdominal_pain", "nausea",
        "joint_pain", "dark_urine", "fever"
    ],
    "cirrhosis": [
        "jaundice", "fatigue", "swelling_legs", "bruising_easily",
        "weight_loss", "confusion", "abdominal_swelling"
    ],
    "celiac_disease": [
        "diarrhea", "bloating", "fatigue", "weight_loss",
        "abdominal_pain", "nausea", "skin_rash"
    ],
    "crohns_disease": [
        "abdominal_pain", "diarrhea", "fatigue", "weight_loss",
        "fever", "blood_in_stool", "mouth_sores"
    ],
    "ulcerative_colitis": [
        "bloody_diarrhea", "abdominal_pain", "urgency_to_defecate",
        "weight_loss", "fatigue", "fever"
    ],

    # ── Infectious / Tropical ─────────────────────────────────
    "malaria": [
        "high_fever", "chills", "sweating", "headache",
        "nausea", "body_ache", "fatigue"
    ],
    "dengue": [
        "high_fever", "severe_headache", "joint_pain", "muscle_pain",
        "skin_rash", "nausea", "fatigue"
    ],
    "typhoid": [
        "sustained_fever", "weakness", "stomach_pain", "headache",
        "loss_of_appetite", "diarrhea", "rash"
    ],
    "measles": [
        "high_fever", "cough", "runny_nose", "skin_rash",
        "red_eyes", "sensitivity_to_light", "white_spots_in_mouth"
    ],
    "chickenpox": [
        "itchy_rash", "blisters", "fever", "fatigue",
        "headache", "loss_of_appetite"
    ],
    "mumps": [
        "swollen_salivary_glands", "fever", "headache", "fatigue",
        "muscle_ache", "loss_of_appetite"
    ],
    "rubella": [
        "mild_fever", "skin_rash", "headache", "red_eyes",
        "swollen_lymph_nodes", "joint_pain"
    ],
    "tetanus": [
        "jaw_stiffness", "muscle_spasms", "fever", "sweating",
        "difficulty_swallowing", "rapid_heartbeat"
    ],
    "rabies": [
        "fever", "headache", "confusion", "agitation",
        "hydrophobia", "excessive_salivation", "paralysis"
    ],
    "ebola": [
        "high_fever", "severe_headache", "muscle_pain", "vomiting",
        "diarrhea", "internal_bleeding", "fatigue"
    ],
    "zika_virus": [
        "mild_fever", "skin_rash", "joint_pain", "red_eyes",
        "headache", "muscle_pain"
    ],
    "chikungunya": [
        "high_fever", "severe_joint_pain", "skin_rash", "headache",
        "muscle_pain", "fatigue"
    ],
    "yellow_fever": [
        "fever", "jaundice", "headache", "body_ache",
        "nausea", "vomiting", "fatigue"
    ],
    "meningitis": [
        "severe_headache", "fever", "neck_stiffness", "nausea",
        "sensitivity_to_light", "confusion", "skin_rash"
    ],
    "sepsis": [
        "high_fever", "rapid_heartbeat", "rapid_breathing", "confusion",
        "low_blood_pressure", "sweating", "chills"
    ],

    # ── Skin ──────────────────────────────────────────────────
    "eczema": [
        "itchy_skin", "dry_skin", "redness", "skin_rash",
        "cracked_skin", "swelling"
    ],
    "psoriasis": [
        "red_patches", "silvery_scales", "dry_skin", "itching",
        "burning_sensation", "thickened_nails"
    ],
    "fungal_infection": [
        "itching", "skin_rash", "redness", "peeling_skin",
        "ring_shaped_rash", "burning_sensation"
    ],
    "acne": [
        "pimples", "blackheads", "whiteheads", "oily_skin",
        "skin_redness", "scarring"
    ],
    "cellulitis": [
        "skin_redness", "swelling", "warmth", "pain",
        "fever", "blisters", "skin_tenderness"
    ],
    "scabies": [
        "intense_itching", "skin_rash", "tiny_blisters",
        "red_bumps", "itching_at_night"
    ],

    # ── Musculoskeletal ───────────────────────────────────────
    "arthritis": [
        "joint_pain", "joint_stiffness", "swelling", "redness",
        "decreased_range_of_motion", "fatigue"
    ],
    "osteoporosis": [
        "back_pain", "loss_of_height", "stooped_posture",
        "bone_fracture", "bone_pain"
    ],
    "gout": [
        "severe_joint_pain", "swelling", "redness", "warmth",
        "limited_mobility", "tenderness"
    ],
    "fibromyalgia": [
        "widespread_pain", "fatigue", "sleep_problems", "memory_problems",
        "headache", "depression", "abdominal_cramps"
    ],
    "herniated_disc": [
        "back_pain", "leg_pain", "numbness", "tingling",
        "muscle_weakness", "sciatica"
    ],

    # ── Neurological ──────────────────────────────────────────
    "migraine": [
        "severe_headache", "nausea", "sensitivity_to_light",
        "sensitivity_to_sound", "visual_disturbances", "vomiting"
    ],
    "epilepsy": [
        "seizures", "confusion", "staring_spell", "uncontrollable_jerking",
        "loss_of_consciousness", "anxiety"
    ],
    "parkinsons_disease": [
        "tremor", "slow_movement", "muscle_stiffness", "balance_problems",
        "speech_changes", "writing_changes"
    ],
    "alzheimers_disease": [
        "memory_loss", "confusion", "difficulty_speaking",
        "disorientation", "mood_changes", "poor_judgment"
    ],
    "multiple_sclerosis": [
        "numbness", "tingling", "vision_problems", "fatigue",
        "muscle_weakness", "balance_problems", "dizziness"
    ],
    "bells_palsy": [
        "facial_drooping", "difficulty_closing_eye", "drooling",
        "loss_of_taste", "ear_pain", "headache"
    ],

    # ── Endocrine / Metabolic ─────────────────────────────────
    "diabetes_type_1": [
        "frequent_urination", "excessive_thirst", "weight_loss",
        "fatigue", "blurred_vision", "hunger"
    ],
    "diabetes_type_2": [
        "frequent_urination", "excessive_thirst", "fatigue",
        "blurred_vision", "slow_healing_wounds", "tingling_hands_feet"
    ],
    "hyperthyroidism": [
        "weight_loss", "rapid_heartbeat", "anxiety", "tremor",
        "sweating", "heat_intolerance", "fatigue"
    ],
    "hypothyroidism": [
        "fatigue", "weight_gain", "cold_intolerance", "dry_skin",
        "constipation", "depression", "muscle_weakness"
    ],
    "cushings_syndrome": [
        "weight_gain", "round_face", "purple_stretch_marks",
        "high_blood_pressure", "fatigue", "muscle_weakness"
    ],

    # ── Urinary / Renal ───────────────────────────────────────
    "urinary_tract_infection": [
        "burning_urination", "frequent_urination", "pelvic_pain",
        "cloudy_urine", "strong_urine_odor", "fever"
    ],
    "kidney_stones": [
        "severe_side_pain", "blood_in_urine", "nausea", "vomiting",
        "frequent_urination", "burning_urination"
    ],
    "kidney_infection": [
        "fever", "back_pain", "nausea", "vomiting",
        "burning_urination", "frequent_urination", "chills"
    ],
    "chronic_kidney_disease": [
        "fatigue", "swelling_legs", "nausea", "shortness_of_breath",
        "decreased_urination", "confusion", "chest_pain"
    ],

    # ── Eyes / ENT ────────────────────────────────────────────
    "conjunctivitis": [
        "red_eyes", "itchy_eyes", "eye_discharge", "tearing",
        "sensitivity_to_light", "gritty_feeling"
    ],
    "glaucoma": [
        "eye_pain", "blurred_vision", "halos_around_lights",
        "headache", "nausea", "vision_loss"
    ],
    "ear_infection": [
        "ear_pain", "fever", "hearing_loss", "fluid_drainage",
        "difficulty_sleeping", "irritability"
    ],

    # ── Mental Health ─────────────────────────────────────────
    "depression": [
        "persistent_sadness", "loss_of_interest", "fatigue",
        "sleep_problems", "appetite_changes", "difficulty_concentrating",
        "feelings_of_worthlessness"
    ],
    "generalized_anxiety": [
        "excessive_worry", "restlessness", "fatigue", "difficulty_concentrating",
        "muscle_tension", "sleep_problems", "irritability"
    ],
    "panic_disorder": [
        "sudden_fear", "rapid_heartbeat", "sweating", "trembling",
        "shortness_of_breath", "chest_pain", "nausea"
    ],
    "insomnia": [
        "difficulty_falling_asleep", "waking_up_early", "fatigue",
        "irritability", "difficulty_concentrating", "daytime_sleepiness"
    ],

    # ── Blood / Immune ────────────────────────────────────────
    "anemia": [
        "fatigue", "pale_skin", "dizziness", "shortness_of_breath",
        "cold_hands_feet", "headache", "weakness"
    ],
    "leukemia": [
        "fatigue", "frequent_infections", "weight_loss", "easy_bruising",
        "nosebleed", "bone_pain", "sweating"
    ],
    "lymphoma": [
        "swollen_lymph_nodes", "fatigue", "fever", "night_sweats",
        "weight_loss", "itching", "shortness_of_breath"
    ],
    "hiv_aids": [
        "fever", "fatigue", "swollen_lymph_nodes", "weight_loss",
        "night_sweats", "skin_rash", "mouth_sores"
    ],
    "lupus": [
        "fatigue", "joint_pain", "skin_rash", "fever",
        "butterfly_rash", "sensitivity_to_light", "hair_loss"
    ],

    # ── Other ─────────────────────────────────────────────────
    "allergic_rhinitis": [
        "sneezing", "runny_nose", "itchy_eyes", "nasal_congestion",
        "watery_eyes", "postnasal_drip"
    ],
    "sleep_apnea": [
        "loud_snoring", "gasping_during_sleep", "daytime_sleepiness",
        "morning_headache", "difficulty_concentrating", "irritability"
    ],
    "vertigo": [
        "spinning_sensation", "dizziness", "nausea", "vomiting",
        "balance_problems", "hearing_loss"
    ],
    "heat_stroke": [
        "high_body_temperature", "confusion", "nausea", "rapid_heartbeat",
        "headache", "red_skin", "unconsciousness"
    ],
    "dehydration": [
        "excessive_thirst", "dry_mouth", "dark_urine", "fatigue",
        "dizziness", "decreased_urination", "headache"
    ],
}

KNOWLEDGE_BASE = {disease: set(symptoms) for disease, symptoms in _RAW_KNOWLEDGE_BASE.items()}

# ──────────────────────────────────────────────────────────────
# Symptom aliases — maps common user terms to canonical names
# ──────────────────────────────────────────────────────────────
SYMPTOM_ALIASES = {
    # Common shorthands
    "cold":              "runny_nose",
    "flu":               "high_fever",
    "temperature":       "fever",
    "high_temperature":  "high_fever",
    "tired":             "fatigue",
    "tiredness":         "fatigue",
    "exhaustion":        "fatigue",
    "body_pain":         "body_ache",
    "bodyache":          "body_ache",
    "breathlessness":    "shortness_of_breath",
    "breathing_problem": "breathing_difficulty",
    "stomach_ache":      "stomach_pain",
    "tummy_pain":        "stomach_pain",
    "belly_pain":        "abdominal_pain",
    "throwing_up":       "vomiting",
    "puking":            "vomiting",
    "loose_motions":     "diarrhea",
    "loose_stool":       "diarrhea",
    "running_nose":      "runny_nose",
    "stuffy_nose":       "nasal_congestion",
    "blocked_nose":      "nasal_congestion",
    "sore_eyes":         "red_eyes",
    "eye_redness":       "red_eyes",
    "tiredness":         "fatigue",
    "exhaustion":        "fatigue",
    "head_pain":         "headache",
    "head_ache":         "headache",
    "headache":          "headache",
    "migraine":          "severe_headache",
    "giddiness":         "dizziness",
    "lightheaded":       "dizziness",
    "stomachache":       "stomach_pain",
    "earache":           "ear_pain",
    "rash":              "skin_rash",
    "itch":              "itching",
    "scratching":        "itching",
    "puke":              "vomiting",
    "weight_decrease":   "weight_loss",
    "weight_increase":   "weight_gain",
    "peeing_often":      "frequent_urination",
    "painful_urination": "burning_urination",
    "yellow_skin":       "jaundice",
    "yellow_eyes":       "jaundice",
    "rapid_pulse":       "rapid_heartbeat",
    "fast_heartbeat":    "rapid_heartbeat",
    "heart_racing":      "rapid_heartbeat",
    "throat_pain":       "sore_throat",
    "back_ache":         "back_pain",
    "muscle_pain":       "body_ache",
    "joint_ache":        "joint_pain",
    "swelling":          "swelling_legs",
    "swollen_feet":      "swelling_legs",
    "coughing":          "cough",
    "dry_cough":         "dry_cough",
    "sneezing_a_lot":    "sneezing",
}

# ──────────────────────────────────────────────────────────────
# Build a master set of all known symptoms for validation
# ──────────────────────────────────────────────────────────────
ALL_SYMPTOMS = set()
for _symptoms in KNOWLEDGE_BASE.values():
    ALL_SYMPTOMS.update(_symptoms)

# ──────────────────────────────────────────────────────────────
# Additional knowledge structures for scalable reasoning
# ──────────────────────────────────────────────────────────────
SEVERITY_KEYWORDS = {
    "CRITICAL": {
        "chest_pain", "coughing_blood", "shortness_of_breath",
        "unconsciousness", "paralysis", "severe_headache",
        "confusion", "vision_problems", "breathing_difficulty"
    },
    "HIGH": {
        "high_fever", "rapid_heartbeat", "dizziness", "jaundice",
        "persistent_cough", "blood_in_stool", "dehydration",
        "vomiting_blood", "swelling_legs"
    },
    "MEDIUM": {
        "fever", "fatigue", "headache", "nausea", "vomiting",
        "diarrhea", "cough", "sore_throat", "weakness"
    },
    "LOW": {
        "sneezing", "runny_nose", "mild_fever", "itching",
        "watery_eyes", "congestion", "stuffy_nose"
    },
}


def infer_severity(symptoms):
    symptoms = set(symptoms)
    for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        if symptoms & SEVERITY_KEYWORDS[level]:
            return level
    return "MEDIUM"


KNOWLEDGE_BASE = {disease: set(symptoms) for disease, symptoms in _RAW_KNOWLEDGE_BASE.items()}

SYMPTOM_FREQUENCY = Counter(symptom for symptoms in KNOWLEDGE_BASE.values() for symptom in symptoms)
SYMPTOM_TO_DISEASES = {}
for disease, symptoms in KNOWLEDGE_BASE.items():
    for symptom in symptoms:
        SYMPTOM_TO_DISEASES.setdefault(symptom, []).append(disease)

# Distinctive symptoms are used to enforce knowledge-engineering rules.
# A disease will only be considered if the user has at least one of its core symptoms.
DISEASE_DISTINCTIVE = {
    "sinusitis": ["nasal_congestion", "facial_pain"],
    "pericarditis": ["sharp_chest_pain"],
    "pleurisy": ["chest_pain"],
    "asthma": ["wheezing"],
    "measles": ["skin_rash"],
}

# Priority weights help rank critical diseases higher in the final candidate list.
DISEASE_PRIORITY = {
    "heart_attack": 10,
    "pulmonary_embolism": 9,
    "angina": 8,
    "coronary_artery_disease": 7,
    "stroke": 9,
    "myocarditis": 6,
    "pericarditis": 5,
    "pneumonia": 5,
    "pulmonary_embolism": 9,
    "panic_disorder": 4,
}

DISEASE_RULES = {
    disease: {
        "symptoms": symptoms,
        "severity": infer_severity(symptoms),
        "total_symptoms": len(symptoms),
        "priority": DISEASE_PRIORITY.get(disease, 0),
        "frequency_score": sum(1 / SYMPTOM_FREQUENCY[symptom] for symptom in symptoms)
    }
    for disease, symptoms in KNOWLEDGE_BASE.items()
}
