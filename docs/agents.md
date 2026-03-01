# Project Knot — Agent Reference

All agents extend `BaseAgent` and implement `execute(task_type, payload)`. Communication uses standardized `AgentRequest`/`AgentResponse` models.

---

## 1. RouterAgent (Orchestrator)

**Purpose:** Parse natural language queries, plan execution, orchestrate other agents, and synthesize unified responses.

**Task Types:**
- `route_query` — Full orchestration pipeline: parse → plan → execute → synthesize
- `parse_query` — Parse intent only (returns intent + execution plan)

**Intent Detection (keyword-based):**
| Intent | Trigger Keywords |
|--------|-----------------|
| `fto_analysis` | fto, infringement, risk, commercialize |
| `landscape` | landscape, white space, opportunity, gap |
| `validity` | prior art, validity, challenge, novel |
| `corporate_intel` | parent company, ownership, subsidiary |
| `product_match` | product, match, commercial |
| `patent_search` | (default fallback) |

**Entity Extraction:** Technologies (IoT, sensors, blockchain, ML, etc.), patent numbers (US/EP/IN patterns), company names, products.

**Constraint Extraction:** Jurisdictions (US, EU, IN, CN, JP).

**Dependencies:** All other agents.

---

## 2. DataCustodianAgent

**Purpose:** OCR simulation, text normalization, field validation for patent data.

**Task Types:**
- `normalize_patent` — Normalize text fields, extract keywords, detect language
- `validate_patent` — Check required fields, return errors/warnings
- `process_text` — Simulate OCR, extract keywords

**Dependencies:** PatentStore, text_processing service.

---

## 3. ScraperAgent

**Purpose:** Patent API ingestion with simulated rate limiting.

**Task Types:**
- `fetch_patents` — Search patents by keywords/jurisdictions (rate limit: 10 requests)
- `fetch_by_source` — Fetch from specific source (USPTO/EPO/CGPDTM)
- `check_status` — Returns operational status and rate limit info

**Dependencies:** PatentStore.

---

## 4. IntegrationAgent

**Purpose:** Data unification, duplicate detection, conflict resolution across patent sources.

**Task Types:**
- `detect_duplicates` — Find duplicate patents by title similarity and keyword overlap
- `unify_records` — Merge multiple patent records, select canonical version
- `resolve_conflict` — Resolve field conflicts (priority: USPTO > EPO > CGPDTM)

**Dependencies:** PatentStore, similarity service, text_processing service.

---

## 5. CorporateIntelAgent

**Purpose:** Corporate ownership resolution, ultimate parent finding, subsidiary tracking.

**Task Types:**
- `resolve_parent` — Find ultimate parent and all subsidiaries for a company
- `get_graph` — Return full ownership graph (nodes + edges) for visualization
- `resolve_assignees` — Batch resolve assignee names to companies

**Output:** ultimate_parent_id, ultimate_parent_name, subsidiary_count, total_patents.

**Dependencies:** GraphStore, PatentStore, graph_traversal service.

---

## 6. MarketAnalystAgent

**Purpose:** Patent-to-product linking via keyword matching.

**Task Types:**
- `find_product_matches` — Find products matching a patent's keywords
- `match_patent_to_products` — Match product description to patents, return ranked list with similarity scores

**Dependencies:** PatentStore, SearchStore, similarity service.

---

## 7. LandscapingAgent

**Purpose:** Patent clustering, white space detection, innovation opportunity identification.

**Task Types:**
- `analyze_landscape` — Full landscape analysis returning clusters, white spaces, and ranked opportunities
- `find_white_spaces` — Detect gaps in patent coverage

**Key Output:** `LandscapeReport` with clusters (grouped by IPC/CPC classification + keywords), white spaces (uncovered areas), and `RankedOpportunity` with competitive intensity (low/medium/high).

**Dependencies:** PatentStore, clustering service.

---

## 8. FTOAnalystAgent

**Purpose:** Freedom-to-operate risk analysis with claim-by-claim matching.

**Task Types:**
- `analyze_fto` — Full risk analysis for a product/technology
  - Searches patents by keywords + target markets
  - Filters expired patents
  - Claim-by-claim similarity analysis
  - Risk classification: high (>=0.3), medium (>=0.15), low (<0.15)
- `check_patent` — Single patent analysis against a description

**Output:** `FTOReport` with risk counts, recommendations, and sorted analyses (highest risk first).

**Dependencies:** PatentStore, similarity service.

---

## 9. ValidityResearcherAgent

**Purpose:** Prior art search and patent novelty assessment.

**Task Types:**
- `find_prior_art` — Search prior art using keyword matching (filters by publication date < filing date)
- `validate_patent` — Full novelty assessment
  - `appears_valid`: no strong prior art
  - `questionable`: moderate relevance prior art found
  - `likely_invalid`: relevance > 0.5

**Dependencies:** PatentStore, SearchStore, similarity service.

---

## Agent Lifecycle

Every agent call follows this lifecycle (implemented in `BaseAgent.handle_request`):

1. Record start time
2. Call `execute(task_type, payload)`
3. Catch any exceptions
4. Return `AgentResponse` with:
   - `execution_time_ms`
   - `confidence_score` (0.0–1.0)
   - `status` (success/partial/failure)
   - `errors` list
