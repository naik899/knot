"""Factory for building the deep agent orchestrator."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from knot.config import Settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are the Knot orchestrator — an IP intelligence system for Indian MSMEs and startups.

You have access to domain subagents via the `task` tool and direct tools for patent search and data quality. Use write_todos to plan multi-step analyses before executing.

Capabilities:
- FTO (Freedom-to-Operate) risk analysis
- Patent landscape mapping and white space identification
- Patent validity research and prior art search
- Patent-product matching for commercial applications
- Corporate ownership resolution and assignee mapping
- Patent search across USPTO, EPO, and CGPDTM databases
- Data normalization, validation, and deduplication

When handling a query:
1. Use write_todos to create a plan of action.
2. Delegate domain work to the appropriate subagent via the task tool.
3. Use search_patents and data quality tools directly when needed.
4. Synthesize results from subagents into a coherent executive summary.

Always provide structured, actionable responses with clear risk levels and recommendations.\
"""


def build_deep_agent(
    settings: Settings,
    agents: dict,
) -> tuple | None:
    """Build the deep agent orchestrator.

    Returns (compiled_graph, skill_files) or None if unavailable.
    Lazy-imports deepagents so the app starts even without the package.
    """
    if not settings.deepagent_enabled:
        logger.info("Deep agent disabled via settings")
        return None

    try:
        from deepagents import create_deep_agent
        from langchain_openai import AzureChatOpenAI
        from langgraph.checkpoint.memory import MemorySaver
    except ImportError:
        logger.warning("deepagents/langchain-openai not installed — deep agent unavailable")
        return None

    if not settings.azure_openai_endpoint or not settings.azure_openai_api_key:
        logger.warning("Azure OpenAI credentials not configured — deep agent unavailable")
        return None

    try:
        from knot.deepagent.skill_loader import load_skill_files
        from knot.deepagent.subagents import build_subagents
        from knot.deepagent.tools import make_data_tools, make_search_tools

        model = AzureChatOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_deployment=settings.azure_openai_chat_deployment,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

        main_tools = (
            make_search_tools(agents["scraper"])
            + make_data_tools(agents["data_custodian"], agents["integration"])
        )

        subagent_configs = build_subagents(agents)
        skill_files = load_skill_files()
        checkpointer = MemorySaver()

        agent = create_deep_agent(
            model=model,
            tools=main_tools,
            system_prompt=SYSTEM_PROMPT,
            subagents=subagent_configs,
            skills=["/skills/"],
            checkpointer=checkpointer,
            name="knot-orchestrator",
        )

        logger.info("Deep agent built successfully with %d subagents", len(subagent_configs))
        return (agent, skill_files)

    except Exception:
        logger.exception("Failed to build deep agent")
        return None
