"""Agent 1: Data Custodian - OCR/normalization and field validation."""

from knot.agents.base import BaseAgent
from knot.models.patent import Patent, Claim
from knot.services.text_processing import normalize_text, extract_keywords, simulate_ocr, detect_language
from knot.stores.patent_store import PatentStore


class DataCustodianAgent(BaseAgent):
    agent_name = "data_custodian"

    def __init__(self, patent_store: PatentStore):
        self.patent_store = patent_store

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "normalize_patent":
            return self._normalize_patent(payload)
        elif task_type == "validate_patent":
            return self._validate_patent(payload)
        elif task_type == "process_text":
            return self._process_text(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _normalize_patent(self, payload: dict) -> dict:
        patent_id = payload.get("patent_id")
        patent = self.patent_store.get(patent_id)
        if not patent:
            raise ValueError(f"Patent {patent_id} not found")

        # Normalize text fields
        normalized_title = normalize_text(patent.title)
        normalized_abstract = normalize_text(patent.abstract)

        # Normalize claims
        normalized_claims = []
        for claim in patent.claims:
            normalized_claims.append(Claim(
                number=claim.number,
                type=claim.type,
                depends_on=claim.depends_on,
                text=claim.text,
                normalized_text=normalize_text(claim.text),
            ))

        # Extract keywords if not present
        all_text = f"{patent.title} {patent.abstract} " + " ".join(c.text for c in patent.claims)
        keywords = patent.keywords or extract_keywords(all_text)

        # Detect language
        language = detect_language(patent.raw_text or patent.abstract)

        return {
            "patent_id": patent_id,
            "normalized_title": normalized_title,
            "normalized_abstract": normalized_abstract,
            "normalized_claims": [c.model_dump() for c in normalized_claims],
            "keywords": keywords,
            "language": language,
            "confidence_score": 0.95,
        }

    def _validate_patent(self, payload: dict) -> dict:
        patent_id = payload.get("patent_id")
        patent = self.patent_store.get(patent_id)
        if not patent:
            raise ValueError(f"Patent {patent_id} not found")

        errors = []
        warnings = []

        if not patent.title:
            errors.append("Missing title")
        if not patent.abstract:
            warnings.append("Missing abstract")
        if not patent.claims:
            errors.append("Missing claims")
        if not patent.assignees:
            warnings.append("Missing assignees")
        if not patent.publication_number:
            errors.append("Missing publication number")
        if not patent.filing_date:
            warnings.append("Missing filing date")
        if not patent.source:
            errors.append("Missing source")

        is_valid = len(errors) == 0

        return {
            "patent_id": patent_id,
            "is_valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "confidence_score": 1.0 if is_valid else 0.5,
        }

    def _process_text(self, payload: dict) -> dict:
        raw_text = payload.get("text", "")
        processed = simulate_ocr(raw_text)
        keywords = extract_keywords(processed)
        language = detect_language(raw_text)

        return {
            "processed_text": processed,
            "keywords": keywords,
            "language": language,
            "confidence_score": 0.9,
        }
