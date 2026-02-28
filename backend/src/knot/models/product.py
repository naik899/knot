"""Product-related models."""

from typing import Optional

from pydantic import BaseModel, Field


class ProductDescription(BaseModel):
    name: str
    description: str
    features: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    target_markets: list[str] = Field(default_factory=list)


class ProductInfo(BaseModel):
    id: str
    name: str
    manufacturer: str
    description: str = ""
    specifications: dict = Field(default_factory=dict)
    availability: str = Field(default="commercial", description="commercial, prototype, discontinued")
    url: str = ""


class ProductMatch(BaseModel):
    patent_id: str
    product_id: str
    product_name: str
    manufacturer: str = ""
    confidence_score: float = Field(ge=0, le=1)
    matching_claims: list[int] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    matched_keywords: list[str] = Field(default_factory=list)
