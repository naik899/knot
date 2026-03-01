"""REST API endpoints for Project Knot."""

import logging
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from knot.api.dependencies import Container, get_container
from knot.models.messages import AgentRequest

logger = logging.getLogger(__name__)

router = APIRouter()


# --- Request/Response models ---

class QueryRequest(BaseModel):
    query: str = Field(description="Natural language query about IP intelligence")


class FTORequest(BaseModel):
    description: str = Field(description="Product or technology description")
    target_markets: list[str] = Field(default_factory=list, description="Target market jurisdictions (US, EU, IN, etc.)")
    keywords: list[str] = Field(default_factory=list, description="Optional additional keywords")


class CorporateResolveRequest(BaseModel):
    company_name: str = Field(default="", description="Company name to resolve")
    company_id: str = Field(default="", description="Company ID to resolve")


class LandscapeRequest(BaseModel):
    domain: str = Field(description="Technology domain to analyze")
    keywords: list[str] = Field(default_factory=list, description="Optional domain keywords")


class ValidityRequest(BaseModel):
    patent_id: str = Field(default="", description="Patent ID to validate")
    keywords: list[str] = Field(default_factory=list, description="Keywords for prior art search")


class ProductMatchRequest(BaseModel):
    description: str = Field(description="Product description to match against patents")
    keywords: list[str] = Field(default_factory=list, description="Optional keywords")


# --- Endpoints ---

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    container = get_container()
    return {
        "status": "healthy",
        "version": "0.1.0",
        "stores": {
            "patents": container.patent_store.count(),
            "companies": container.graph_store.count(),
            "products": len(container.search_store.get_all_products()),
            "prior_art": len(container.search_store.get_all_prior_art()),
        },
    }


@router.post("/query")
async def query(request: QueryRequest):
    """Natural language query — deep agent with RouterAgent fallback."""
    container = get_container()

    # Try deep agent first
    if container.deep_agent is not None:
        try:
            thread_id = uuid4().hex
            result = container.deep_agent.invoke(
                {
                    "messages": [{"role": "user", "content": request.query}],
                    "files": container.skill_files or {},
                },
                config={"configurable": {"thread_id": thread_id}},
            )
            from knot.deepagent.response import extract_response

            response = extract_response(result, request.query)
            if response and response.get("executive_summary"):
                return response
            logger.warning("Deep agent returned empty response — falling back to RouterAgent")
        except Exception:
            logger.exception("Deep agent failed — falling back to RouterAgent")

    # Fallback: RouterAgent
    agent_request = AgentRequest(
        source_agent="api",
        target_agent="router",
        task_type="route_query",
        payload={"query": request.query},
    )
    response = container.router.handle_request(agent_request)
    if response.status == "failure":
        raise HTTPException(status_code=500, detail=response.errors)
    return response.result


@router.post("/fto/analyze")
async def fto_analyze(request: FTORequest):
    """Direct FTO analysis."""
    container = get_container()
    agent_request = AgentRequest(
        source_agent="api",
        target_agent="fto_analyst",
        task_type="analyze_fto",
        payload={
            "description": request.description,
            "target_markets": request.target_markets,
            "keywords": request.keywords,
        },
    )
    response = container.fto_analyst.handle_request(agent_request)
    if response.status == "failure":
        raise HTTPException(status_code=500, detail=response.errors)
    return response.result


@router.post("/corporate/resolve")
async def corporate_resolve(request: CorporateResolveRequest):
    """Resolve ultimate parent company."""
    container = get_container()
    agent_request = AgentRequest(
        source_agent="api",
        target_agent="corporate_intel",
        task_type="resolve_parent",
        payload={
            "company_name": request.company_name,
            "company_id": request.company_id,
        },
    )
    response = container.corporate_intel.handle_request(agent_request)
    if response.status == "failure":
        raise HTTPException(status_code=500, detail=response.errors)
    return response.result


@router.get("/corporate/graph/{company_id}")
async def corporate_graph(company_id: str):
    """Get ownership graph for a company."""
    container = get_container()
    agent_request = AgentRequest(
        source_agent="api",
        target_agent="corporate_intel",
        task_type="get_graph",
        payload={"company_id": company_id},
    )
    response = container.corporate_intel.handle_request(agent_request)
    if response.status == "failure":
        raise HTTPException(status_code=500, detail=response.errors)
    return response.result


@router.post("/landscape/analyze")
async def landscape_analyze(request: LandscapeRequest):
    """Technology landscape analysis."""
    container = get_container()
    agent_request = AgentRequest(
        source_agent="api",
        target_agent="landscaping",
        task_type="analyze_landscape",
        payload={
            "domain": request.domain,
            "keywords": request.keywords,
        },
    )
    response = container.landscaping.handle_request(agent_request)
    if response.status == "failure":
        raise HTTPException(status_code=500, detail=response.errors)
    return response.result


@router.post("/validity/prior-art")
async def validity_prior_art(request: ValidityRequest):
    """Find prior art for a patent."""
    container = get_container()
    agent_request = AgentRequest(
        source_agent="api",
        target_agent="validity_researcher",
        task_type="find_prior_art" if request.patent_id else "find_prior_art",
        payload={
            "patent_id": request.patent_id,
            "keywords": request.keywords,
        },
    )
    response = container.validity_researcher.handle_request(agent_request)
    if response.status == "failure":
        raise HTTPException(status_code=500, detail=response.errors)
    return response.result


@router.post("/products/match")
async def products_match(request: ProductMatchRequest):
    """Patent-product linkage."""
    container = get_container()
    agent_request = AgentRequest(
        source_agent="api",
        target_agent="market_analyst",
        task_type="match_patent_to_products",
        payload={
            "description": request.description,
            "keywords": request.keywords,
        },
    )
    response = container.market_analyst.handle_request(agent_request)
    if response.status == "failure":
        raise HTTPException(status_code=500, detail=response.errors)
    return response.result


@router.get("/patents/search")
async def search_patents(
    q: str = Query(default="", description="Search query"),
    jurisdiction: Optional[str] = Query(default=None, description="Filter by jurisdiction"),
):
    """Search patents."""
    container = get_container()
    jurisdictions = [jurisdiction] if jurisdiction else None
    results = container.patent_store.search(q, jurisdictions)
    return {
        "query": q,
        "results": [p.model_dump() for p in results],
        "total": len(results),
    }


@router.get("/patents/{patent_id}")
async def get_patent(patent_id: str):
    """Get a single patent by ID."""
    container = get_container()
    patent = container.patent_store.get(patent_id)
    if not patent:
        raise HTTPException(status_code=404, detail=f"Patent {patent_id} not found")
    return patent.model_dump()
