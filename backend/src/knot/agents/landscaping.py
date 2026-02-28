"""Agent 6: Landscaping Specialist - Clustering and white space detection."""

from knot.agents.base import BaseAgent
from knot.models.landscape import PatentCluster, WhiteSpace, RankedOpportunity, LandscapeReport
from knot.services.clustering import cluster_patents, identify_white_spaces
from knot.services.text_processing import extract_keywords
from knot.stores.patent_store import PatentStore


class LandscapingAgent(BaseAgent):
    agent_name = "landscaping"

    def __init__(self, patent_store: PatentStore):
        self.patent_store = patent_store

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

        # Identify white spaces
        all_domain_keywords = set(domain_keywords)
        for p in patents:
            all_domain_keywords.update(p.keywords)

        # Add some potential white space keywords not in existing patents
        potential_keywords = {
            "underwater-iot", "quantum-sensing", "5g-sensor",
            "ai-calibration", "edge-ml", "digital-twin-sensor",
        }
        all_domain_keywords.update(potential_keywords)

        ws_data = identify_white_spaces(clusters, all_domain_keywords)

        white_spaces = []
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
