"""In-memory search store for products and prior art."""

from typing import Optional
from knot.models.product import ProductInfo, ProductMatch
from knot.models.validity import PriorArtCandidate


class SearchStore:
    def __init__(self):
        self._products: dict[str, ProductInfo] = {}
        self._product_matches: list[ProductMatch] = []
        self._prior_art: dict[str, PriorArtCandidate] = {}

    # Product methods
    def add_product(self, product: ProductInfo) -> None:
        self._products[product.id] = product

    def get_product(self, product_id: str) -> Optional[ProductInfo]:
        return self._products.get(product_id)

    def get_all_products(self) -> list[ProductInfo]:
        return list(self._products.values())

    def search_products(self, query: str) -> list[ProductInfo]:
        query_lower = query.lower()
        terms = set(query_lower.split())
        results = []
        for product in self._products.values():
            text = f"{product.name} {product.description} {product.manufacturer}".lower()
            if terms & set(text.split()):
                results.append(product)
        return results

    # Product match methods
    def add_product_match(self, match: ProductMatch) -> None:
        self._product_matches.append(match)

    def get_matches_for_patent(self, patent_id: str) -> list[ProductMatch]:
        return [m for m in self._product_matches if m.patent_id == patent_id]

    def get_all_matches(self) -> list[ProductMatch]:
        return list(self._product_matches)

    # Prior art methods
    def add_prior_art(self, prior_art: PriorArtCandidate) -> None:
        self._prior_art[prior_art.id] = prior_art

    def get_prior_art(self, prior_art_id: str) -> Optional[PriorArtCandidate]:
        return self._prior_art.get(prior_art_id)

    def get_all_prior_art(self) -> list[PriorArtCandidate]:
        return list(self._prior_art.values())

    def search_prior_art(self, keywords: list[str]) -> list[PriorArtCandidate]:
        kw_set = set(k.lower() for k in keywords)
        results = []
        for pa in self._prior_art.values():
            pa_kw = set(k.lower() for k in pa.keywords)
            pa_text = set(pa.title.lower().split()) | set(pa.relevant_text.lower().split())
            if kw_set & (pa_kw | pa_text):
                results.append(pa)
        return results
