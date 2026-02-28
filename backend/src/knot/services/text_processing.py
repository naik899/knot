"""Text normalization, keyword extraction, and OCR simulation."""

import re
import string


# Common patent/technical stop words
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "shall", "should", "may", "might", "can", "could", "that", "which",
    "who", "whom", "this", "these", "those", "it", "its", "not", "no",
    "nor", "as", "if", "then", "than", "so", "such", "said", "each",
    "every", "any", "all", "both", "few", "more", "most", "other",
    "some", "one", "two", "three", "first", "second", "third",
    "comprising", "comprises", "comprised", "wherein", "thereof",
    "therein", "thereto", "claim", "claims", "according", "includes",
    "including", "method", "system", "device", "apparatus", "means",
}


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, collapse whitespace, remove special chars.

    This function is idempotent - calling it multiple times produces the same result.
    """
    if not text:
        return ""
    # Lowercase
    result = text.lower()
    # Remove non-alphanumeric except spaces and hyphens
    result = re.sub(r"[^\w\s\-]", " ", result)
    # Collapse whitespace
    result = re.sub(r"\s+", " ", result)
    return result.strip()


def extract_keywords(text: str, max_keywords: int = 20) -> list[str]:
    """Extract meaningful keywords from text, filtering stop words."""
    normalized = normalize_text(text)
    words = normalized.split()
    # Filter stop words and short words
    keywords = []
    seen = set()
    for word in words:
        word_clean = word.strip("-")
        if (
            word_clean
            and word_clean not in STOP_WORDS
            and len(word_clean) > 2
            and word_clean not in seen
            and not word_clean.isdigit()
        ):
            seen.add(word_clean)
            keywords.append(word_clean)
    return keywords[:max_keywords]


def simulate_ocr(text: str) -> str:
    """Simulate OCR by adding realistic artifacts, then cleaning them.

    In a real system this would use Tesseract or AWS Textract.
    For the MVP, we simulate the normalization pipeline.
    """
    # Simulate: just normalize the text as if it came from OCR
    return normalize_text(text)


def extract_claim_numbers(text: str) -> list[int]:
    """Extract claim numbers referenced in text."""
    pattern = r"claim\s+(\d+)"
    matches = re.findall(pattern, text.lower())
    return [int(m) for m in matches]


def detect_language(text: str) -> str:
    """Simple language detection based on character frequency."""
    if not text:
        return "en"
    # Check for Devanagari (Hindi)
    devanagari = sum(1 for c in text if "\u0900" <= c <= "\u097F")
    if devanagari > len(text) * 0.1:
        return "hi"
    return "en"
