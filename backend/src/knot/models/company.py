"""Company and corporate ownership models."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Company(BaseModel):
    id: str
    canonical_name: str
    aliases: list[str] = Field(default_factory=list)
    ultimate_parent_id: Optional[str] = None
    subsidiaries: list[str] = Field(default_factory=list)
    jurisdiction: str = ""
    company_type: str = Field(default="corporation", description="corporation, subsidiary, shell")
    patent_ids: list[str] = Field(default_factory=list)


class OwnershipEdge(BaseModel):
    from_company_id: str
    to_company_id: str
    ownership_percentage: float = Field(ge=0, le=100)
    effective_date: Optional[date] = None
    source: str = ""


class OwnershipGraph(BaseModel):
    nodes: list[Company] = Field(default_factory=list)
    edges: list[OwnershipEdge] = Field(default_factory=list)
