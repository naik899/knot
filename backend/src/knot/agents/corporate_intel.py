"""Agent 2: Corporate Intelligence - Ownership graphs and assignee resolution."""

from knot.agents.base import BaseAgent
from knot.services.graph_traversal import find_ultimate_parent, get_all_subsidiaries, resolve_assignee_to_company
from knot.stores.graph_store import GraphStore
from knot.stores.patent_store import PatentStore


class CorporateIntelAgent(BaseAgent):
    agent_name = "corporate_intel"

    def __init__(self, graph_store: GraphStore, patent_store: PatentStore):
        self.graph_store = graph_store
        self.patent_store = patent_store

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "resolve_parent":
            return self._resolve_parent(payload)
        elif task_type == "get_graph":
            return self._get_graph(payload)
        elif task_type == "resolve_assignees":
            return self._resolve_assignees(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _resolve_parent(self, payload: dict) -> dict:
        company_name = payload.get("company_name", "")
        company_id = payload.get("company_id", "")

        if company_id:
            company = self.graph_store.get_company(company_id)
        else:
            company = self.graph_store.find_company_by_name(company_name)

        if not company:
            return {
                "resolved": False,
                "company_name": company_name or company_id,
                "error": "Company not found",
                "confidence_score": 0.0,
            }

        parent_id = find_ultimate_parent(self.graph_store, company.id)
        parent = self.graph_store.get_company(parent_id)
        subsidiaries = get_all_subsidiaries(self.graph_store, parent_id)

        # Get all patents owned by the parent and its subsidiaries
        all_entity_ids = [parent_id] + subsidiaries
        patent_ids = []
        for eid in all_entity_ids:
            entity = self.graph_store.get_company(eid)
            if entity:
                patent_ids.extend(entity.patent_ids)

        return {
            "resolved": True,
            "query_company": company.canonical_name,
            "query_company_id": company.id,
            "query_company_type": company.company_type,
            "ultimate_parent_id": parent_id,
            "ultimate_parent_name": parent.canonical_name if parent else None,
            "subsidiary_count": len(subsidiaries),
            "subsidiaries": subsidiaries,
            "total_patents": len(patent_ids),
            "patent_ids": patent_ids,
            "confidence_score": 0.95,
        }

    def _get_graph(self, payload: dict) -> dict:
        company_id = payload.get("company_id", "")
        company = self.graph_store.get_company(company_id)
        if not company:
            return {"error": "Company not found", "confidence_score": 0.0}

        graph = self.graph_store.get_ownership_graph(company_id)
        return {
            "company_id": company_id,
            "company_name": company.canonical_name,
            "nodes": [
                {
                    "id": n.id,
                    "name": n.canonical_name,
                    "type": n.company_type,
                    "jurisdiction": n.jurisdiction,
                    "patent_count": len(n.patent_ids),
                }
                for n in graph.nodes
            ],
            "edges": [
                {
                    "from": e.from_company_id,
                    "to": e.to_company_id,
                    "ownership_percentage": e.ownership_percentage,
                    "source": e.source,
                }
                for e in graph.edges
            ],
            "confidence_score": 0.95,
        }

    def _resolve_assignees(self, payload: dict) -> dict:
        assignees = payload.get("assignees", [])
        results = []
        for assignee in assignees:
            result = resolve_assignee_to_company(self.graph_store, assignee)
            results.append(result)

        resolved_count = sum(1 for r in results if r["resolved"])
        return {
            "assignee_resolutions": results,
            "total": len(assignees),
            "resolved_count": resolved_count,
            "resolution_rate": resolved_count / max(len(assignees), 1),
            "confidence_score": resolved_count / max(len(assignees), 1),
        }
