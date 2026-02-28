"""Tests for similarity service."""

from knot.services.similarity import (
    jaccard_similarity,
    keyword_similarity,
    claim_text_similarity,
    determine_risk_level,
)


class TestJaccardSimilarity:
    def test_identical_sets(self):
        s = {"a", "b", "c"}
        assert jaccard_similarity(s, s) == 1.0

    def test_disjoint_sets(self):
        assert jaccard_similarity({"a", "b"}, {"c", "d"}) == 0.0

    def test_partial_overlap(self):
        result = jaccard_similarity({"a", "b", "c"}, {"b", "c", "d"})
        assert 0.0 < result < 1.0
        # intersection={b,c}=2, union={a,b,c,d}=4, so 2/4=0.5
        assert result == 0.5

    def test_empty_sets(self):
        assert jaccard_similarity(set(), set()) == 0.0
        assert jaccard_similarity({"a"}, set()) == 0.0


class TestKeywordSimilarity:
    def test_same_keywords(self):
        assert keyword_similarity(["sensor", "iot"], ["sensor", "iot"]) == 1.0

    def test_case_insensitive(self):
        assert keyword_similarity(["Sensor"], ["sensor"]) == 1.0


class TestClaimTextSimilarity:
    def test_similar_texts(self):
        score, matched = claim_text_similarity(
            "A temperature sensor with wireless communication",
            "wireless temperature monitoring sensor device",
        )
        assert score > 0.0
        assert len(matched) > 0

    def test_unrelated_texts(self):
        score, matched = claim_text_similarity(
            "pharmaceutical compound synthesis",
            "automobile engine combustion",
        )
        assert score == 0.0


class TestDetermineRiskLevel:
    def test_high_risk(self):
        assert determine_risk_level(0.5) == "high"
        assert determine_risk_level(0.3) == "high"

    def test_medium_risk(self):
        assert determine_risk_level(0.2) == "medium"
        assert determine_risk_level(0.15) == "medium"

    def test_low_risk(self):
        assert determine_risk_level(0.1) == "low"
        assert determine_risk_level(0.0) == "low"
