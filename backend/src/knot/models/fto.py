"""Freedom to Operate analysis models."""

from pydantic import BaseModel, Field


class ClaimMatch(BaseModel):
    patent_id: str
    claim_number: int
    claim_text: str = ""
    similarity_score: float = Field(ge=0, le=1)
    matched_keywords: list[str] = Field(default_factory=list)
    risk_level: str = Field(description="high, medium, low")
    reasoning: str = ""
    mitigation_suggestions: list[str] = Field(default_factory=list)


class InfringementAnalysis(BaseModel):
    patent_id: str
    patent_title: str = ""
    assignee: str = ""
    overall_risk: str = Field(description="high, medium, low, none")
    claim_matches: list[ClaimMatch] = Field(default_factory=list)
    recommendation: str = ""


class FTOReport(BaseModel):
    product_description: str
    target_markets: list[str] = Field(default_factory=list)
    analyses: list[InfringementAnalysis] = Field(default_factory=list)
    overall_risk: str = "low"
    summary: str = ""
    high_risk_count: int = 0
    medium_risk_count: int = 0
    low_risk_count: int = 0
    recommendations: list[str] = Field(default_factory=list)
