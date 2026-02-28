"""Technology landscape and white space models."""

from pydantic import BaseModel, Field


class PatentCluster(BaseModel):
    id: str
    label: str = ""
    keywords: list[str] = Field(default_factory=list)
    patent_ids: list[str] = Field(default_factory=list)
    density: float = 0.0
    classification_codes: list[str] = Field(default_factory=list)


class WhiteSpace(BaseModel):
    id: str
    description: str
    adjacent_clusters: list[str] = Field(default_factory=list)
    opportunity_score: float = Field(ge=0, le=1, default=0.5)
    suggested_keywords: list[str] = Field(default_factory=list)


class RankedOpportunity(BaseModel):
    white_space: WhiteSpace
    rank: int
    rationale: str = ""
    competitive_intensity: str = Field(default="medium", description="low, medium, high")


class LandscapeReport(BaseModel):
    domain: str
    clusters: list[PatentCluster] = Field(default_factory=list)
    white_spaces: list[WhiteSpace] = Field(default_factory=list)
    opportunities: list[RankedOpportunity] = Field(default_factory=list)
    total_patents_analyzed: int = 0
    summary: str = ""
