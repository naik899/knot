"""Agent 5: Integration Agent - Data unification, duplicate detection, conflict resolution."""

from knot.agents.base import BaseAgent
from knot.services.similarity import keyword_similarity
from knot.services.text_processing import normalize_text
from knot.stores.patent_store import PatentStore


class IntegrationAgent(BaseAgent):
    agent_name = "integration"

    def __init__(self, patent_store: PatentStore):
        self.patent_store = patent_store

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "detect_duplicates":
            return self._detect_duplicates(payload)
        elif task_type == "unify_records":
            return self._unify_records(payload)
        elif task_type == "resolve_conflict":
            return self._resolve_conflict(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _detect_duplicates(self, payload: dict) -> dict:
        patent_id = payload.get("patent_id")
        patent = self.patent_store.get(patent_id)
        if not patent:
            raise ValueError(f"Patent {patent_id} not found")

        duplicates = []
        all_patents = self.patent_store.get_all()
        normalized_title = normalize_text(patent.title)

        for other in all_patents:
            if other.id == patent_id:
                continue
            # Check for duplicates by title similarity and keyword overlap
            other_title = normalize_text(other.title)
            title_match = normalized_title == other_title
            kw_sim = keyword_similarity(patent.keywords, other.keywords)

            if title_match or kw_sim > 0.6:
                duplicates.append({
                    "patent_id": other.id,
                    "title": other.title,
                    "similarity": kw_sim,
                    "match_type": "title" if title_match else "keywords",
                })

        return {
            "patent_id": patent_id,
            "duplicates": duplicates,
            "duplicate_count": len(duplicates),
            "confidence_score": 0.85,
        }

    def _unify_records(self, payload: dict) -> dict:
        patent_ids = payload.get("patent_ids", [])
        patents = [self.patent_store.get(pid) for pid in patent_ids]
        patents = [p for p in patents if p is not None]

        if not patents:
            return {"unified": False, "error": "No valid patents found", "confidence_score": 0.0}

        # Use the most recent patent as the canonical version
        canonical = sorted(patents, key=lambda p: p.publication_date or "0000-00-00", reverse=True)[0]

        # Merge keywords from all sources
        all_keywords = set()
        all_sources = set()
        for p in patents:
            all_keywords.update(p.keywords)
            all_sources.add(p.source)

        return {
            "unified": True,
            "canonical_id": canonical.id,
            "merged_keywords": sorted(all_keywords),
            "sources": sorted(all_sources),
            "records_merged": len(patents),
            "confidence_score": 0.9,
        }

    def _resolve_conflict(self, payload: dict) -> dict:
        field = payload.get("field", "")
        values = payload.get("values", [])
        sources = payload.get("sources", [])

        if not values:
            return {"resolved_value": None, "strategy": "none", "confidence_score": 0.0}

        # Priority: most recent authoritative source
        # Simple strategy: prefer USPTO > EPO > CGPDTM, or first non-empty value
        source_priority = {"USPTO": 3, "EPO": 2, "CGPDTM": 1}

        if sources:
            best_idx = 0
            best_priority = 0
            for i, source in enumerate(sources):
                priority = source_priority.get(source, 0)
                if priority > best_priority:
                    best_priority = priority
                    best_idx = i
            resolved = values[best_idx] if best_idx < len(values) else values[0]
        else:
            resolved = values[0]

        return {
            "field": field,
            "resolved_value": resolved,
            "strategy": "source_priority",
            "confidence_score": 0.8,
        }
