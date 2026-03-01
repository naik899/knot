"""Subagent configurations for the deep agent orchestrator."""

from __future__ import annotations

from knot.deepagent.tools import (
    make_corporate_tools,
    make_fto_tools,
    make_landscape_tools,
    make_market_tools,
    make_search_tools,
    make_validity_tools,
)


def build_subagents(agents: dict) -> list[dict]:
    """Build 5 domain subagent configurations.

    Each subagent gets a focused tool set and its own skills path prefix.
    Custom subagents do NOT auto-inherit the main agent's skills.
    """
    fto_tools = make_fto_tools(agents["fto_analyst"])
    search_tools = make_search_tools(agents["scraper"])
    corporate_tools = make_corporate_tools(agents["corporate_intel"])
    validity_tools = make_validity_tools(agents["validity_researcher"])
    landscape_tools = make_landscape_tools(agents["landscaping"])
    market_tools = make_market_tools(agents["market_analyst"])

    return [
        {
            "name": "fto-analyst",
            "description": "Performs Freedom-to-Operate analysis including patent search, claim matching, risk assessment, and assignee resolution.",
            "system_prompt": (
                "You are an FTO analyst. Your job is to assess patent infringement risk.\n"
                "Steps:\n"
                "1. Use search_patents to find relevant patents for the described technology.\n"
                "2. Use analyze_fto to perform claim-by-claim risk analysis.\n"
                "3. For high-risk patents, use check_patent_risk for detailed analysis.\n"
                "4. Use resolve_assignees to identify patent owners.\n"
                "5. Optionally use find_prior_art if invalidation may reduce risk.\n"
                "6. Return a structured JSON with overall_risk, analyses, and recommendations."
            ),
            "tools": fto_tools + search_tools + [corporate_tools[2]] + [validity_tools[0]],
            "skills": ["/skills/fto/"],
        },
        {
            "name": "landscape-analyst",
            "description": "Analyzes patent landscapes to identify clusters, white spaces, and innovation opportunities in a technology domain.",
            "system_prompt": (
                "You are a landscape analyst. Your job is to map patent landscapes.\n"
                "Steps:\n"
                "1. Use analyze_landscape to cluster patents in the domain.\n"
                "2. Use find_white_spaces to identify innovation gaps.\n"
                "3. Synthesize clusters and white spaces into strategic recommendations.\n"
                "4. Return a structured JSON with clusters, white_spaces, opportunities, and summary."
            ),
            "tools": landscape_tools,
            "skills": ["/skills/landscape/"],
        },
        {
            "name": "validity-researcher",
            "description": "Researches patent validity by finding prior art and assessing claim novelty and obviousness.",
            "system_prompt": (
                "You are a validity researcher. Your job is to assess patent validity.\n"
                "Steps:\n"
                "1. Use find_prior_art to search for anticipating references.\n"
                "2. Use validate_patent for comprehensive validity assessment.\n"
                "3. Evaluate the impact of prior art on specific claims.\n"
                "4. Return a structured JSON with prior_art_results, overall_validity, and summary."
            ),
            "tools": validity_tools,
            "skills": ["/skills/validity/"],
        },
        {
            "name": "market-analyst",
            "description": "Matches patents to commercial products and identifies licensing or infringement opportunities.",
            "system_prompt": (
                "You are a market analyst. Your job is to connect patents to products.\n"
                "Steps:\n"
                "1. Use match_patent_to_products to find patents relevant to a product description.\n"
                "2. Use find_product_matches to find products using a specific patent.\n"
                "3. Rank matches by confidence and highlight evidence.\n"
                "4. Return a structured JSON with matches, confidence_scores, and evidence."
            ),
            "tools": market_tools,
            "skills": ["/skills/market/"],
        },
        {
            "name": "corporate-intel",
            "description": "Resolves corporate ownership structures, maps assignee networks, and identifies ultimate parent companies.",
            "system_prompt": (
                "You are a corporate intelligence analyst. Your job is to map ownership structures.\n"
                "Steps:\n"
                "1. Use resolve_assignees to map patent assignee names to companies.\n"
                "2. Use resolve_parent_company to find ultimate parent entities.\n"
                "3. Use get_ownership_graph to visualize corporate structures.\n"
                "4. Return a structured JSON with ownership chains and entity relationships."
            ),
            "tools": corporate_tools,
            "skills": ["/skills/corporate/"],
        },
    ]
