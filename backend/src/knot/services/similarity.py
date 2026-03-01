"""Similarity scoring: Jaccard (rule-based) and cosine (embedding-based)."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from knot.services.llm_service import LLMService


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


# ------------------------------------------------------------------
# Embedding-based similarity (requires Azure OpenAI)
# ------------------------------------------------------------------

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def semantic_similarity(text_a: str, text_b: str, llm_service: "LLMService") -> float:
    """Compute cosine similarity using Azure OpenAI embeddings.

    Returns 0.0 if embeddings are unavailable.
    """
    embeddings = llm_service.embed([text_a, text_b])
    if embeddings is None or len(embeddings) < 2:
        return 0.0
    return cosine_similarity(embeddings[0], embeddings[1])
