# Project Knot — System Architecture

## Overview

Project Knot is an **Agentic IP Intelligence Mesh** designed for Indian MSMEs and startups. It uses a multi-agent architecture where specialized agents collaborate to provide patent intelligence, freedom-to-operate analysis, corporate ownership resolution, and technology landscape mapping.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Vue.js)                 │
│        Dashboard │ Query │ FTO │ Corporate │ ...     │
└──────────────────────────┬──────────────────────────┘
                           │ HTTP/JSON
┌──────────────────────────▼──────────────────────────┐
│                  FastAPI REST API                    │
│                   /api/v1/*                          │
├─────────────────────────────────────────────────────┤
│              Dependency Injection Container          │
│         (stores, agents, configuration)              │
├─────────────────────────────────────────────────────┤
│                   Agent Layer                        │
│  ┌──────────────────────────────────────────────┐   │
│  │              RouterAgent (orchestrator)       │   │
│  │     parses intent → plans → executes → synth │   │
│  └──────────┬───────────────────────────────────┘   │
│             │ delegates to                          │
│  ┌──────────▼───────────────────────────────────┐   │
│  │  DataCustodian │ Scraper │ Integration       │   │
│  │  CorporateIntel │ MarketAnalyst              │   │
│  │  Landscaping │ FTOAnalyst │ ValidityResearch  │   │
│  └──────────┬───────────────────────────────────┘   │
│             │ uses                                   │
│  ┌──────────▼───────────────────────────────────┐   │
│  │             Service Layer                     │   │
│  │  text_processing │ similarity │ clustering    │   │
│  │  graph_traversal                              │   │
│  └──────────┬───────────────────────────────────┘   │
│             │ reads/writes                           │
│  ┌──────────▼───────────────────────────────────┐   │
│  │             Store Layer (In-Memory)           │   │
│  │  PatentStore │ GraphStore │ SearchStore        │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Agent Layers

### Layer 1 — Data Agents
Handle data ingestion, normalization, and deduplication:
- **DataCustodianAgent**: OCR simulation, text normalization, patent validation
- **ScraperAgent**: Patent API ingestion with rate limiting
- **IntegrationAgent**: Duplicate detection, conflict resolution across sources

### Layer 2 — Intelligence Agents
Perform analysis and generate insights:
- **CorporateIntelAgent**: Ownership graph resolution, ultimate parent finding
- **MarketAnalystAgent**: Patent-to-product matching
- **LandscapingAgent**: Technology clustering, white space detection
- **FTOAnalystAgent**: Freedom-to-operate risk analysis
- **ValidityResearcherAgent**: Prior art search, novelty assessment

### Layer 3 — Orchestration
- **RouterAgent**: Natural language query parsing, execution planning, multi-agent orchestration, response synthesis

## Data Flow

### Natural Language Query
1. User submits query via API or frontend
2. RouterAgent parses intent (keyword-based NLP)
3. RouterAgent creates execution plan (agent dependency graph)
4. Agents execute in topological order, passing results forward
5. RouterAgent synthesizes all outputs into unified response

### Direct Analysis (e.g., FTO)
1. API endpoint receives structured request
2. Single agent executes with store access
3. Agent returns structured result via AgentResponse

## Communication Protocol

All inter-agent communication uses standardized models:

- **AgentRequest**: `request_id`, `source_agent`, `target_agent`, `task_type`, `payload`, `priority`, `timeout_ms`
- **AgentResponse**: `request_id`, `agent`, `status` (success/partial/failure), `result`, `confidence_score`, `execution_time_ms`, `errors`

## Storage (MVP)

The MVP uses in-memory dict-based stores:
- **PatentStore**: Patent documents with full-text and keyword search
- **GraphStore**: Corporate ownership graph (companies + edges)
- **SearchStore**: Products, product matches, and prior art candidates

Mock data is seeded on application startup.

## Configuration

Pydantic-based settings loaded from environment variables (prefix `KNOT_`):
- Server: host `0.0.0.0`, port `8000`
- API prefix: `/api/v1`
- Rate limiting: 60 requests/minute (simulated)
- Agent timeout: 300,000ms (5 minutes)
