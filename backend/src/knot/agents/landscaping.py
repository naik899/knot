"""Agent 6: Landscaping Specialist - Clustering and white space detection."""

from __future__ import annotations

from typing import TYPE_CHECKING

from knot.agents.base import BaseAgent
from knot.models.landscape import PatentCluster, WhiteSpace, RankedOpportunity, LandscapeReport
from knot.services.clustering import cluster_patents, identify_white_spaces
from knot.services.text_processing import extract_keywords
from knot.stores.patent_store import PatentStore

if TYPE_CHECKING:
    from knot.services.llm_service import LLMService

_CLUSTER_LABEL_SYSTEM = """\
You are a patent technology analyst. Given a list of patent titles and keywords \
belonging to a cluster, generate a concise descriptive label (3-6 words) and a \
one-sentence description of the technology area.

Return ONLY valid JSON:
{"label": "...", "description": "..."}
"""

_WHITE_SPACE_SYSTEM = """\
You are a patent landscape analyst. Given the existing technology clusters in a \
domain, identify innovation opportunities (white spaces) that are NOT yet \
covered by existing patents. For each white space, provide a description, an \
opportunity score (0.0-1.0), and 3-5 suggested keywords.

Return ONLY valid JSON array:
[{"description": "...", "opportunity_score": 0.0-1.0, "keywords": ["..."]}]
"""


class LandscapingAgent(BaseAgent):
    agent_name = "landscaping"

    def __init__(self, patent_store: PatentStore, llm_service: "LLMService | None" = None):
        self.patent_store = patent_store
        self._llm = llm_service

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "analyze_landscape":
            return self._analyze_landscape(payload)
        elif task_type == "find_white_spaces":
            return self._find_white_spaces(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _analyze_landscape(self, payload: dict) -> dict:
        domain = payload.get("domain", "")
        domain_keywords = payload.get("keywords", [])

        if not domain_keywords:
            domain_keywords = extract_keywords(domain)

        # Find relevant patents
        patents = self.patent_store.search_by_keywords(domain_keywords)
        if not patents:
            # Broaden search
            patents = self.patent_store.get_all()

        # Cluster patents
        clusters = cluster_patents(patents)

        # LLM-enhanced cluster labels
        use_llm = self._llm and self._llm.is_available
        if use_llm:
            for cluster in clusters:
                titles = [p_id for p_id in cluster.patent_ids[:10]]
                user_msg = (
                    f"Cluster keywords: {', '.join(cluster.keywords[:15])}\n"
                    f"Patent IDs in cluster: {', '.join(titles)}"
                )
                label_result = self._llm.chat_json(_CLUSTER_LABEL_SYSTEM, user_msg, max_tokens=256)
                if label_result:
                    cluster.label = label_result.get("label", cluster.label)
                    cluster.description = label_result.get("description", cluster.description)

        # Identify white spaces
        all_domain_keywords = set(domain_keywords)
        for p in patents:
            all_domain_keywords.update(p.keywords)

        # LLM-powered white space identification
        white_spaces = []
        if use_llm:
            import json
            cluster_summary = json.dumps(
                [{"label": c.label, "keywords": c.keywords[:10]} for c in clusters],
                default=str,
            )
            user_msg = f"Domain: {domain}\n\nExisting clusters:\n{cluster_summary}"
            llm_ws = self._llm.chat_json(_WHITE_SPACE_SYSTEM, user_msg, max_tokens=1024)
            if isinstance(llm_ws, list):
                for i, ws in enumerate(llm_ws):
                    white_spaces.append(WhiteSpace(
                        id=f"WS{i+1:03d}",
                        description=ws.get("description", ""),
                        adjacent_clusters=[],
                        opportunity_score=float(ws.get("opportunity_score", 0.5)),
                        suggested_keywords=ws.get("keywords", [])[:5],
                    ))

        # Fallback to rule-based white space detection
        if not white_spaces:
            potential_keywords = {
                "underwater-iot", "quantum-sensing", "5g-sensor",
                "ai-calibration", "edge-ml", "digital-twin-sensor",
            }
            all_domain_keywords.update(potential_keywords)
            ws_data = identify_white_spaces(clusters, all_domain_keywords)
            for i, ws in enumerate(ws_data):
                white_spaces.append(WhiteSpace(
                    id=f"WS{i+1:03d}",
                    description=ws["description"],
                    adjacent_clusters=ws.get("adjacent_clusters", []),
                    opportunity_score=ws.get("opportunity_score", 0.5),
                    suggested_keywords=ws.get("keywords", [])[:5],
                ))

        # Rank opportunities
        opportunities = []
        for i, ws in enumerate(white_spaces):
            competitive = "low" if ws.opportunity_score > 0.7 else "medium" if ws.opportunity_score > 0.4 else "high"
            opportunities.append(RankedOpportunity(
                white_space=ws,
                rank=i + 1,
                rationale=f"Opportunity in {ws.description[:50]} with score {ws.opportunity_score:.2f}",
                competitive_intensity=competitive,
            ))

        report = LandscapeReport(
            domain=domain,
            clusters=clusters,
            white_spaces=white_spaces,
            opportunities=opportunities,
            total_patents_analyzed=len(patents),
            summary=f"Analyzed {len(patents)} patents in {domain}. Found {len(clusters)} clusters and {len(white_spaces)} white spaces.",
        )

        return {
            "report": report.model_dump(),
            "confidence_score": 0.85,
        }

    def _find_white_spaces(self, payload: dict) -> dict:
        keywords = payload.get("keywords", [])
        patents = self.patent_store.search_by_keywords(keywords)
        clusters = cluster_patents(patents)

        all_kw = set(keywords)
        for p in patents:
            all_kw.update(p.keywords)

        ws_data = identify_white_spaces(clusters, all_kw)

        return {
            "white_spaces": ws_data,
            "patents_analyzed": len(patents),
            "clusters_found": len(clusters),
            "confidence_score": 0.8,
        }
