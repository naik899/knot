"""Tests for in-memory stores."""

from datetime import date
from knot.stores.patent_store import PatentStore
from knot.stores.graph_store import GraphStore
from knot.stores.search_store import SearchStore
from knot.models.patent import Patent, Claim, Classification, Inventor
from knot.models.product import ProductInfo
from knot.models.company import Company, OwnershipEdge


def _make_patent(**overrides):
    defaults = dict(
        id="TEST001",
        title="Test Patent",
        abstract="A test patent abstract",
        claims=[Claim(number=1, type="independent", text="A test claim")],
        assignees=["Test Corp"],
        inventors=[Inventor(name="Test Inventor", country="US")],
        filing_date=date(2020, 1, 1),
        publication_date=date(2020, 6, 1),
        classifications=[Classification(system="IPC", code="H04W", description="Wireless")],
        source="USPTO",
        publication_number="US12345678",
        status="active",
        keywords=["test", "patent"],
        jurisdictions=["US"],
    )
    defaults.update(overrides)
    return Patent(**defaults)


class TestPatentStore:
    def test_add_and_get(self):
        store = PatentStore()
        patent = _make_patent()
        store.add(patent)
        assert store.get("TEST001") is not None
        assert store.get("TEST001").title == "Test Patent"

    def test_count(self):
        store = PatentStore()
        assert store.count() == 0

    def test_search(self):
        store = PatentStore()
        patent = _make_patent(
            id="TEST001",
            title="Temperature Sensor Patent",
            abstract="A temperature sensor",
            keywords=["temperature", "sensor"],
        )
        store.add(patent)
        results = store.search("temperature")
        assert len(results) >= 1

    def test_get_nonexistent(self):
        store = PatentStore()
        assert store.get("NONEXISTENT") is None


class TestGraphStore:
    def test_add_and_get_company(self):
        store = GraphStore()
        company = Company(
            id="C001",
            canonical_name="Test Corp",
            aliases=["Test"],
            company_type="corporation",
            jurisdiction="US",
            subsidiaries=[],
        )
        store.add_company(company)
        assert store.get_company("C001") is not None

    def test_find_by_name(self):
        store = GraphStore()
        company = Company(
            id="C001",
            canonical_name="Test Corp",
            aliases=["TestCo"],
            company_type="corporation",
            jurisdiction="US",
            subsidiaries=[],
        )
        store.add_company(company)
        found = store.find_company_by_name("TestCo")
        assert found is not None
        assert found.id == "C001"

    def test_ownership_edges(self):
        store = GraphStore()
        edge = OwnershipEdge(
            from_company_id="C001",
            to_company_id="C002",
            ownership_percentage=100.0,
            effective_date=date(2020, 1, 1),
            source="SEC",
        )
        store.add_edge(edge)
        parent_edges = store.get_parent_edges("C002")
        assert len(parent_edges) == 1
        assert parent_edges[0].from_company_id == "C001"


class TestSearchStore:
    def test_add_and_get_products(self):
        store = SearchStore()
        product = ProductInfo(
            id="P001",
            name="Test Product",
            manufacturer="Test Corp",
            description="A test product",
        )
        store.add_product(product)
        products = store.get_all_products()
        assert len(products) == 1
