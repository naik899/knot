# Project Knot — Demo Guide

## Prerequisites

- Python 3.9+
- Node.js 18+
- `uv` (Python package manager)

## Startup

### 1. Start the Backend

```bash
cd backend
uv sync --all-extras
uv run python -m knot.main
```

The API server starts at `http://localhost:8000`. Mock data (patents, companies, products, prior art) is seeded automatically on startup.

### 2. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI opens at `http://localhost:5173` with API calls proxied to the backend.

---

## Demo Scenario: IoT Temperature Sensor for Indian Market

### Scene 1 — Dashboard Overview

1. Open `http://localhost:5173`
2. The dashboard shows:
   - Patent count, company count, product count from the backend
   - Quick query box
   - Quick links to all analysis tools

### Scene 2 — Natural Language Query

1. Navigate to **Query** (`/query`)
2. Enter: `What is the FTO risk for IoT temperature sensors in India?`
3. The RouterAgent:
   - Detects intent: `fto_analysis`
   - Extracts entities: technology=IoT, sensors, temperature; jurisdiction=IN
   - Plans execution: scraper → fto_analyst → corporate_intel → validity_researcher
   - Executes agents in order
   - Returns synthesized response with sections and recommendations

### Scene 3 — FTO Analysis (Direct)

1. Navigate to **FTO Analysis** (`/fto`)
2. Fill in:
   - **Description**: "Wireless IoT temperature sensor with cloud connectivity for industrial monitoring"
   - **Target Markets**: IN, US
   - **Keywords**: IoT, sensor, temperature, wireless
3. Click **Run FTO Analysis**
4. Review:
   - Overall risk level badge (high/medium/low)
   - Risk count summary (high/medium/low counts)
   - Claim match table showing which patent claims overlap
   - Recommendations for design-around strategies

### Scene 4 — Corporate Intelligence

1. Navigate to **Corporate Intel** (`/corporate`)
2. Enter: `Nest Labs`
3. View:
   - Ultimate parent resolution (e.g., Alphabet Inc.)
   - Subsidiary count and total patents
   - Ownership graph with nodes (companies) and edges (ownership percentages)

### Scene 5 — Landscape Analysis

1. Navigate to **Landscape** (`/landscape`)
2. Enter domain: `IoT sensors`
3. View:
   - Patent clusters grouped by technology area
   - White space opportunities (uncovered technology gaps)
   - Ranked opportunities with competitive intensity

### Scene 6 — Patent Search

1. Navigate to **Patents** (`/patents`)
2. Search: `sensor`
3. Browse patent cards with title, abstract, keywords, status
4. Click a patent to see full detail including all claims

### Scene 7 — Prior Art Search

1. Navigate to **Prior Art** (`/validity`)
2. Enter patent ID: `PAT-001`
3. View:
   - Validity assessment (appears_valid / questionable / likely_invalid)
   - Prior art results with relevance scores
   - Matched keywords and analysis text

---

## Key Talking Points

- **Multi-agent architecture**: 9 specialized agents collaborate, orchestrated by the RouterAgent
- **Natural language interface**: Plain English queries are parsed into structured execution plans
- **Claim-level analysis**: FTO doesn't just find patents — it matches individual claims
- **Corporate transparency**: Resolves shell companies and ownership chains
- **White space detection**: Identifies innovation opportunities by finding gaps in patent coverage
- **Indian MSME focus**: Designed for the Indian patent landscape (CGPDTM integration planned)
