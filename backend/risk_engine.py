def fuse_risk(acoustic_score: float, llm_score: float) -> float:
    """40% M2's acoustic synthetic-voice score + 60% M1's LLM scam-intent score."""
    acoustic_score = max(0.0, min(1.0, acoustic_score))
    llm_score = max(0.0, min(1.0, llm_score))
    return round(0.40 * acoustic_score + 0.60 * llm_score, 4)