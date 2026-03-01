"""Agent 3: Market Analyst - Patent-product keyword matching."""

from __future__ import annotations

from typing import TYPE_CHECKING

from knot.agents.base import BaseAgent
from knot.models.product import ProductMatch
from knot.services.similarity import keyword_similarity, claim_text_similarity
from knot.services.text_processing import extract_keywords
from knot.stores.patent_store import PatentStore
from knot.stores.search_store import SearchStore

if TYPE_CHECKING:
    from knot.services.llm_service import LLMService

_PATENT_PRODUCT_SYSTEM = """\
You are a patent-product matching analyst. Given a patent's title, abstract, \
and keywords alongside a product description, assess how relevant the patent \
is to the product. Return ONLY valid JSON:
{
  "relevance_score": 0.0-1.0,
  "evidence": ["reason 1", "reason 2"],
  "matching_claims_hint": [list of claim numbers most relevant, or empty]
}
"""


class MarketAnalystAgent(BaseAgent):
    agent_name = "market_analyst"

    def __init__(self, patent_store: PatentStore, search_store: SearchStore, llm_service: "LLMService | None" = None):
        self.patent_store = patent_store
        self.search_store = search_store
        self._llm = llm_service

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "find_product_matches":
            return self._find_product_matches(payload)
        elif task_type == "match_patent_to_products":
            return self._match_patent_to_products(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _find_product_matches(self, payload: dict) -> dict:
        patent_id = payload.get("patent_id", "")
        patent = self.patent_store.get(patent_id)
        if not patent:
            raise ValueError(f"Patent {patent_id} not found")

        products = self.search_store.get_all_products()
        matches = []

        for product in products:
            # Compare patent keywords with product description keywords
            product_keywords = extract_keywords(f"{product.name} {product.description}")
            sim = keyword_similarity(patent.keywords, product_keywords)

            if sim > 0.1:
                # Check claim-level matching
                matching_claims = []
                for claim in patent.claims:
                    claim_sim, matched_kw = claim_text_similarity(claim.text, product.description)
                    if claim_sim > 0.1:
                        matching_claims.append(claim.number)

                match = ProductMatch(
                    patent_id=patent_id,
                    product_id=product.id,
                    product_name=product.name,
                    manufacturer=product.manufacturer,
                    confidence_score=min(sim * 2, 1.0),  # Scale up for readability
                    matching_claims=matching_claims,
                    evidence=[f"Keyword overlap: {sim:.2f}"],
                    matched_keywords=sorted(set(patent.keywords) & set(product_keywords)),
                )
                matches.append(match)

        # Sort by confidence
        matches.sort(key=lambda m: m.confidence_score, reverse=True)

        return {
            "patent_id": patent_id,
            "matches": [m.model_dump() for m in matches],
            "total_matches": len(matches),
            "confidence_score": 0.85 if matches else 0.5,
        }

    def _match_patent_to_products(self, payload: dict) -> dict:
        """Match a product description against all patents."""
        description = payload.get("description", "")
        keywords = payload.get("keywords", [])

        if not keywords:
            keywords = extract_keywords(description)

        all_patents = self.patent_store.get_all()
        matches = []
        use_llm = self._llm and self._llm.is_available

        for patent in all_patents:
            sim = keyword_similarity(keywords, patent.keywords)
            evidence = [f"Keyword overlap: {sim:.2f}"]
            matched_kw = sorted(set(k.lower() for k in keywords) & set(k.lower() for k in patent.keywords))

            # LLM re-scoring for candidates that pass keyword threshold
            if use_llm and sim > 0.05:
                user_msg = (
                    f"Patent: {patent.title}\n"
                    f"Patent keywords: {', '.join(patent.keywords[:15])}\n\n"
                    f"Product description: {description[:500]}"
                )
                llm_result = self._llm.chat_json(_PATENT_PRODUCT_SYSTEM, user_msg, max_tokens=256)
                if llm_result:
                    sim = float(llm_result.get("relevance_score", sim))
                    evidence = llm_result.get("evidence", evidence)

            if sim > 0.1:
                matches.append({
                    "patent_id": patent.id,
                    "patent_title": patent.title,
                    "assignee": patent.assignees[0] if patent.assignees else "",
                    "similarity": sim,
                    "matched_keywords": matched_kw,
                    "evidence": evidence,
                })

        matches.sort(key=lambda m: m["similarity"], reverse=True)

        return {
            "description": description[:100],
            "matches": matches[:20],
            "total_matches": len(matches),
            "confidence_score": 0.8,
        }
