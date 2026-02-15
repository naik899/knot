# Project Knot: Agentic IP Intelligence Mesh

> Untying the complex legal knots of Intellectual Property through AI-powered multi-agent intelligence

## Overview

Project Knot is a decentralized, multi-agent orchestration framework that democratizes Intellectual Property (IP) intelligence for Indian MSMEs and startups. By leveraging Amazon Bedrock's Claude models and a sophisticated 9-agent architecture, Knot provides enterprise-grade patent analysis, Freedom to Operate (FTO) assessments, and corporate intelligence—reducing analysis time from weeks to minutes.

## The Problem

Indian startups and MSMEs face critical IP challenges:

- **Fragmented Data**: Patent information scattered across USPTO, EPO, and India's CGPDTM
- **Hidden Ownership**: Deceptive patent assignees using shell companies and subsidiaries
- **Siloed Context**: R&D teams lack strategic business intelligence about patent landscapes
- **Resource Constraints**: Traditional IP analysis requires expensive legal expertise and weeks of research

## The Solution

Knot uses specialized AI agents to perform high-order reasoning across legal, technical, and commercial datasets:

### 9-Agent Architecture

**Layer 1-2: Data & Sanitization**
- **Agent 1 (Data Custodian)**: Automated OCR, cleaning, and normalization of patent PDFs
- **Agent 4 (Scraper & API Connector)**: Real-time ingestion from USPTO, EPO, CGPDTM APIs and SEC filings
- **Agent 5 (Integration Agent)**: Synchronizes disparate data sources into unified processing stream

**Layer 3: Contextual Enrichment**
- **Agent 2 (Corporate Intelligence)**: Maps assignees to ultimate parent companies using graph analysis
- **Agent 3 (Market Analyst)**: Links patent claims to existing products and market disclosures

**Layer 4: Specialized IP Reasoning**
- **Agent 6 (Landscaping Specialist)**: Identifies "white spaces" for R&D opportunities
- **Agent 7 (FTO Risk Analyst)**: Multi-step Freedom to Operate risk assessment
- **Agent 8 (Validity Researcher)**: Discovers prior art to challenge or verify patent claims

**Layer 5: Cognitive Interface**
- **Agent 9 (Router Agent)**: Central LLM orchestrator that triages queries to specialized sub-agents

## Key Features

### 🎯 Freedom to Operate Analysis
- Identify potentially infringing patents in <10 minutes
- Claim-by-claim analysis with risk levels (high/medium/low)
- Actionable recommendations for mitigation

### 🏢 Corporate Intelligence
- 90%+ accuracy in identifying ultimate parent companies
- Graph-based ownership hierarchy visualization
- M&A event tracking and impact analysis

### 🗺️ Technology Landscape Mapping
- Patent clustering by technical concepts
- White space identification for R&D opportunities
- Competitive intensity analysis

### 🔍 Prior Art Discovery
- Multi-source search (academic publications, standards, earlier patents)
- Automated claim-to-prior-art mapping
- Validity assessment reports

### 🔗 Patent-to-Product Linkage
- Web scraping for commercial product disclosures
- Specification comparison and confidence scoring
- Identify defensive vs. commercialized patents

## Technology Stack

- **LLM Infrastructure**: Amazon Bedrock with Claude 3.7/3.5 Sonnet
- **Development**: Amazon Q Developer for code generation
- **IDE**: Kiro for spec-driven development
- **Databases**: 
  - MongoDB Atlas (patent documents)
  - Amazon Neptune (corporate graphs)
  - Amazon OpenSearch (full-text search)
- **Compute**: AWS Lambda (serverless agent execution)
- **Orchestration**: AWS Step Functions

## Success Metrics

- ✅ **90%+ accuracy** in identifying ultimate parent companies via graph analysis
- ✅ **<10 minute** time-to-insight for FTO searches (down from 2 weeks)
- ✅ **Comprehensive coverage** across USPTO, EPO, and CGPDTM patent databases
- ✅ **Protective shield** for Indian startups against international patent trolls

## Roadmap

### Phase 1: MVP (Current - Hackathon)
- ✅ Router Agent with query parsing and orchestration
- ✅ Data Custodian for patent document processing
- ✅ Corporate Intelligence with basic assignee resolution
- ✅ Simple FTO analysis with keyword-based search

### Phase 2: Biotech Support
- 🔄 SMILES database integration for chemical/pharmaceutical patents
- 🔄 Molecular structure search and similarity analysis
- 🔄 Substructure matching for compound patents

### Phase 3: Full Indian Integration
- 🔄 Real-time CGPDTM (Indian Patent Office) data ingestion
- 🔄 Hindi language support for patent processing
- 🔄 India-specific landscape analysis and FTO assessments

## Getting Started

### Prerequisites

- AWS Account with Bedrock access
- Python 3.9+ or Node.js 18+
- MongoDB Atlas account
- API keys for USPTO, EPO, CGPDTM

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/knot.git
cd knot

# Install dependencies
pip install -r requirements.txt  # Python
# or
npm install  # Node.js

# Configure environment
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Quick Start

```python
from knot import KnotClient

# Initialize client
client = KnotClient(api_key="your-api-key")

# Perform FTO analysis
result = client.analyze_fto(
    product_description="IoT sensor for temperature monitoring",
    target_markets=["US", "EU", "India"]
)

print(f"Risk Level: {result.overall_risk}")
print(f"High Risk Patents: {len(result.high_risk_patents)}")
```

## Documentation

- [Requirements Document](.kiro/specs/project-knot/requirements.md) - Detailed functional requirements
- [Design Document](.kiro/specs/project-knot/design.md) - System architecture and agent interfaces
- [Implementation Plan](.kiro/specs/project-knot/tasks.md) - Development roadmap (coming soon)
- [API Documentation](docs/api.md) - REST API reference (coming soon)

## Architecture Diagram

```
┌─────────────┐
│   User UI   │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────────┐
│         Agent 9: Router Agent                    │
│    (Query Parsing & Orchestration)               │
└──────┬──────────────────────────────────────────┘
       │
       ├─────► Agent 1: Data Custodian (OCR/Normalization)
       ├─────► Agent 2: Corporate Intelligence (Graph Analysis)
       ├─────► Agent 3: Market Analyst (Product Linkage)
       ├─────► Agent 4: Scraper (API Ingestion)
       ├─────► Agent 5: Integration (Data Unification)
       ├─────► Agent 6: Landscaping (White Space Detection)
       ├─────► Agent 7: FTO Risk Analyst (Infringement Analysis)
       └─────► Agent 8: Validity Researcher (Prior Art)
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Check the [tasks.md](.kiro/specs/project-knot/tasks.md) for available tasks
2. Create a feature branch
3. Implement with tests (unit + property-based)
4. Submit pull request with test coverage

## Testing

```bash
# Run unit tests
pytest tests/unit/

# Run property-based tests
pytest tests/property/

# Run integration tests
pytest tests/integration/

# Run all tests with coverage
pytest --cov=knot tests/
```

## License

[MIT License](LICENSE)

## Acknowledgments

- Built for AWS Hackathon 2024
- Powered by Amazon Bedrock and Claude AI
- Developed with Kiro IDE and Amazon Q Developer

## Contact

- **Project Lead**: Abhishek More
- **Website**: [https://projectknot.io](https://projectknot.io)

---

**Project Knot** - Democratizing IP Intelligence for Indian Innovation 🇮🇳
