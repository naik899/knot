"""Patent-related data models."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Classification(BaseModel):
    system: str = Field(description="Classification system (IPC, CPC, etc.)")
    code: str = Field(description="Classification code")
    description: str = Field(default="", description="Human-readable description")


class Inventor(BaseModel):
    name: str
    country: str = ""


class Claim(BaseModel):
    number: int
    type: str = Field(description="'independent' or 'dependent'")
    depends_on: Optional[int] = None
    text: str
    normalized_text: str = ""


class Patent(BaseModel):
    id: str = Field(description="Internal unique ID")
    source: str = Field(description="USPTO, EPO, or CGPDTM")
    publication_number: str
    title: str
    abstract: str = ""
    claims: list[Claim] = Field(default_factory=list)
    assignees: list[str] = Field(default_factory=list)
    inventors: list[Inventor] = Field(default_factory=list)
    filing_date: Optional[date] = None
    publication_date: Optional[date] = None
    expiry_date: Optional[date] = None
    classifications: list[Classification] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    raw_text: str = ""
    language: str = "en"
    status: str = Field(default="active", description="active, expired, abandoned")
    jurisdictions: list[str] = Field(default_factory=list)
