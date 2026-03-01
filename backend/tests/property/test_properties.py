"""Property-based tests using Hypothesis."""

from hypothesis import given, settings, assume
from hypothesis import strategies as st
from knot.services.text_processing import normalize_text, extract_keywords
from knot.services.similarity import jaccard_similarity, keyword_similarity
from tests.property.strategies import patent_strategy


# Property 5: normalize_text is idempotent
@given(text=st.text(max_size=500))
@settings(max_examples=100)
def test_normalize_text_idempotent(text):
    once = normalize_text(text)
    twice = normalize_text(once)
    assert once == twice


# Property 12: Jaccard similarity is symmetric
@given(
    a=st.frozensets(st.text(min_size=1, max_size=10), min_size=0, max_size=20),
    b=st.frozensets(st.text(min_size=1, max_size=10), min_size=0, max_size=20),
)
@settings(max_examples=100)
def test_jaccard_symmetric(a, b):
    assert jaccard_similarity(set(a), set(b)) == jaccard_similarity(set(b), set(a))


# Property 13: Jaccard similarity is between 0 and 1
@given(
    a=st.frozensets(st.text(min_size=1, max_size=10), min_size=0, max_size=20),
    b=st.frozensets(st.text(min_size=1, max_size=10), min_size=0, max_size=20),
)
@settings(max_examples=100)
def test_jaccard_bounded(a, b):
    score = jaccard_similarity(set(a), set(b))
    assert 0.0 <= score <= 1.0


# Property 15: Identical sets have similarity 1.0
@given(s=st.frozensets(st.text(min_size=1, max_size=10), min_size=1, max_size=20))
@settings(max_examples=100)
def test_jaccard_identity(s):
    assert jaccard_similarity(set(s), set(s)) == 1.0


# Property 17: extract_keywords returns no duplicates
@given(text=st.text(min_size=10, max_size=500))
@settings(max_examples=100)
def test_extract_keywords_no_duplicates(text):
    keywords = extract_keywords(text)
    assert len(keywords) == len(set(keywords))


# Property 21: normalize_text returns lowercase
@given(text=st.text(min_size=1, max_size=500))
@settings(max_examples=100)
def test_normalize_text_lowercase(text):
    result = normalize_text(text)
    assert result == result.lower()


# Property 22: keyword_similarity is symmetric
@given(
    a=st.lists(st.from_regex(r"[a-z]{2,8}", fullmatch=True), min_size=0, max_size=10),
    b=st.lists(st.from_regex(r"[a-z]{2,8}", fullmatch=True), min_size=0, max_size=10),
)
@settings(max_examples=100)
def test_keyword_similarity_symmetric(a, b):
    assert keyword_similarity(a, b) == keyword_similarity(b, a)
