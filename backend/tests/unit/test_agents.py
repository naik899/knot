"""Tests for agent implementations."""

from knot.models.messages import AgentRequest
from knot.mock_data.seed import seed_all
from knot.api.dependencies import Container


def _make_request(target: str, task_type: str, payload: dict) -> AgentRequest:
    return AgentRequest(
        source_agent="test",
        target_agent=target,
        task_type=task_type,
        payload=payload,
    )


class TestDataCustodianAgent:
    def test_process_text(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("data_custodian", "process_text", {
            "text": "A Temperature SENSOR with   Wireless Communication!!",
        })
        resp = container.data_custodian.handle_request(req)
        assert resp.status == "success"
        assert "processed_text" in resp.result

    def test_validate_patent(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("data_custodian", "validate_patent", {
            "patent_id": "PAT001",
        })
        resp = container.data_custodian.handle_request(req)
        assert resp.status == "success"
        assert "is_valid" in resp.result


class TestCorporateIntelAgent:
    def test_resolve_parent(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("corporate_intel", "resolve_parent", {
            "company_name": "SensorTech",
        })
        resp = container.corporate_intel.handle_request(req)
        assert resp.status == "success"
        assert resp.result["resolved"] is True
        assert resp.result["ultimate_parent_name"] == "TechGlobal Corp"

    def test_get_graph(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("corporate_intel", "get_graph", {
            "company_id": "COMP001",
        })
        resp = container.corporate_intel.handle_request(req)
        assert resp.status == "success"
        assert "nodes" in resp.result
        assert "edges" in resp.result


class TestFTOAnalystAgent:
    def test_analyze_fto(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("fto_analyst", "analyze_fto", {
            "description": "IoT temperature sensor with wireless communication",
            "target_markets": ["US"],
            "keywords": ["iot", "temperature", "sensor", "wireless"],
        })
        resp = container.fto_analyst.handle_request(req)
        assert resp.status == "success"
        assert "report" in resp.result
        report = resp.result["report"]
        assert "analyses" in report
        assert "summary" in report

    def test_check_single_patent(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("fto_analyst", "check_patent", {
            "patent_id": "PAT001",
            "description": "temperature sensor device",
        })
        resp = container.fto_analyst.handle_request(req)
        assert resp.status == "success"


class TestMarketAnalystAgent:
    def test_match_products(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("market_analyst", "match_patent_to_products", {
            "description": "IoT temperature sensor",
            "keywords": ["iot", "temperature", "sensor"],
        })
        resp = container.market_analyst.handle_request(req)
        assert resp.status == "success"
        assert "matches" in resp.result


class TestLandscapingAgent:
    def test_analyze_landscape(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("landscaping", "analyze_landscape", {
            "domain": "IoT sensors",
            "keywords": ["iot", "sensor"],
        })
        resp = container.landscaping.handle_request(req)
        assert resp.status == "success"
        assert "report" in resp.result


class TestValidityResearcherAgent:
    def test_find_prior_art(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("validity_researcher", "find_prior_art", {
            "patent_id": "PAT001",
            "keywords": ["sensor", "temperature"],
        })
        resp = container.validity_researcher.handle_request(req)
        assert resp.status == "success"
        assert "prior_art_results" in resp.result


class TestRouterAgent:
    def test_fto_query(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("router", "route_query", {
            "query": "Analyze FTO for IoT temperature sensor in US",
        })
        resp = container.router.handle_request(req)
        assert resp.status == "success"
        assert "executive_summary" in resp.result

    def test_corporate_query(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("router", "route_query", {
            "query": "Who owns SensorTech Innovations?",
        })
        resp = container.router.handle_request(req)
        assert resp.status == "success"

    def test_landscape_query(self):
        container = Container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        req = _make_request("router", "route_query", {
            "query": "Show patent landscape for IoT sensors",
        })
        resp = container.router.handle_request(req)
        assert resp.status == "success"
