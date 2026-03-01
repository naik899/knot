"""Load all mock data into stores at startup."""

import json
from pathlib import Path
from datetime import date

from knot.models.patent import Patent, Claim, Classification, Inventor
from knot.models.company import Company, OwnershipEdge
from knot.models.product import ProductInfo
from knot.models.validity import PriorArtCandidate
from knot.stores.patent_store import PatentStore
from knot.stores.graph_store import GraphStore
from knot.stores.search_store import SearchStore

MOCK_DATA_DIR = Path(__file__).parent


def _parse_date(d: str | None) -> date | None:
    if d is None:
        return None
    return date.fromisoformat(d)


def load_patents(store: PatentStore) -> None:
    with open(MOCK_DATA_DIR / "patents.json") as f:
        data = json.load(f)
    for p in data:
        patent = Patent(
            id=p["id"],
            source=p["source"],
            publication_number=p["publication_number"],
            title=p["title"],
            abstract=p["abstract"],
            claims=[Claim(**c) for c in p["claims"]],
            assignees=p["assignees"],
            inventors=[Inventor(**i) for i in p["inventors"]],
            filing_date=_parse_date(p.get("filing_date")),
            publication_date=_parse_date(p.get("publication_date")),
            expiry_date=_parse_date(p.get("expiry_date")),
            classifications=[Classification(**c) for c in p["classifications"]],
            keywords=p["keywords"],
            status=p["status"],
            jurisdictions=p["jurisdictions"],
        )
        store.add(patent)


def load_companies(store: GraphStore) -> None:
    with open(MOCK_DATA_DIR / "companies.json") as f:
        data = json.load(f)
    for c in data:
        company = Company(**c)
        store.add_company(company)
    # Build ownership edges from the data
    for c in data:
        if c.get("ultimate_parent_id"):
            # Find direct parent by walking the tree
            _add_ownership_edges(store, c, data)


def _add_ownership_edges(store: GraphStore, company_data: dict, all_companies: list[dict]) -> None:
    """Add ownership edges. If ultimate_parent_id is set, create edge from parent to this company."""
    child_id = company_data["id"]
    parent_id = company_data.get("ultimate_parent_id")
    if not parent_id:
        return
    # Check if this child is a direct subsidiary of the parent
    parent_data = next((c for c in all_companies if c["id"] == parent_id), None)
    if parent_data and child_id in parent_data.get("subsidiaries", []):
        edge = OwnershipEdge(
            from_company_id=parent_id,
            to_company_id=child_id,
            ownership_percentage=100.0,
            effective_date=date(2015, 1, 1),
            source="SEC Filing",
        )
        store.add_edge(edge)
    else:
        # Find intermediate parent
        for c in all_companies:
            if child_id in c.get("subsidiaries", []):
                edge = OwnershipEdge(
                    from_company_id=c["id"],
                    to_company_id=child_id,
                    ownership_percentage=100.0,
                    effective_date=date(2018, 6, 1),
                    source="Corporate Filing",
                )
                store.add_edge(edge)
                break


def load_products(store: SearchStore) -> None:
    with open(MOCK_DATA_DIR / "products.json") as f:
        data = json.load(f)
    for p in data:
        product = ProductInfo(**p)
        store.add_product(product)


def load_prior_art(store: SearchStore) -> None:
    with open(MOCK_DATA_DIR / "prior_art.json") as f:
        data = json.load(f)
    for pa in data:
        candidate = PriorArtCandidate(
            id=pa["id"],
            title=pa["title"],
            source_type=pa["source_type"],
            source=pa["source"],
            publication_date=_parse_date(pa.get("publication_date")),
            relevant_text=pa["relevant_text"],
            keywords=pa["keywords"],
            url=pa.get("url", ""),
        )
        store.add_prior_art(candidate)


def seed_all(patent_store: PatentStore, graph_store: GraphStore, search_store: SearchStore) -> None:
    """Load all mock data into stores."""
    load_patents(patent_store)
    load_companies(graph_store)
    load_products(search_store)
    load_prior_art(search_store)
