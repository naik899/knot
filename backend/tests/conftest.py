"""Shared fixtures for all tests."""

import pytest
from knot.stores.patent_store import PatentStore
from knot.stores.graph_store import GraphStore
from knot.stores.search_store import SearchStore
from knot.mock_data.seed import seed_all
from knot.api.dependencies import Container


@pytest.fixture
def patent_store():
    store = PatentStore()
    return store


@pytest.fixture
def graph_store():
    store = GraphStore()
    return store


@pytest.fixture
def search_store():
    store = SearchStore()
    return store


@pytest.fixture
def seeded_container():
    """Container with all mock data loaded."""
    container = Container()
    seed_all(container.patent_store, container.graph_store, container.search_store)
    return container


@pytest.fixture
def seeded_patent_store(seeded_container):
    return seeded_container.patent_store


@pytest.fixture
def seeded_graph_store(seeded_container):
    return seeded_container.graph_store


@pytest.fixture
def seeded_search_store(seeded_container):
    return seeded_container.search_store
