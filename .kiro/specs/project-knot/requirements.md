# Requirements Document: Project Knot - Agentic IP Intelligence Mesh

## Introduction

Project Knot is a decentralized, multi-agent orchestration framework designed to democratize Intellectual Property (IP) intelligence for Indian MSMEs and startups. The system performs high-order reasoning across legal, technical, and commercial datasets, linking global patent data to corporate hierarchies and product disclosures.

### Core Problem Statement

Indian startups and MSMEs face three critical IP challenges:
1. **Fragmented Data**: Patent information scattered across USPTO, EPO, and India's CGPDTM with inconsistent formats
2. **Hidden Ownership**: Deceptive patent assignees using shell companies and subsidiaries to obscure true ownership
3. **Siloed Context**: R&D teams lacking strategic business intelligence about patent landscapes and commercial applications

### Solution Approach

Project Knot addresses these challenges through a 9-agent architecture that provides:
- **Unified Data Access**: Automated ingestion and normalization from multiple patent offices
- **Corporate Intelligence**: Graph-based analysis achieving 90%+ accuracy in identifying ultimate parent companies
- **Rapid FTO Analysis**: Reducing time-to-insight from 2 weeks to under 10 minutes
- **Strategic Context**: Linking patents to products, identifying white spaces, and discovering prior art

The system targets Indian MSMEs and startups, providing a "protective shield" against international patent trolls while enabling informed R&D investment decisions.

## Glossary

- **System**: The Project Knot multi-agent orchestration framework
- **Router_Agent**: Central LLM orchestrator (Agent 9) that triages user queries to specialized sub-agents
- **Data_Custodian**: Agent 1 responsible for OCR, cleaning, and normalization of patent documents
- **Corporate_Intelligence_Agent**: Agent 2 that maps patent assignees to ultimate parent companies
- **Market_Analyst**: Agent 3 that links patent claims to existing products and market disclosures
- **Scraper_Agent**: Agent 4 that performs real-time ingestion from patent office APIs and SEC filings
- **Integration_Agent**: Agent 5 that synchronizes disparate data sources into unified processing stream
- **Landscaping_Specialist**: Agent 6 that identifies white spaces for R&D opportunities
- **FTO_Risk_Analyst**: Agent 7 that performs multi-step Freedom to Operate risk assessments
- **Validity_Researcher**: Agent 8 that finds prior art to challenge or verify patent claims
- **FTO**: Freedom to Operate - legal assessment of whether a product/process infringes existing patents
- **Patent_Office_API**: External APIs from USPTO, EPO, and CGPDTM (Indian Patent Office)
- **Ultimate_Parent_Company**: The top-level corporate entity in an ownership hierarchy
- **White_Space**: Technology areas with minimal patent coverage, representing R&D opportunities
- **Prior_Art**: Previously published information that may invalidate patent claims
- **User**: Indian MSME or startup seeking IP intelligence insights

## Requirements

### Requirement 1: Central Query Routing and Orchestration

**User Story:** As a user, I want to submit natural language queries about IP intelligence, so that the system can automatically route my request to the appropriate specialized agents.

#### Acceptance Criteria

1. WHEN a user submits a query, THE Router_Agent SHALL parse the query intent and identify relevant specialized agents
2. WHEN multiple agents are needed, THE Router_Agent SHALL orchestrate the execution sequence and manage inter-agent dependencies
3. WHEN an agent completes its task, THE Router_Agent SHALL aggregate results and determine if additional agents are required
4. WHEN all required agents complete execution, THE Router_Agent SHALL synthesize a unified response for the user
5. WHEN a query cannot be routed, THE Router_Agent SHALL request clarification from the user with specific guidance

### Requirement 2: Patent Document Processing and Normalization

**User Story:** As a user, I want patent documents from multiple sources to be automatically cleaned and normalized, so that I can search and analyze them consistently.

#### Acceptance Criteria

1. WHEN a patent PDF is ingested, THE Data_Custodian SHALL perform OCR to extract text content
2. WHEN text is extracted, THE Data_Custodian SHALL normalize formatting, remove artifacts, and standardize field structures
3. WHEN patent data contains multiple languages, THE Data_Custodian SHALL detect the language and apply appropriate processing rules
4. WHEN normalization is complete, THE Data_Custodian SHALL validate that all required patent fields are present and properly formatted
5. WHEN validation fails, THE Data_Custodian SHALL log the error with specific field information and mark the document for manual review

### Requirement 3: Real-Time Patent Office Data Ingestion

**User Story:** As a user, I want the system to automatically fetch the latest patent data from global patent offices, so that my searches reflect current information.

