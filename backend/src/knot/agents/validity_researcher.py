"""Agent 8: Validity Researcher - Prior art search with date filtering."""

from __future__ import annotations

from typing import TYPE_CHECKING

from knot.agents.base import BaseAgent
from knot.models.validity import PriorArtAnalysis, ValidityReport
from knot.services.similarity import keyword_similarity
from knot.services.text_processing import extract_keywords
from knot.stores.patent_store import PatentStore
from knot.stores.search_store import SearchStore

if TYPE_CHECKING:
    from knot.services.llm_service import LLMService

_PRIOR_ART_RELEVANCE_SYSTEM = """\
You are a patent validity analyst. Given a prior art document and target patent \
claims, assess whether the prior art anticipates or renders obvious the claims.

Return ONLY valid JSON:
{
  "relevance_score": 0.0-1.0,
  "analysis": "2-3 sentence explanation of how the prior art relates to the claims",
  "anticipates_claims": [list of claim numbers that may be anticipated],
  "obviousness_claims": [list of claim numbers that may be obvious in view of this art]
}
"""

_VALIDITY_OPINION_SYSTEM = """\
You are a patent validity analyst. Given the prior art search results below, \
provide a concise validity opinion. State whether the patent appears valid, \
questionable, or likely invalid, and explain why. Return plain text (not JSON).\
"""


class ValidityResearcherAgent(BaseAgent):
    agent_name = "validity_researcher"

    def __init__(self, patent_store: PatentStore, search_store: SearchStore, llm_service: "LLMService | None" = None):
        self.patent_store = patent_store
        self.search_store = search_store
        self._llm = llm_service

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "find_prior_art":
            return self._find_prior_art(payload)
        elif task_type == "validate_patent":
            return self._validate_patent(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _find_prior_art(self, payload: dict) -> dict:
        patent_id = payload.get("patent_id", "")
        keywords = payload.get("keywords", [])

        patent = self.patent_store.get(patent_id) if patent_id else None

        if patent and not keywords:
            keywords = patent.keywords

        # Search prior art store
        candidates = self.search_store.search_prior_art(keywords)

        # Filter by date if we have a target patent
        if patent and patent.filing_date:
            candidates = [
                c for c in candidates
                if c.publication_date is None or c.publication_date < patent.filing_date
            ]

        # Score each candidate
        results = []
        use_llm = self._llm and self._llm.is_available and patent

        for candidate in candidates:
            pa_keywords = candidate.keywords
            relevance = keyword_similarity(keywords, pa_keywords)

            # Check which claims might be affected
            matched_claims = []
            analysis_text = ""

            if use_llm:
                claims_text = "\n".join(f"Claim {c.number}: {c.text}" for c in patent.claims[:10])
                user_msg = (
                    f"Prior art title: {candidate.title}\n"
                    f"Prior art keywords: {', '.join(pa_keywords)}\n"
                    f"Prior art date: {candidate.publication_date}\n\n"
                    f"Target patent claims:\n{claims_text}"
                )
                llm_result = self._llm.chat_json(_PRIOR_ART_RELEVANCE_SYSTEM, user_msg, max_tokens=512)
                if llm_result:
                    relevance = float(llm_result.get("relevance_score", relevance))
                    analysis_text = llm_result.get("analysis", "")
                    matched_claims = (
                        llm_result.get("anticipates_claims", [])
                        + llm_result.get("obviousness_claims", [])
                    )
                    # Deduplicate
                    matched_claims = sorted(set(matched_claims))

            if not matched_claims and patent:
                for claim in patent.claims:
                    claim_kw = extract_keywords(claim.text)
                    claim_sim = keyword_similarity(claim_kw, pa_keywords)
                    if claim_sim > 0.1:
                        matched_claims.append(claim.number)

            if not analysis_text:
                analysis_text = f"Prior art '{candidate.title}' published {candidate.publication_date} has {relevance:.0%} relevance."

            if relevance > 0.05:
                results.append(PriorArtAnalysis(
                    prior_art_id=candidate.id,
                    target_patent_id=patent_id,
                    relevance_score=relevance,
                    matched_claims=matched_claims,
                    matched_keywords=sorted(set(k.lower() for k in keywords) & set(k.lower() for k in pa_keywords)),
                    analysis=analysis_text,
                ))

        results.sort(key=lambda r: r.relevance_score, reverse=True)

        return {
            "patent_id": patent_id,
            "prior_art_results": [r.model_dump() for r in results],
            "total_candidates": len(results),
            "confidence_score": 0.8 if results else 0.5,
        }

    def _validate_patent(self, payload: dict) -> dict:
        patent_id = payload.get("patent_id", "")
        patent = self.patent_store.get(patent_id)
        if not patent:
            raise ValueError(f"Patent {patent_id} not found")

        # Find prior art
        prior_art_result = self._find_prior_art({"patent_id": patent_id})
        results = prior_art_result["prior_art_results"]

        # Determine overall validity
        if not results:
            validity = "appears_valid"
            summary = f"No prior art found that predates patent {patent.publication_number}. Patent appears novel."
            strongest = None
        else:
            max_relevance = max(r["relevance_score"] for r in results)
            if max_relevance > 0.5:
                validity = "likely_invalid"
                summary = f"Strong prior art found with {max_relevance:.0%} relevance. Patent validity is questionable."
            elif max_relevance > 0.25:
                validity = "questionable"
                summary = f"Moderate prior art found with {max_relevance:.0%} relevance. Further investigation recommended."
            else:
                validity = "appears_valid"
                summary = f"Only weak prior art found (max {max_relevance:.0%} relevance). Patent appears valid."
            strongest = results[0]["prior_art_id"] if results else None

            # LLM-powered validity opinion
            if self._llm and self._llm.is_available:
                import json
                context = json.dumps(
                    {"patent": patent.title, "prior_art": results[:5], "rule_based_validity": validity},
                    default=str,
                )
                llm_opinion = self._llm.chat(_VALIDITY_OPINION_SYSTEM, context, max_tokens=512)
                if llm_opinion:
                    summary = llm_opinion

        report = ValidityReport(
            target_patent_id=patent_id,
            target_patent_title=patent.title,
            prior_art_results=[PriorArtAnalysis(**r) for r in results],
            overall_validity=validity,
            summary=summary,
            strongest_prior_art=strongest,
        )

        return {
            "report": report.model_dump(),
            "confidence_score": 0.85,
        }
