"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from knot.main import create_app
from knot.api.dependencies import get_container
from knot.mock_data.seed import seed_all


@pytest.fixture
def client():
    app = create_app()
    container = get_container()
    seed_all(container.patent_store, container.graph_store, container.search_store)
    return TestClient(app)


class TestHealthEndpoint:
    def test_health(self, client):
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["stores"]["patents"] > 0


class TestQueryEndpoint:
    def test_fto_query(self, client):
        resp = client.post("/api/v1/query", json={
            "query": "Analyze FTO for IoT temperature sensor in US",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "executive_summary" in data

    def test_corporate_query(self, client):
        resp = client.post("/api/v1/query", json={
            "query": "Who owns SensorTech?",
        })
        assert resp.status_code == 200


class TestFTOEndpoint:
    def test_fto_analyze(self, client):
        resp = client.post("/api/v1/fto/analyze", json={
            "description": "IoT temperature sensor",
            "target_markets": ["US"],
            "keywords": ["iot", "temperature", "sensor"],
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "report" in data
        assert "analyses" in data["report"]


class TestCorporateEndpoints:
    def test_resolve(self, client):
        resp = client.post("/api/v1/corporate/resolve", json={
            "company_name": "SensorTech",
        })
        assert resp.status_code == 200

    def test_graph(self, client):
        resp = client.get("/api/v1/corporate/graph/COMP001")
        assert resp.status_code == 200
        data = resp.json()
        assert "nodes" in data


class TestLandscapeEndpoint:
    def test_analyze(self, client):
        resp = client.post("/api/v1/landscape/analyze", json={
            "domain": "IoT sensors",
            "keywords": ["iot", "sensor"],
        })
        assert resp.status_code == 200


class TestValidityEndpoint:
    def test_prior_art(self, client):
        resp = client.post("/api/v1/validity/prior-art", json={
            "patent_id": "PAT001",
            "keywords": ["sensor"],
        })
        assert resp.status_code == 200


class TestProductsEndpoint:
    def test_match(self, client):
        resp = client.post("/api/v1/products/match", json={
            "description": "temperature sensor",
            "keywords": ["temperature", "sensor"],
        })
        assert resp.status_code == 200


class TestPatentsEndpoints:
    def test_get_patent(self, client):
        resp = client.get("/api/v1/patents/PAT001")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "PAT001"

    def test_get_nonexistent(self, client):
        resp = client.get("/api/v1/patents/NONEXISTENT")
        assert resp.status_code == 404

    def test_search(self, client):
        resp = client.get("/api/v1/patents/search?q=temperature")
        assert resp.status_code == 200
        data = resp.json()
        assert "results" in data