#### Acceptance Criteria

1. WHEN the system initializes, THE Scraper_Agent SHALL establish connections to USPTO, EPO, and CGPDTM APIs
2. WHEN new patent publications are available, THE Scraper_Agent SHALL fetch and queue them for processing within 24 hours
3. WHEN API rate limits are encountered, THE Scraper_Agent SHALL implement exponential backoff and retry logic
4. WHEN SEC filings are updated, THE Scraper_Agent SHALL extract corporate structure and M&A information
5. WHEN data ingestion fails, THE Scraper_Agent SHALL log the failure with timestamp and error details for monitoring

### Requirement 4: Multi-Source Data Integration

**User Story:** As a user, I want data from different patent offices and corporate databases to be synchronized, so that I can perform unified searches across all sources.

#### Acceptance Criteria

1. WHEN data arrives from multiple sources, THE Integration_Agent SHALL map fields to a unified schema
2. WHEN duplicate patents are detected across sources, THE Integration_Agent SHALL merge records and preserve all source references
3. WHEN data conflicts exist, THE Integration_Agent SHALL apply resolution rules prioritizing the most recent authoritative source
4. WHEN integration is complete, THE Integration_Agent SHALL update the unified index for search availability
5. WHEN schema mapping fails, THE Integration_Agent SHALL quarantine the record and alert administrators

### Requirement 5: Corporate Hierarchy and Assignee Resolution

**User Story:** As a user, I want to identify the ultimate parent company behind patent assignees, so that I can understand true ownership despite shell companies and subsidiaries.

#### Acceptance Criteria

1. WHEN a patent assignee is processed, THE Corporate_Intelligence_Agent SHALL query corporate databases to identify ownership relationships
2. WHEN subsidiary relationships are found, THE Corporate_Intelligence_Agent SHALL traverse the ownership graph to identify the ultimate parent company
3. WHEN M&A events are detected, THE Corporate_Intelligence_Agent SHALL update ownership mappings with effective dates
4. WHEN ownership resolution completes, THE Corporate_Intelligence_Agent SHALL achieve 90% or greater accuracy in identifying ultimate parent companies
5. WHEN ownership cannot be determined, THE Corporate_Intelligence_Agent SHALL flag the assignee as unresolved and provide available partial information

### Requirement 6: Patent-to-Product Linkage

**User Story:** As a user, I want to see which patents are linked to actual products in the market, so that I can assess real-world commercial relevance.

#### Acceptance Criteria

1. WHEN a patent is analyzed, THE Market_Analyst SHALL scrape web sources to identify product disclosures matching patent claims
2. WHEN product matches are found, THE Market_Analyst SHALL extract product names, descriptions, and commercial availability
3. WHEN patent claims reference technical specifications, THE Market_Analyst SHALL compare them against published product datasheets
4. WHEN linkage analysis completes, THE Market_Analyst SHALL assign confidence scores to each patent-product relationship
5. WHEN no product matches are found, THE Market_Analyst SHALL indicate the patent may be defensive or speculative

### Requirement 7: Technology Landscape Analysis and White Space Identification

**User Story:** As a user, I want to identify technology areas with minimal patent coverage, so that I can focus R&D efforts on opportunities with lower IP risk.

#### Acceptance Criteria

1. WHEN a technology domain is specified, THE Landscaping_Specialist SHALL retrieve all relevant patents and cluster them by technical concepts
2. WHEN patent clusters are identified, THE Landscaping_Specialist SHALL analyze density and identify gaps representing white spaces
3. WHEN white spaces are found, THE Landscaping_Specialist SHALL rank them by R&D opportunity based on market size and competitive activity
4. WHEN landscape analysis completes, THE Landscaping_Specialist SHALL generate visualizations showing patent density and white space regions
5. WHEN insufficient patent data exists, THE Landscaping_Specialist SHALL indicate the domain requires additional data collection

### Requirement 8: Freedom to Operate Risk Assessment

**User Story:** As a user, I want to assess whether my product or technology infringes existing patents, so that I can make informed decisions about commercialization risks.

#### Acceptance Criteria

1. WHEN a product description is provided, THE FTO_Risk_Analyst SHALL identify all potentially relevant patents based on technical claims
2. WHEN relevant patents are identified, THE FTO_Risk_Analyst SHALL perform claim-by-claim analysis against the product features
3. WHEN potential infringement is detected, THE FTO_Risk_Analyst SHALL assign risk levels (high, medium, low) with justification
4. WHEN FTO analysis completes, THE FTO_Risk_Analyst SHALL reduce time-to-insight from 2 weeks to under 10 minutes
5. WHEN patents are expired or abandoned, THE FTO_Risk_Analyst SHALL exclude them from risk calculations

