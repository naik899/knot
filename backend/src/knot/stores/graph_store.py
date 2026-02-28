"""In-memory graph store simulating Neo4j for corporate ownership."""

from typing import Optional
from knot.models.company import Company, OwnershipEdge, OwnershipGraph


class GraphStore:
    def __init__(self):
        self._companies: dict[str, Company] = {}
        self._edges: list[OwnershipEdge] = []
        self._alias_index: dict[str, str] = {}  # alias_lower -> company_id

    def add_company(self, company: Company) -> None:
        self._companies[company.id] = company
        self._alias_index[company.canonical_name.lower()] = company.id
        for alias in company.aliases:
            self._alias_index[alias.lower()] = company.id

    def add_edge(self, edge: OwnershipEdge) -> None:
        self._edges.append(edge)

    def get_company(self, company_id: str) -> Optional[Company]:
        return self._companies.get(company_id)

    def get_all_companies(self) -> list[Company]:
        return list(self._companies.values())

    def find_company_by_name(self, name: str) -> Optional[Company]:
        company_id = self._alias_index.get(name.lower())
        if company_id:
            return self._companies.get(company_id)
        # Fuzzy match
        name_lower = name.lower()
        for alias, cid in self._alias_index.items():
            if name_lower in alias or alias in name_lower:
                return self._companies.get(cid)
        return None

    def get_parent_edges(self, company_id: str) -> list[OwnershipEdge]:
        """Get edges where this company is owned by another (to_company_id == company_id)."""
        return [e for e in self._edges if e.to_company_id == company_id]

    def get_subsidiary_edges(self, company_id: str) -> list[OwnershipEdge]:
        """Get edges where this company owns another (from_company_id == company_id)."""
        return [e for e in self._edges if e.from_company_id == company_id]

    def get_ownership_graph(self, company_id: str) -> OwnershipGraph:
        """Build the full ownership graph around a company."""
        visited = set()
        nodes = []
        edges = []
        queue = [company_id]
        while queue:
            cid = queue.pop(0)
            if cid in visited:
                continue
            visited.add(cid)
            company = self._companies.get(cid)
            if company:
                nodes.append(company)
            for edge in self._edges:
                if edge.from_company_id == cid and edge.to_company_id not in visited:
                    edges.append(edge)
                    queue.append(edge.to_company_id)
                if edge.to_company_id == cid and edge.from_company_id not in visited:
                    edges.append(edge)
                    queue.append(edge.from_company_id)
        return OwnershipGraph(nodes=nodes, edges=edges)

    def count(self) -> int:
        return len(self._companies)
