"""Extract structured responses from deep agent message history."""

from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)


def extract_response(result: dict, query: str) -> dict:
    """Walk the deep agent's message history and build a response dict.

    Matches the existing /query response shape from RouterAgent._synthesize().

    Returns:
        dict with: query, executive_summary, sections, agent_results,
        confidence_score, orchestration
    """
    messages = result.get("messages", [])
    if not messages:
        return {}

    executive_summary = ""
    agent_results: dict = {}

    for msg in reversed(messages):
        msg_type = type(msg).__name__

        if msg_type == "AIMessage" and not executive_summary:
            content = msg.content if hasattr(msg, "content") else ""
            if isinstance(content, str) and content.strip():
                executive_summary = content.strip()

        if msg_type == "ToolMessage":
            content = msg.content if hasattr(msg, "content") else ""
            tool_name = getattr(msg, "name", "") or ""
            if content and tool_name and tool_name not in agent_results:
                try:
                    parsed = json.loads(content) if isinstance(content, str) else content
                    agent_results[tool_name] = parsed
                except (json.JSONDecodeError, TypeError):
                    agent_results[tool_name] = {"raw": content}

    sections = _build_sections(agent_results)

    return {
        "query": query,
        "executive_summary": executive_summary,
        "sections": sections,
        "agent_results": agent_results,
        "confidence_score": _estimate_confidence(agent_results),
        "orchestration": "deep_agent",
    }


def _build_sections(agent_results: dict) -> list[dict]:
    """Build display sections from agent tool results."""
    sections = []

    section_map = {
        "analyze_fto": ("FTO Risk Analysis", "fto"),
        "check_patent_risk": ("Patent Risk Detail", "fto"),
        "analyze_landscape": ("Landscape Analysis", "landscape"),
        "find_white_spaces": ("White Space Opportunities", "landscape"),
        "find_prior_art": ("Prior Art Search", "validity"),
        "validate_patent": ("Validity Assessment", "validity"),
        "match_patent_to_products": ("Patent-Product Matches", "market"),
        "find_product_matches": ("Product Matches", "market"),
        "resolve_parent_company": ("Corporate Ownership", "corporate"),
        "get_ownership_graph": ("Ownership Graph", "corporate"),
        "resolve_assignees": ("Assignee Resolution", "corporate"),
        "search_patents": ("Patent Search Results", "search"),
    }

    for tool_name, data in agent_results.items():
        if tool_name in section_map:
            title, category = section_map[tool_name]
            sections.append({
                "title": title,
                "category": category,
                "data": data,
            })

    return sections


def _estimate_confidence(agent_results: dict) -> float:
    """Estimate overall confidence from agent results."""
    if not agent_results:
        return 0.0

    scores = []
    for data in agent_results.values():
        if isinstance(data, dict):
            score = data.get("confidence_score")
            if isinstance(score, (int, float)):
                scores.append(float(score))

    return sum(scores) / len(scores) if scores else 0.5
