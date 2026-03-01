"""Tests for text processing service."""

from knot.services.text_processing import (
    normalize_text,
    extract_keywords,
    simulate_ocr,
    extract_claim_numbers,
    detect_language,
)


class TestNormalizeText:
    def test_basic_normalization(self):
        assert normalize_text("Hello  World!") == "hello world"

    def test_empty_string(self):
        assert normalize_text("") == ""

    def test_idempotent(self):
        text = "Some Complex!! Text   Here"
        once = normalize_text(text)
        twice = normalize_text(once)
        assert once == twice

    def test_special_characters(self):
        result = normalize_text("patent #12345 (US)")
        assert "patent" in result
        assert "12345" in result

    def test_preserves_hyphens(self):
        result = normalize_text("multi-sensor device")
        assert "multi-sensor" in result


class TestExtractKeywords:
    def test_filters_stop_words(self):
        keywords = extract_keywords("the method for comprising a system")
        assert "the" not in keywords
        assert "method" not in keywords
        assert "comprising" not in keywords

    def test_extracts_meaningful_words(self):
        keywords = extract_keywords("temperature sensor with wireless communication")
        assert "temperature" in keywords
        assert "sensor" in keywords
        assert "wireless" in keywords

    def test_respects_max_keywords(self):
        text = " ".join(f"word{i}" for i in range(50))
        keywords = extract_keywords(text, max_keywords=5)
        assert len(keywords) <= 5

    def test_no_duplicates(self):
        keywords = extract_keywords("sensor sensor sensor temperature temperature")
        assert len(keywords) == len(set(keywords))

    def test_empty_input(self):
        assert extract_keywords("") == []


class TestSimulateOCR:
    def test_returns_normalized_text(self):
        result = simulate_ocr("RAW OCR TEXT WITH   SPACES")
        assert result == normalize_text("RAW OCR TEXT WITH   SPACES")


class TestExtractClaimNumbers:
    def test_finds_claim_references(self):
        text = "The method of claim 1, further comprising claim 3"
        numbers = extract_claim_numbers(text)
        assert 1 in numbers
        assert 3 in numbers

    def test_no_claims(self):
        assert extract_claim_numbers("no references here") == []


class TestDetectLanguage:
    def test_english(self):
        assert detect_language("This is English text") == "en"

    def test_empty(self):
        assert detect_language("") == "en"
