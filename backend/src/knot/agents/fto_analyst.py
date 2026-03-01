"""Agent 7: FTO Risk Analyst - Claim-by-claim analysis, risk levels, exclude expired."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from knot.agents.base import BaseAgent
from knot.models.fto import ClaimMatch, InfringementAnalysis, FTOReport
from knot.services.similarity import claim_text_similarity, determine_risk_level
from knot.services.text_processing import extract_keywords
from knot.stores.patent_store import PatentStore

if TYPE_CHECKING:
    from knot.services.llm_service import LLMService

_CLAIM_ANALYSIS_SYSTEM = """\
You are a patent claim analyst. Compare the patent claim against the product \
description. Assess infringement risk (high/medium/low), provide a similarity \
score (0.0-1.0), explain your reasoning in 2-3 sentences, and suggest \
mitigation steps if risk is medium or high.

Return ONLY valid JSON:
{
  "risk_level": "high" | "medium" | "low",
  "similarity_score": 0.0-1.0,
  "reasoning": "...",
  "mitigation_suggestions": ["..."]
}
"""

_FTO_RECOMMENDATION_SYSTEM = """\
You are a patent attorney assistant. Given the FTO analysis results below, \
write 2-4 concise, actionable recommendations for the product team. \
Return ONLY a JSON array of strings, e.g. ["rec1", "rec2"].\
"""


class FTOAnalystAgent(BaseAgent):
    agent_name = "fto_analyst"

    def __init__(self, patent_store: PatentStore, llm_service: "LLMService | None" = None):
        self.patent_store = patent_store
        self._llm = llm_service

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "analyze_fto":
            return self._analyze_fto(payload)
        elif task_type == "check_patent":
            return self._check_single_patent(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _analyze_fto(self, payload: dict) -> dict:
        description = payload.get("description", "")
        target_markets = payload.get("target_markets", [])
        keywords = payload.get("keywords", [])

        if not keywords:
            keywords = extract_keywords(description)

        # Search for relevant patents
        patents = self.patent_store.search_by_keywords(keywords, target_markets if target_markets else None)

        if not patents and target_markets:
            # Try without jurisdiction filter
            patents = self.patent_store.search_by_keywords(keywords)

        analyses = []
        today = date.today()

        for patent in patents:
            # Skip expired patents
            if patent.status == "expired" or (patent.expiry_date and patent.expiry_date < today):
                continue

            # Check jurisdiction overlap
            if target_markets:
                jurisdiction_overlap = any(j in patent.jurisdictions for j in target_markets)
                if not jurisdiction_overlap:
                    continue

            # Claim-by-claim analysis
            claim_matches = []
            max_risk = "low"
            use_llm = self._llm and self._llm.is_available

            for claim in patent.claims:
                llm_result = None
                if use_llm:
                    user_msg = (
                        f"Patent claim (claim {claim.number}):\n{claim.text}\n\n"
                        f"Product description:\n{description}"
                    )
                    llm_result = self._llm.chat_json(_CLAIM_ANALYSIS_SYSTEM, user_msg, max_tokens=512)

                if llm_result:
                    sim = float(llm_result.get("similarity_score", 0.0))
                    risk = llm_result.get("risk_level", "low")
                    reasoning = llm_result.get("reasoning", "")
                    mitigations = llm_result.get("mitigation_suggestions", [])
                    matched_kw = []  # LLM reasoning replaces keyword matching
                else:
                    sim, matched_kw = claim_text_similarity(claim.text, description)
                    risk = determine_risk_level(sim)
                    reasoning = ""
                    mitigations = []

                if sim > 0.05:
                    claim_matches.append(ClaimMatch(
                        patent_id=patent.id,
                        claim_number=claim.number,
                        claim_text=claim.text[:200],
                        similarity_score=sim,
                        matched_keywords=matched_kw,
                        risk_level=risk,
                        reasoning=reasoning,
                        mitigation_suggestions=mitigations,
                    ))
                    if risk == "high":
                        max_risk = "high"
                    elif risk == "medium" and max_risk != "high":
                        max_risk = "medium"

            if claim_matches:
                # Generate recommendation
                if max_risk == "high":
                    rec = f"HIGH RISK: Patent {patent.publication_number} has claims closely matching your product. Consider design-around or licensing."
                elif max_risk == "medium":
                    rec = f"MEDIUM RISK: Patent {patent.publication_number} has some overlap. Monitor and consider legal review."
                else:
                    rec = f"LOW RISK: Patent {patent.publication_number} has minimal overlap."

                analyses.append(InfringementAnalysis(
                    patent_id=patent.id,
                    patent_title=patent.title,
                    assignee=patent.assignees[0] if patent.assignees else "",
                    overall_risk=max_risk,
                    claim_matches=claim_matches,
                    recommendation=rec,
                ))

        # Sort by risk level
        risk_order = {"high": 0, "medium": 1, "low": 2, "none": 3}
        analyses.sort(key=lambda a: risk_order.get(a.overall_risk, 3))

        high_risk = sum(1 for a in analyses if a.overall_risk == "high")
        medium_risk = sum(1 for a in analyses if a.overall_risk == "medium")
        low_risk = sum(1 for a in analyses if a.overall_risk == "low")

        overall = "high" if high_risk > 0 else "medium" if medium_risk > 0 else "low"

        recommendations = []
        if use_llm and analyses:
            import json
            summary_ctx = json.dumps(
                {"description": description[:300], "high": high_risk, "medium": medium_risk, "low": low_risk,
                 "top_risks": [{"patent": a.patent_title, "risk": a.overall_risk, "rec": a.recommendation} for a in analyses[:5]]},
                default=str,
            )
            llm_recs = self._llm.chat_json(_FTO_RECOMMENDATION_SYSTEM, summary_ctx, max_tokens=512)
            if isinstance(llm_recs, list):
                recommendations = llm_recs

        if not recommendations:
            if high_risk:
                recommendations.append(f"Found {high_risk} high-risk patent(s). Immediate legal review recommended.")
            if medium_risk:
                recommendations.append(f"Found {medium_risk} medium-risk patent(s). Consider design modifications.")
            if not analyses:
                recommendations.append("No significant patent risks identified in target markets.")

        report = FTOReport(
            product_description=description[:200],
            target_markets=target_markets,
            analyses=analyses,
            overall_risk=overall,
            summary=f"FTO analysis found {len(analyses)} relevant patents: {high_risk} high-risk, {medium_risk} medium-risk, {low_risk} low-risk.",
            high_risk_count=high_risk,
            medium_risk_count=medium_risk,
            low_risk_count=low_risk,
            recommendations=recommendations,
        )

        return {
            "report": report.model_dump(),
            "confidence_score": 0.85,
        }

    def _check_single_patent(self, payload: dict) -> dict:
        patent_id = payload.get("patent_id", "")
        description = payload.get("description", "")

        patent = self.patent_store.get(patent_id)
        if not patent:
            raise ValueError(f"Patent {patent_id} not found")

        claim_matches = []
        for claim in patent.claims:
            sim, matched_kw = claim_text_similarity(claim.text, description)
            risk = determine_risk_level(sim)
            claim_matches.append(ClaimMatch(
                patent_id=patent_id,
                claim_number=claim.number,
                claim_text=claim.text[:200],
                similarity_score=sim,
                matched_keywords=matched_kw,
                risk_level=risk,
            ))

        max_risk = "low"
        for cm in claim_matches:
            if cm.risk_level == "high":
                max_risk = "high"
            elif cm.risk_level == "medium" and max_risk != "high":
                max_risk = "medium"

        return {
            "patent_id": patent_id,
            "patent_title": patent.title,
            "overall_risk": max_risk,
            "claim_matches": [cm.model_dump() for cm in claim_matches],
            "confidence_score": 0.85,
        }
