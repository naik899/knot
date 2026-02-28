# Project Knot — API Reference

Base URL: `http://localhost:8000/api/v1`

## Health Check

### `GET /health`
Returns system health and store counts.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "stores": {
    "patents": 10,
    "companies": 5,
    "products": 3
  }
}
```

---

## Query

### `POST /query`
Natural language query routed to the appropriate agents.

**Request:**
```json
{
  "query": "What is the FTO risk for IoT temperature sensors in India?"
}
```

**Response:**
```json
{
  "agent": "router",
  "status": "success",
  "confidence_score": 0.85,
  "execution_time_ms": 150,
  "result": {
    "intent": "fto_analysis",
    "executive_summary": "...",
    "sections": [
      {
        "title": "Patent Search",
        "summary": "Found 5 relevant patents",
        "details": {},
        "recommendations": ["..."]
      }
    ]
  }
}
```

---

## FTO Analysis

### `POST /fto/analyze`
Direct freedom-to-operate analysis.

**Request:**
```json
{
  "product_description": "Wireless IoT temperature sensor for industrial monitoring",
  "target_markets": ["IN", "US"],
  "keywords": ["IoT", "sensor", "temperature"]
}
```

**Response:**
```json
{
  "result": {
    "product_description": "...",
    "target_markets": ["IN", "US"],
    "overall_risk": "medium",
    "high_risk_count": 1,
    "medium_risk_count": 2,
    "low_risk_count": 3,
    "summary": "...",
    "recommendations": ["Design around claim 3 of PAT-001", "..."],
    "analyses": [
      {
        "patent_id": "PAT-001",
        "patent_title": "IoT Sensor Network",
        "overall_risk": "high",
        "claim_matches": [
          {
            "patent_id": "PAT-001",
            "claim_number": 1,
            "claim_text": "...",
            "similarity_score": 0.45,
            "risk_level": "high",
            "matched_keywords": ["sensor", "temperature"]
          }
        ]
      }
    ]
  }
}
```

---

## Corporate Intelligence

### `POST /corporate/resolve`
Resolve a company's ultimate parent and subsidiary structure.

**Request:**
```json
{
  "company_name": "Nest Labs"
}
```

**Response:**
```json
{
  "result": {
    "ultimate_parent_id": "COMP-001",
    "ultimate_parent_name": "Alphabet Inc.",
    "subsidiary_count": 3,
    "total_patents": 15
  }
}
```

### `GET /corporate/graph/{company_id}`
Get the full ownership graph for a company.

**Response:**
```json
{
  "result": {
    "nodes": [
      {
        "id": "COMP-001",
        "canonical_name": "Alphabet Inc.",
        "company_type": "corporation",
        "jurisdiction": "US",
        "patent_ids": ["PAT-001"]
      }
    ],
    "edges": [
      {
        "from_company_id": "COMP-001",
        "to_company_id": "COMP-002",
        "ownership_percentage": 100
      }
    ]
  }
}
```

---

## Landscape Analysis

### `POST /landscape/analyze`
Analyze a technology domain's patent landscape.

**Request:**
```json
{
  "domain": "IoT sensors",
  "keywords": ["temperature", "humidity", "wireless"]
}
```

**Response:**
```json
{
  "result": {
    "domain": "IoT sensors",
    "total_patents_analyzed": 10,
    "summary": "...",
    "clusters": [
      {
        "id": "cluster-1",
        "label": "Temperature Sensing",
        "keywords": ["temperature", "sensor", "thermal"],
        "patent_ids": ["PAT-001", "PAT-003"],
        "density": 0.7
      }
    ],
    "white_spaces": [
      {
        "id": "ws-1",
        "description": "Uncovered area in humidity-wireless intersection",
        "opportunity_score": 0.8,
        "suggested_keywords": ["humidity", "wireless"],
        "adjacent_clusters": ["cluster-1"]
      }
    ],
    "opportunities": [
      {
        "rank": 1,
        "white_space": { "...": "..." },
        "rationale": "Low competition with high market potential",
        "competitive_intensity": "low"
      }
    ]
  }
}
```

---

## Prior Art / Validity

### `POST /validity/prior-art`
Search for prior art against a patent.

**Request:**
```json
{
  "patent_id": "PAT-001",
  "keywords": ["sensor", "temperature"]
}
```

**Response:**
```json
{
  "result": {
    "target_patent_id": "PAT-001",
    "overall_validity": "questionable",
    "summary": "Found prior art with moderate relevance",
    "strongest_prior_art": "PA-002",
    "prior_art_results": [
      {
        "prior_art_id": "PA-002",
        "target_patent_id": "PAT-001",
        "relevance_score": 0.45,
        "matched_keywords": ["sensor", "temperature"],
        "analysis": "Shares key concepts..."
      }
    ]
  }
}
```

---

## Product Matching

### `POST /products/match`
Match a product description to relevant patents.

**Request:**
```json
{
  "product_description": "Smart thermostat with wireless connectivity",
  "keywords": ["thermostat", "wireless", "smart"]
}
```

**Response:**
```json
{
  "result": {
    "matches": [
      {
        "patent_id": "PAT-003",
        "product_name": "Smart Thermostat",
        "confidence_score": 0.6,
        "matched_keywords": ["wireless", "smart"]
      }
    ]
  }
}
```

---

## Patents

### `GET /patents/search`
Search patents by keyword and optional jurisdiction filter.

**Query Parameters:**
- `q` (string, required): Search query
- `jurisdictions` (string, optional): Comma-separated jurisdiction codes

**Example:** `GET /patents/search?q=sensor&jurisdictions=IN,US`

**Response:**
```json
{
  "result": {
    "patents": [
      {
        "id": "PAT-001",
        "title": "IoT Sensor Network",
        "source": "USPTO",
        "publication_number": "US-2023-001",
        "abstract": "...",
        "status": "active",
        "keywords": ["sensor", "IoT"],
        "filing_date": "2020-01-15"
      }
    ]
  }
}
```

### `GET /patents/{patent_id}`
Get a single patent by ID.

**Response:** Full patent object including claims, classifications, inventors, and assignees.

---

## Error Responses

All endpoints return HTTP 500 on internal errors:
```json
{
  "detail": "Error description message"
}
```
