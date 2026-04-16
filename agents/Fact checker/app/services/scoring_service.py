import re
from app.config import TRUSTED_SOURCES, MISINFO_ENTITIES, VAGUE_PHRASES


def calculate_score(body: str, sources: list, entities: list):
    score = 100
    flagged_sources = []
    flagged_claims = []

    # --- Source Check ---
    for src in sources:
        if src not in TRUSTED_SOURCES:
            score -= 15
            flagged_sources.append(src)

    # --- Entity Check ---
    for ent in entities:
        if ent in MISINFO_ENTITIES:
            score -= 30

    # --- Sentence Analysis ---
    sentences = re.split(r'[.!?]', body)

    for sentence in sentences:
        sentence_lower = sentence.lower()

        # vague phrases
        for phrase in VAGUE_PHRASES:
            if phrase in sentence_lower:
                score -= 10
                flagged_claims.append(sentence.strip())

        # fake entities
        for ent in MISINFO_ENTITIES:
            if ent.lower() in sentence_lower:
                flagged_claims.append(sentence.strip())

    # --- Source Count Bonus ---
    if len(sources) >= 3:
        score += 5

    # Clamp score
    score = max(0, min(100, score))

    return score, list(set(flagged_claims)), flagged_sources


def get_verdict(score: int):
    if score >= 70:
        return "PASS"
    elif score >= 40:
        return "WARN"
    return "FAIL"