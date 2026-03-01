"""LangChain @tool wrappers that delegate to existing Knot agents."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from langchain_core.tools import tool

if TYPE_CHECKING:
    from knot.agents.corporate_intel import CorporateIntelAgent
    from knot.agents.data_custodian import DataCustodianAgent
    from knot.agents.fto_analyst import FTOAnalystAgent
    from knot.agents.integration import IntegrationAgent
    from knot.agents.landscaping import LandscapingAgent
    from knot.agents.market_analyst import MarketAnalystAgent
    from knot.agents.scraper import ScraperAgent
    from knot.agents.validity_researcher import ValidityResearcherAgent


# --- FTO tools ---

def make_fto_tools(fto_agent: FTOAnalystAgent) -> list:
    @tool
    def analyze_fto(description: str, target_markets: list[str] | None = None, keywords: list[str] | None = None) -> str:
        """Run a Freedom-to-Operate analysis for a product/technology description.
        Returns patent infringement risk assessment with claim-level matches."""
        result = fto_agent.execute("analyze_fto", {
            "description": description,
            "target_markets": target_markets or [],
            "keywords": keywords or [],
        })
        return json.dumps(result, default=str)

    @tool
    def check_patent_risk(patent_id: str, description: str) -> str:
        """Check infringement risk of a single patent against a product description.
        Returns claim-by-claim risk analysis."""
        result = fto_agent.execute("check_patent", {
            "patent_id": patent_id,
            "description": description,
        })
        return json.dumps(result, default=str)

    return [analyze_fto, check_patent_risk]


# --- Landscape tools ---

def make_landscape_tools(landscaping_agent: LandscapingAgent) -> list:
    @tool
    def analyze_landscape(domain: str, keywords: list[str] | None = None) -> str:
        """Analyze the patent landscape for a technology domain.
        Returns clusters, white spaces, and ranked opportunities."""
        result = landscaping_agent.execute("analyze_landscape", {
            "domain": domain,
            "keywords": keywords or [],
        })
        return json.dumps(result, default=str)

    @tool
    def find_white_spaces(domain: str, keywords: list[str] | None = None) -> str:
        """Identify innovation white spaces in a technology domain.
        Returns gaps and opportunities not covered by existing patents."""
        result = landscaping_agent.execute("find_white_spaces", {
            "domain": domain,
            "keywords": keywords or [],
        })
        return json.dumps(result, default=str)

    return [analyze_landscape, find_white_spaces]


# --- Validity tools ---

def make_validity_tools(validity_agent: ValidityResearcherAgent) -> list:
    @tool
    def find_prior_art(patent_id: str = "", keywords: list[str] | None = None) -> str:
        """Search for prior art relevant to a patent or technology area.
        Returns prior art candidates with relevance scoring."""
        result = validity_agent.execute("find_prior_art", {
            "patent_id": patent_id,
            "keywords": keywords or [],
        })
        return json.dumps(result, default=str)

    @tool
    def validate_patent(patent_id: str, keywords: list[str] | None = None) -> str:
        """Assess patent validity by finding prior art and analyzing claim novelty.
        Returns validity opinion with supporting evidence."""
        result = validity_agent.execute("validate_patent", {
            "patent_id": patent_id,
            "keywords": keywords or [],
        })
        return json.dumps(result, default=str)

    return [find_prior_art, validate_patent]


# --- Market tools ---

def make_market_tools(market_agent: MarketAnalystAgent) -> list:
    @tool
    def match_patent_to_products(description: str, keywords: list[str] | None = None) -> str:
        """Match a product description against patents to find relevant IP.
        Returns ranked patent matches with confidence scores."""
        result = market_agent.execute("match_patent_to_products", {
            "description": description,
            "keywords": keywords or [],
        })
        return json.dumps(result, default=str)

    @tool
    def find_product_matches(patent_id: str) -> str:
        """Find commercial products that may use a specific patent.
        Returns product matches with relevance evidence."""
        result = market_agent.execute("find_product_matches", {
            "patent_id": patent_id,
        })
        return json.dumps(result, default=str)

    return [match_patent_to_products, find_product_matches]


# --- Corporate tools ---

def make_corporate_tools(corporate_agent: CorporateIntelAgent) -> list:
    @tool
    def resolve_parent_company(company_name: str = "", company_id: str = "") -> str:
        """Resolve the ultimate parent company for a given entity.
        Traverses ownership chains to find the top-level parent."""
        result = corporate_agent.execute("resolve_parent", {
            "company_name": company_name,
            "company_id": company_id,
        })
        return json.dumps(result, default=str)

    @tool
    def get_ownership_graph(company_id: str) -> str:
        """Get the full ownership graph for a company.
        Returns nodes (companies) and edges (ownership relationships)."""
        result = corporate_agent.execute("get_graph", {
            "company_id": company_id,
        })
        return json.dumps(result, default=str)

    @tool
    def resolve_assignees(assignee_names: list[str]) -> str:
        """Resolve patent assignee names to canonical company entities.
        Handles variations, abbreviations, and subsidiary relationships."""
        result = corporate_agent.execute("resolve_assignees", {
            "assignee_names": assignee_names,
        })
        return json.dumps(result, default=str)

    return [resolve_parent_company, get_ownership_graph, resolve_assignees]


# --- Search tools ---

def make_search_tools(scraper_agent: ScraperAgent) -> list:
    @tool
    def search_patents(keywords: list[str], jurisdictions: list[str] | None = None) -> str:
        """Search patents by keywords and optional jurisdiction filters.
        Returns matching patents from USPTO, EPO, CGPDTM databases."""
        result = scraper_agent.execute("fetch_patents", {
            "keywords": keywords,
            "jurisdictions": jurisdictions or [],
        })
        return json.dumps(result, default=str)

    return [search_patents]


# --- Data quality tools ---

def make_data_tools(custodian_agent: DataCustodianAgent, integration_agent: IntegrationAgent) -> list:
    @tool
    def normalize_patent(patent_id: str) -> str:
        """Normalize a patent record: clean text, extract keywords, standardize fields.
        Returns the normalized patent data."""
        result = custodian_agent.execute("normalize_patent", {
            "patent_id": patent_id,
        })
        return json.dumps(result, default=str)

    @tool
    def validate_patent_data(patent_id: str) -> str:
        """Validate patent data completeness and consistency.
        Returns validation results with any issues found."""
        result = custodian_agent.execute("validate_patent", {
            "patent_id": patent_id,
        })
        return json.dumps(result, default=str)

    @tool
    def detect_duplicates(patent_id: str) -> str:
        """Detect duplicate patent records in the database.
        Returns potential duplicates with similarity scores."""
        result = integration_agent.execute("detect_duplicates", {
            "patent_id": patent_id,
        })
        return json.dumps(result, default=str)

    return [normalize_patent, validate_patent_data, detect_duplicates]


# --- Aggregator ---

def make_all_tools(agents: dict) -> list:
    """Build all LangChain tools from the agents dict."""
    all_tools = []
    all_tools.extend(make_fto_tools(agents["fto_analyst"]))
    all_tools.extend(make_landscape_tools(agents["landscaping"]))
    all_tools.extend(make_validity_tools(agents["validity_researcher"]))
    all_tools.extend(make_market_tools(agents["market_analyst"]))
    all_tools.extend(make_corporate_tools(agents["corporate_intel"]))
    all_tools.extend(make_search_tools(agents["scraper"]))
    all_tools.extend(make_data_tools(agents["data_custodian"], agents["integration"]))
    return all_tools
