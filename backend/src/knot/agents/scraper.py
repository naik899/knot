"""Agent 4: Scraper & API Connector - Mock API ingestion with simulated rate limits."""

import time

from knot.agents.base import BaseAgent
from knot.stores.patent_store import PatentStore


class ScraperAgent(BaseAgent):
    agent_name = "scraper"

    def __init__(self, patent_store: PatentStore):
        self.patent_store = patent_store
        self._request_count = 0
        self._rate_limit = 10  # max requests per "minute" (simulated)

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "fetch_patents":
            return self._fetch_patents(payload)
        elif task_type == "fetch_by_source":
            return self._fetch_by_source(payload)
        elif task_type == "check_status":
            return self._check_status()
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _simulate_rate_limit(self) -> dict | None:
        """Simulate API rate limiting."""
        self._request_count += 1
        if self._request_count > self._rate_limit:
            return {
                "rate_limited": True,
                "retry_after_seconds": 60,
                "message": "Rate limit exceeded. Simulating backoff.",
            }
        return None

    def _fetch_patents(self, payload: dict) -> dict:
        rate_check = self._simulate_rate_limit()
        if rate_check:
            return {**rate_check, "patents": [], "confidence_score": 0.5}

        keywords = payload.get("keywords", [])
        jurisdictions = payload.get("jurisdictions", None)

        # Search existing store (simulating API fetch)
        results = self.patent_store.search_by_keywords(keywords, jurisdictions)

        return {
            "patents": [
                {
                    "id": p.id,
                    "title": p.title,
                    "source": p.source,
                    "publication_number": p.publication_number,
                    "assignees": p.assignees,
                    "status": p.status,
                }
                for p in results
            ],
            "total_found": len(results),
            "source": "mock_api",
            "rate_limited": False,
            "confidence_score": 0.9,
        }

    def _fetch_by_source(self, payload: dict) -> dict:
        rate_check = self._simulate_rate_limit()
        if rate_check:
            return {**rate_check, "patents": [], "confidence_score": 0.5}

        source = payload.get("source", "USPTO")
        all_patents = self.patent_store.get_all()
        results = [p for p in all_patents if p.source == source]

        return {
            "patents": [
                {
                    "id": p.id,
                    "title": p.title,
                    "source": p.source,
                    "publication_number": p.publication_number,
                }
                for p in results
            ],
            "total_found": len(results),
            "source": source,
            "confidence_score": 0.95,
        }

    def _check_status(self) -> dict:
        return {
            "status": "operational",
            "request_count": self._request_count,
            "rate_limit": self._rate_limit,
            "sources_available": ["USPTO", "EPO", "CGPDTM"],
            "confidence_score": 1.0,
        }
