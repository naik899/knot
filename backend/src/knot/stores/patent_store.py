"""In-memory patent store simulating MongoDB."""

from typing import Optional
from knot.models.patent import Patent


class PatentStore:
    def __init__(self):
        self._patents: dict[str, Patent] = {}

    def add(self, patent: Patent) -> None:
        self._patents[patent.id] = patent

    def get(self, patent_id: str) -> Optional[Patent]:
        return self._patents.get(patent_id)

    def get_all(self) -> list[Patent]:
        return list(self._patents.values())

    def search(self, query: str, jurisdictions: list[str] | None = None) -> list[Patent]:
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        results = []
        for patent in self._patents.values():
            # Check title and abstract
            text = f"{patent.title} {patent.abstract}".lower()
            patent_kw = set(patent.keywords)
            if query_terms & set(text.split()) or query_terms & patent_kw:
                if jurisdictions:
                    if any(j in patent.jurisdictions for j in jurisdictions):
                        results.append(patent)
                else:
                    results.append(patent)
        return results

    def search_by_keywords(self, keywords: list[str], jurisdictions: list[str] | None = None) -> list[Patent]:
        kw_set = set(k.lower() for k in keywords)
        results = []
        for patent in self._patents.values():
            patent_kw = set(k.lower() for k in patent.keywords)
            overlap = kw_set & patent_kw
            if overlap:
                if jurisdictions:
                    if any(j in patent.jurisdictions for j in jurisdictions):
                        results.append(patent)
                else:
                    results.append(patent)
        return results

    def search_by_classification(self, code_prefix: str) -> list[Patent]:
        results = []
        for patent in self._patents.values():
            for cls in patent.classifications:
                if cls.code.startswith(code_prefix):
                    results.append(patent)
                    break
        return results

    def get_by_assignee(self, assignee: str) -> list[Patent]:
        assignee_lower = assignee.lower()
        return [p for p in self._patents.values() if any(assignee_lower in a.lower() for a in p.assignees)]

    def count(self) -> int:
        return len(self._patents)