### Requirement 9: Prior Art Discovery for Patent Validity

**User Story:** As a user, I want to find prior art that may invalidate threatening patents, so that I can challenge weak patents or negotiate from a stronger position.

#### Acceptance Criteria

1. WHEN a patent is targeted for validity research, THE Validity_Researcher SHALL search academic publications, technical standards, and earlier patents
2. WHEN prior art candidates are found, THE Validity_Researcher SHALL compare publication dates against the target patent's priority date
3. WHEN prior art matches patent claims, THE Validity_Researcher SHALL extract relevant passages and assign relevance scores
4. WHEN validity research completes, THE Validity_Researcher SHALL generate a prior art report with citations and claim mappings
5. WHEN no prior art is found, THE Validity_Researcher SHALL indicate the patent appears novel based on available sources

### Requirement 10: User Query Interface and Response Synthesis

**User Story:** As a user, I want to receive comprehensive, actionable insights in response to my queries, so that I can make strategic IP decisions without needing deep legal expertise.

#### Acceptance Criteria

1. WHEN a user submits a query, THE System SHALL accept natural language input without requiring structured query syntax
2. WHEN processing completes, THE System SHALL present results in a structured format with executive summary, detailed findings, and supporting evidence
3. WHEN multiple insights are available, THE System SHALL prioritize information by relevance and business impact
4. WHEN results include risk assessments, THE System SHALL provide clear recommendations and next steps
5. WHEN the user requests clarification, THE System SHALL provide drill-down capabilities into specific findings

### Requirement 11: System Performance and Scalability

**User Story:** As a user, I want the system to respond quickly even when analyzing large patent portfolios, so that I can iterate on my research efficiently.

#### Acceptance Criteria

1. WHEN a simple FTO query is submitted, THE System SHALL return initial results within 10 minutes
2. WHEN processing large datasets, THE System SHALL provide progress indicators and estimated completion times
3. WHEN multiple users submit concurrent queries, THE System SHALL maintain response times through parallel agent execution
4. WHEN system load increases, THE System SHALL scale agent instances automatically to maintain performance
5. WHEN agent execution fails, THE System SHALL retry with exponential backoff and provide partial results if available

### Requirement 12: Data Security and Access Control

**User Story:** As a user, I want my proprietary product information and search queries to remain confidential, so that my competitive strategy is protected.

#### Acceptance Criteria

1. WHEN a user creates an account, THE System SHALL enforce strong authentication with multi-factor options
2. WHEN user data is stored, THE System SHALL encrypt sensitive information at rest and in transit
3. WHEN queries are processed, THE System SHALL isolate user data and prevent cross-user information leakage
4. WHEN audit logs are generated, THE System SHALL record all data access events with timestamps and user identifiers
5. WHEN data retention policies apply, THE System SHALL automatically purge user data after the specified retention period

### Requirement 13: Integration with Amazon Bedrock, KIRO and Claude Models

**User Story:** As a system administrator, I want the system to leverage Amazon Bedrock's KIRO and Claude models for reasoning capabilities, so that we can provide high-quality IP intelligence without managing LLM infrastructure.

#### Acceptance Criteria

1. WHEN agents require LLM reasoning, THE System SHALL invoke Amazon Bedrock APIs with appropriate KIRO and Claude model versions
2. WHEN API calls are made, THE System SHALL implement retry logic and fallback strategies for service interruptions
3. WHEN token limits are approached, THE System SHALL chunk inputs and aggregate outputs intelligently
4. WHEN model responses are received, THE System SHALL validate output format and extract structured information
5. WHEN API costs exceed budget thresholds, THE System SHALL alert administrators and implement rate limiting

### Requirement 14: Monitoring and Observability

**User Story:** As a system administrator, I want comprehensive monitoring of agent performance and system health, so that I can identify and resolve issues proactively.

#### Acceptance Criteria

1. WHEN agents execute tasks, THE System SHALL log execution times, success rates, and error conditions
2. WHEN performance degrades, THE System SHALL generate alerts with severity levels and diagnostic information
3. WHEN users report issues, THE System SHALL provide request tracing across all agent interactions
4. WHEN system metrics are collected, THE System SHALL aggregate them into dashboards showing key performance indicators
5. WHEN anomalies are detected, THE System SHALL trigger automated diagnostics and notify administrators

### Requirement 15: Biotech and Chemical Patent Support (Phase 2)

