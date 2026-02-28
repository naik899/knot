"""Prior art and patent validity models."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class PriorArtCandidate(BaseModel):
    id: str
    title: str
    source_type: str = Field(description="patent, academic, standard, publication")
    source: str = ""
    publication_date: Optional[date] = None
    relevant_text: str = ""
    keywords: list[str] = Field(default_factory=list)
    url: str = ""


class PriorArtAnalysis(BaseModel):
    prior_art_id: str
    target_patent_id: str
    relevance_score: float = Field(ge=0, le=1)
    matched_claims: list[int] = Field(default_factory=list)
    matched_keywords: list[str] = Field(default_factory=list)
    analysis: str = ""


class ValidityReport(BaseModel):
    target_patent_id: str
    target_patent_title: str = ""
    prior_art_results: list[PriorArtAnalysis] = Field(default_factory=list)
    overall_validity: str = Field(default="appears_valid", description="appears_valid, questionable, likely_invalid")
    summary: str = ""
    strongest_prior_art: Optional[str] = None
