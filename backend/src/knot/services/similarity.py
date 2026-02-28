"""Jaccard similarity scoring and claim matching."""


def jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    """Compute Jaccard similarity between two sets of keywords."""
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def keyword_similarity(keywords_a: list[str], keywords_b: list[str]) -> float:
    """Compute similarity between two keyword lists."""
    set_a = set(k.lower() for k in keywords_a)
    set_b = set(k.lower() for k in keywords_b)
    return jaccard_similarity(set_a, set_b)


def claim_text_similarity(claim_text: str, description: str) -> tuple[float, list[str]]:
    """Compare a patent claim against a product/technology description.

    Returns (similarity_score, matched_keywords).
    """
    from knot.services.text_processing import extract_keywords

    claim_keywords = set(extract_keywords(claim_text))
    desc_keywords = set(extract_keywords(description))

    matched = claim_keywords & desc_keywords
    score = jaccard_similarity(claim_keywords, desc_keywords)

    return score, sorted(matched)


def determine_risk_level(similarity_score: float) -> str:
    """Convert a similarity score to a risk level."""
    if similarity_score >= 0.3:
        return "high"
    elif similarity_score >= 0.15:
        return "medium"
    else:
        return "low"
