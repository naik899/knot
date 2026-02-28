"""Dependency injection for stores and agents."""

from knot.stores.patent_store import PatentStore
from knot.stores.graph_store import GraphStore
from knot.stores.search_store import SearchStore
from knot.agents.data_custodian import DataCustodianAgent
from knot.agents.corporate_intel import CorporateIntelAgent
from knot.agents.market_analyst import MarketAnalystAgent
from knot.agents.scraper import ScraperAgent
from knot.agents.integration import IntegrationAgent
from knot.agents.landscaping import LandscapingAgent
from knot.agents.fto_analyst import FTOAnalystAgent
from knot.agents.validity_researcher import ValidityResearcherAgent
from knot.agents.router import RouterAgent


class Container:
    """Simple dependency injection container."""

    def __init__(self):
        # Stores
        self.patent_store = PatentStore()
        self.graph_store = GraphStore()
        self.search_store = SearchStore()

        # Agents
        self.data_custodian = DataCustodianAgent(self.patent_store)
        self.scraper = ScraperAgent(self.patent_store)
        self.integration = IntegrationAgent(self.patent_store)
        self.corporate_intel = CorporateIntelAgent(self.graph_store, self.patent_store)
        self.market_analyst = MarketAnalystAgent(self.patent_store, self.search_store)
        self.landscaping = LandscapingAgent(self.patent_store)
        self.fto_analyst = FTOAnalystAgent(self.patent_store)
        self.validity_researcher = ValidityResearcherAgent(self.patent_store, self.search_store)

        # Router with all agents
        self.router = RouterAgent({
            "data_custodian": self.data_custodian,
            "scraper": self.scraper,
            "integration": self.integration,
            "corporate_intel": self.corporate_intel,
            "market_analyst": self.market_analyst,
            "landscaping": self.landscaping,
            "fto_analyst": self.fto_analyst,
            "validity_researcher": self.validity_researcher,
        })


# Global container instance
container = Container()


def get_container() -> Container:
    return container
