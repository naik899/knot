"""Custom Hypothesis strategies for property-based testing."""

from hypothesis import strategies as st
from knot.models.patent import Patent, Claim, Classification
from datetime import date


def claim_strategy():
    return st.builds(
        Claim,
        number=st.integers(min_value=1, max_value=100),
        type=st.sampled_from(["independent", "dependent"]),
        text=st.text(min_size=10, max_size=200),
        depends_on=st.none(),
    )


def classification_strategy():
    return st.builds(
        Classification,
        code=st.from_regex(r"[A-H]\d{2}[A-Z]", fullmatch=True),
        description=st.text(min_size=5, max_size=100),
    )


def patent_strategy():
    return st.builds(
        Patent,
        id=st.from_regex(r"PAT\d{3}", fullmatch=True),
        title=st.text(min_size=10, max_size=200),
        abstract=st.text(min_size=20, max_size=500),
        claims=st.lists(claim_strategy(), min_size=1, max_size=5),
        assignees=st.lists(st.text(min_size=3, max_size=50), min_size=1, max_size=3),
        inventors=st.lists(st.text(min_size=3, max_size=50), min_size=1, max_size=3),
        filing_date=st.dates(min_value=date(2000, 1, 1), max_value=date(2025, 12, 31)),
        publication_date=st.dates(min_value=date(2000, 1, 1), max_value=date(2025, 12, 31)),
        classifications=st.lists(classification_strategy(), min_size=0, max_size=3),
        source=st.sampled_from(["USPTO", "EPO", "CGPDTM"]),
        status=st.sampled_from(["active", "expired", "pending"]),
        keywords=st.lists(st.from_regex(r"[a-z]{3,10}", fullmatch=True), min_size=1, max_size=10),
        jurisdictions=st.lists(st.sampled_from(["US", "EU", "IN"]), min_size=1, max_size=3),
    )
