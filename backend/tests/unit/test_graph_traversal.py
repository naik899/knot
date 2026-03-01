"""Tests for graph traversal service."""

from datetime import date
from knot.stores.graph_store import GraphStore
from knot.models.company import Company, OwnershipEdge
from knot.services.graph_traversal import (
    find_ultimate_parent,
    get_all_subsidiaries,
)


def _build_test_graph():
    store = GraphStore()
    # Parent -> Sub1 -> Sub2
    store.add_company(Company(id="P", canonical_name="Parent", aliases=[], company_type="corporation", jurisdiction="US", subsidiaries=["S1"]))
    store.add_company(Company(id="S1", canonical_name="Sub1", aliases=[], company_type="subsidiary", jurisdiction="US", subsidiaries=["S2"]))
    store.add_company(Company(id="S2", canonical_name="Sub2", aliases=[], company_type="subsidiary", jurisdiction="US", subsidiaries=[]))
    store.add_edge(OwnershipEdge(from_company_id="P", to_company_id="S1", ownership_percentage=100.0, effective_date=date(2020, 1, 1), source="test"))
    store.add_edge(OwnershipEdge(from_company_id="S1", to_company_id="S2", ownership_percentage=100.0, effective_date=date(2020, 1, 1), source="test"))
    return store


class TestFindUltimateParent:
    def test_direct_parent(self):
        store = _build_test_graph()
        assert find_ultimate_parent(store, "S1") == "P"

    def test_grandchild(self):
        store = _build_test_graph()
        assert find_ultimate_parent(store, "S2") == "P"

    def test_already_root(self):
        store = _build_test_graph()
        assert find_ultimate_parent(store, "P") == "P"


class TestGetAllSubsidiaries:
    def test_gets_all(self):
        store = _build_test_graph()
        subs = get_all_subsidiaries(store, "P")
        assert "S1" in subs
        assert "S2" in subs

    def test_leaf_has_none(self):
        store = _build_test_graph()
        subs = get_all_subsidiaries(store, "S2")
        assert len(subs) == 0