**User Story:** As a biotech startup, I want the system to understand chemical structures and molecular formulas, so that I can assess FTO for pharmaceutical and chemical innovations.

#### Acceptance Criteria

1. WHERE biotech support is enabled, WHEN a SMILES notation is provided, THE System SHALL parse and normalize the molecular structure
2. WHERE biotech support is enabled, WHEN searching for similar compounds, THE System SHALL perform substructure and similarity searches
3. WHERE biotech support is enabled, WHEN patent claims include chemical formulas, THE System SHALL extract and index them for searchability
4. WHERE biotech support is enabled, WHEN comparing molecules, THE System SHALL identify structural similarities and functional group matches
5. WHERE biotech support is enabled, WHEN biotech queries are submitted, THE System SHALL integrate SMILES database results with patent analysis

### Requirement 16: Indian Patent Office Real-Time Integration (Phase 3)

**User Story:** As an Indian startup, I want real-time access to CGPDTM patent data, so that I can monitor domestic patent activity and identify local competitors.

#### Acceptance Criteria

1. WHERE CGPDTM integration is enabled, WHEN the system initializes, THE Scraper_Agent SHALL establish connection to CGPDTM APIs
2. WHERE CGPDTM integration is enabled, WHEN new Indian patents are published, THE System SHALL ingest them within 24 hours
3. WHERE CGPDTM integration is enabled, WHEN Indian patent data is processed, THE System SHALL handle Hindi and English language content
4. WHERE CGPDTM integration is enabled, WHEN FTO analysis is performed, THE System SHALL include Indian patent coverage in risk assessments
5. WHERE CGPDTM integration is enabled, WHEN landscape analysis is requested, THE System SHALL provide India-specific white space identification

### Requirement 17: Graph-Based Corporate Relationship Analysis

**User Story:** As a user, I want to visualize complex corporate ownership structures, so that I can understand patent portfolio consolidation and M&A impacts.

#### Acceptance Criteria

1. WHEN corporate relationships are queried, THE System SHALL construct a graph representation of ownership hierarchies
2. WHEN graph analysis is performed, THE System SHALL identify ultimate parent companies through graph traversal algorithms
3. WHEN M&A events occur, THE System SHALL update graph edges with acquisition dates and ownership percentages
4. WHEN visualization is requested, THE System SHALL generate interactive graphs showing corporate relationships and patent assignments
5. WHEN graph queries execute, THE System SHALL achieve 90% or greater accuracy in identifying ultimate parent companies

### Requirement 18: Incremental Learning and Feedback Integration

**User Story:** As a user, I want the system to improve its accuracy based on my feedback, so that results become more relevant to my specific industry and use cases.

#### Acceptance Criteria

1. WHEN users provide feedback on results, THE System SHALL capture relevance ratings and correction suggestions
2. WHEN feedback is collected, THE System SHALL aggregate patterns to identify systematic errors or biases
3. WHEN sufficient feedback exists, THE System SHALL retrain classification models to improve accuracy
4. WHEN model updates are deployed, THE System SHALL A/B test new models against baseline performance
5. WHEN feedback indicates incorrect corporate mappings, THE System SHALL update the knowledge graph and propagate corrections

### Requirement 19: Export and Reporting Capabilities

**User Story:** As a user, I want to export analysis results in multiple formats, so that I can share insights with stakeholders and integrate with other tools.

#### Acceptance Criteria

1. WHEN analysis completes, THE System SHALL provide export options including PDF, JSON, and CSV formats
2. WHEN PDF reports are generated, THE System SHALL include executive summaries, visualizations, and detailed findings
3. WHEN JSON exports are requested, THE System SHALL provide structured data with all metadata and confidence scores
4. WHEN CSV exports are generated, THE System SHALL format data for compatibility with spreadsheet and BI tools
5. WHEN exports are created, THE System SHALL include timestamps, query parameters, and data source attributions

### Requirement 20: API Access for Programmatic Integration

**User Story:** As a developer, I want to access Project Knot capabilities through APIs, so that I can integrate IP intelligence into my organization's existing workflows and tools.

#### Acceptance Criteria

1. WHEN API endpoints are accessed, THE System SHALL authenticate requests using API keys or OAuth tokens
2. WHEN API requests are submitted, THE System SHALL accept queries in JSON format with structured parameters
3. WHEN API responses are returned, THE System SHALL provide results in JSON format with consistent schema
4. WHEN API rate limits are exceeded, THE System SHALL return HTTP 429 status with retry-after headers
5. WHEN API documentation is accessed, THE System SHALL provide OpenAPI specifications with examples and authentication details
