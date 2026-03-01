"""Dependency injection for stores and agents."""

import logging

from knot.config import settings
from knot.stores.patent_store import PatentStore
from knot.stores.graph_store import GraphStore
from knot.stores.search_store import SearchStore
from knot.services.llm_service import LLMService
from knot.agents.data_custodian import DataCustodianAgent
from knot.agents.corporate_intel import CorporateIntelAgent
from knot.agents.market_analyst import MarketAnalystAgent
from knot.agents.scraper import ScraperAgent
from knot.agents.integration import IntegrationAgent
from knot.agents.landscaping import LandscapingAgent
from knot.agents.fto_analyst import FTOAnalystAgent
from knot.agents.validity_researcher import ValidityResearcherAgent
from knot.agents.router import RouterAgent

logger = logging.getLogger(__name__)


class Container:
    """Simple dependency injection container."""

    def __init__(self):
        # Services
        self.llm_service = LLMService(settings)

        # Stores
        self.patent_store = PatentStore()
        self.graph_store = GraphStore()
        self.search_store = SearchStore()

        # Agents
        self.data_custodian = DataCustodianAgent(self.patent_store)
        self.scraper = ScraperAgent(self.patent_store)
        self.integration = IntegrationAgent(self.patent_store)
        self.corporate_intel = CorporateIntelAgent(self.graph_store, self.patent_store)
        self.market_analyst = MarketAnalystAgent(self.patent_store, self.search_store, llm_service=self.llm_service)
        self.landscaping = LandscapingAgent(self.patent_store, llm_service=self.llm_service)
        self.fto_analyst = FTOAnalystAgent(self.patent_store, llm_service=self.llm_service)
        self.validity_researcher = ValidityResearcherAgent(self.patent_store, self.search_store, llm_service=self.llm_service)

        # Agents dict (shared by Router and deep agent)
        self._agents_dict = {
            "data_custodian": self.data_custodian,
            "scraper": self.scraper,
            "integration": self.integration,
            "corporate_intel": self.corporate_intel,
            "market_analyst": self.market_analyst,
            "landscaping": self.landscaping,
            "fto_analyst": self.fto_analyst,
            "validity_researcher": self.validity_researcher,
        }

        # Router with all agents (always available as fallback)
        self.router = RouterAgent(self._agents_dict, llm_service=self.llm_service)

        # Deep agent (None if unavailable)
        self.deep_agent = None
        self.skill_files = None
        self._init_deep_agent()

    def _init_deep_agent(self):
        """Try to build the deep agent orchestrator. Gracefully falls back."""
        try:
            from knot.deepagent.agent_factory import build_deep_agent

            result = build_deep_agent(settings, self._agents_dict)
            if result is not None:
                self.deep_agent, self.skill_files = result
                logger.info("Deep agent initialized successfully")
            else:
                logger.info("Deep agent not available — using RouterAgent")
        except ImportError:
            logger.info("deepagents package not installed — using RouterAgent")
        except Exception:
            logger.exception("Failed to initialize deep agent — using RouterAgent")


# Global container instance
container = Container()


def get_container() -> Container:
    return container
