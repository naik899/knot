"""BFS graph traversal for corporate ownership resolution."""

from knot.stores.graph_store import GraphStore


def find_ultimate_parent(graph_store: GraphStore, company_id: str) -> str:
    """Find the ultimate parent company using BFS traversal.

    Returns the company_id of the ultimate parent.
    Handles cycles by tracking visited nodes.
    """
    visited = set()
    current = company_id

    while True:
        if current in visited:
            # Cycle detected, return current as the root
            return current
        visited.add(current)

        # Find parent edges (where this company is the child)
        parent_edges = graph_store.get_parent_edges(current)
        if not parent_edges:
            # No parent found, this is the ultimate parent
            return current

        # Follow the ownership edge to the parent
        # Pick the edge with highest ownership percentage
        best_edge = max(parent_edges, key=lambda e: e.ownership_percentage)
        current = best_edge.from_company_id


def get_all_subsidiaries(graph_store: GraphStore, company_id: str) -> list[str]:
    """Get all subsidiaries (direct and indirect) using BFS."""
    visited = set()
    result = []
    queue = [company_id]

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        sub_edges = graph_store.get_subsidiary_edges(current)
        for edge in sub_edges:
            child = edge.to_company_id
            if child not in visited:
                result.append(child)
                queue.append(child)

    return result


def detect_cycles(graph_store: GraphStore) -> list[list[str]]:
    """Detect cycles in the ownership graph."""
    all_companies = graph_store.get_all_companies()
    cycles = []

    for company in all_companies:
        visited = set()
        path = []
        current = company.id

        while current and current not in visited:
            visited.add(current)
            path.append(current)
            parent_edges = graph_store.get_parent_edges(current)
            if parent_edges:
                current = parent_edges[0].from_company_id
            else:
                current = None

        if current and current in visited:
            # Found a cycle
            cycle_start = path.index(current)
            cycle = path[cycle_start:]
            # Normalize cycle to avoid duplicates
            if sorted(cycle) not in [sorted(c) for c in cycles]:
                cycles.append(cycle)

    return cycles


def resolve_assignee_to_company(graph_store: GraphStore, assignee_name: str) -> dict:
    """Resolve a patent assignee name to company info with ultimate parent."""
    company = graph_store.find_company_by_name(assignee_name)
    if not company:
        return {
            "resolved": False,
            "assignee": assignee_name,
            "company_id": None,
            "ultimate_parent_id": None,
            "ultimate_parent_name": None,
        }

    ultimate_parent_id = find_ultimate_parent(graph_store, company.id)
    ultimate_parent = graph_store.get_company(ultimate_parent_id)

    return {
        "resolved": True,
        "assignee": assignee_name,
        "company_id": company.id,
        "company_name": company.canonical_name,
        "company_type": company.company_type,
        "ultimate_parent_id": ultimate_parent_id,
        "ultimate_parent_name": ultimate_parent.canonical_name if ultimate_parent else None,
    }
