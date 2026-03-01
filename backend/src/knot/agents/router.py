"""Agent 9: Router Agent - Query parsing, execution planning, orchestration, synthesis."""

import re

from knot.agents.base import BaseAgent
from knot.models.messages import AgentRequest
from knot.models.query import QueryIntent, ExecutionPlan, AgentStage


class RouterAgent(BaseAgent):
    agent_name = "router"

    def __init__(self, agents: dict[str, BaseAgent]):
        self.agents = agents

    def execute(self, task_type: str, payload: dict) -> dict:
        if task_type == "route_query":
            return self._route_query(payload)
        elif task_type == "parse_query":
            return self._parse_only(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _route_query(self, payload: dict) -> dict:
        query = payload.get("query", "")
        if not query:
            return {
                "error": "No query provided",
                "suggestion": "Please provide a natural language query about IP intelligence.",
                "confidence_score": 0.0,
            }

        # Step 1: Parse query intent
        intent = self.parse_query(query)

        # Step 2: Plan execution
        plan = self.plan_execution(intent)

        # Step 3: Execute agents in order
        agent_results = self._execute_plan(plan, intent)

        # Step 4: Synthesize response
        response = self._synthesize(intent, agent_results)

        return response

    def parse_query(self, query: str) -> QueryIntent:
        """Parse natural language query into structured intent using rule-based NLP."""
        query_lower = query.lower()

        # Determine primary goal
        primary_goal = self._detect_goal(query_lower)

        # Extract entities
        entities = self._extract_entities(query_lower)

        # Extract constraints
        constraints = self._extract_constraints(query_lower)

        return QueryIntent(
            primary_goal=primary_goal,
            entities=entities,
            constraints=constraints,
            raw_query=query,
        )

    def plan_execution(self, intent: QueryIntent) -> ExecutionPlan:
        """Create an execution plan based on the query intent."""
        stages = []

        if intent.primary_goal == "fto_analysis":
            stages = [
                AgentStage(agent_id="scraper", task_type="fetch_patents", inputs={}, depends_on=[]),
                AgentStage(agent_id="fto_analyst", task_type="analyze_fto", inputs={}, depends_on=["scraper"]),
                AgentStage(agent_id="corporate_intel", task_type="resolve_assignees", inputs={}, depends_on=["fto_analyst"]),
                AgentStage(agent_id="validity_researcher", task_type="find_prior_art", inputs={}, depends_on=["fto_analyst"]),
            ]
        elif intent.primary_goal == "landscape":
            stages = [
                AgentStage(agent_id="landscaping", task_type="analyze_landscape", inputs={}, depends_on=[]),
            ]
        elif intent.primary_goal == "validity":
            stages = [
                AgentStage(agent_id="validity_researcher", task_type="find_prior_art", inputs={}, depends_on=[]),
            ]
        elif intent.primary_goal == "corporate_intel":
            stages = [
                AgentStage(agent_id="corporate_intel", task_type="resolve_parent", inputs={}, depends_on=[]),
            ]
        elif intent.primary_goal == "product_match":
            stages = [
                AgentStage(agent_id="market_analyst", task_type="match_patent_to_products", inputs={}, depends_on=[]),
            ]
        else:
            # Patent search - default
            stages = [
                AgentStage(agent_id="scraper", task_type="fetch_patents", inputs={}, depends_on=[]),
            ]

        return ExecutionPlan(stages=stages, intent=intent)

    def _execute_plan(self, plan: ExecutionPlan, intent: QueryIntent) -> dict:
        """Execute the plan stages in order, passing results forward."""
        results = {}

        for stage in plan.stages:
            agent = self.agents.get(stage.agent_id)
            if not agent:
                results[stage.agent_id] = {"error": f"Agent {stage.agent_id} not available"}
                continue

            # Build payload based on intent and previous results
            payload = self._build_payload(stage, intent, results)

            request = AgentRequest(
                source_agent="router",
                target_agent=stage.agent_id,
                task_type=stage.task_type,
                payload=payload,
            )

            response = agent.handle_request(request)
            results[stage.agent_id] = response.result

        return results

    def _build_payload(self, stage: AgentStage, intent: QueryIntent, previous_results: dict) -> dict:
        """Build the payload for an agent based on intent and previous results."""
        technologies = intent.entities.get("technologies", [])
        products = intent.entities.get("products", [])
        companies = intent.entities.get("companies", [])
        jurisdictions = intent.constraints.get("jurisdictions", [])
        description = " ".join(technologies + products) or intent.raw_query

        if stage.agent_id == "scraper":
            return {
                "keywords": technologies + products,
                "jurisdictions": jurisdictions,
            }
        elif stage.agent_id == "fto_analyst":
            return {
                "description": description,
                "target_markets": jurisdictions,
                "keywords": technologies + products,
            }
        elif stage.agent_id == "corporate_intel":
            if stage.task_type == "resolve_assignees":
                # Get assignees from FTO results
                fto_result = previous_results.get("fto_analyst", {})
                report = fto_result.get("report", {})
                analyses = report.get("analyses", [])
                assignees = list(set(a.get("assignee", "") for a in analyses if a.get("assignee")))
                return {"assignees": assignees}
            else:
                return {
                    "company_name": companies[0] if companies else "",
                }
        elif stage.agent_id == "validity_researcher":
            # Find the highest risk patent from FTO
            fto_result = previous_results.get("fto_analyst", {})
            report = fto_result.get("report", {})
            analyses = report.get("analyses", [])
            high_risk = [a for a in analyses if a.get("overall_risk") == "high"]
            if high_risk:
                return {"patent_id": high_risk[0].get("patent_id", ""), "keywords": technologies}
            elif analyses:
                return {"patent_id": analyses[0].get("patent_id", ""), "keywords": technologies}
            return {"keywords": technologies}
        elif stage.agent_id == "landscaping":
            return {
                "domain": " ".join(technologies) or intent.raw_query,
                "keywords": technologies + products,
            }
        elif stage.agent_id == "market_analyst":
            return {
                "description": description,
                "keywords": technologies + products,
            }
        return {}

    def _synthesize(self, intent: QueryIntent, results: dict) -> dict:
        """Synthesize a unified response from all agent results."""
        sections = []

        # FTO section
        fto = results.get("fto_analyst", {})
        if fto and "report" in fto:
            report = fto["report"]
            sections.append({
                "title": "Freedom to Operate Analysis",
                "summary": report.get("summary", ""),
                "risk_level": report.get("overall_risk", "unknown"),
                "details": {
                    "high_risk_patents": report.get("high_risk_count", 0),
                    "medium_risk_patents": report.get("medium_risk_count", 0),
                    "low_risk_patents": report.get("low_risk_count", 0),
                    "analyses": report.get("analyses", []),
                },
                "recommendations": report.get("recommendations", []),
            })

        # Corporate Intelligence section
        corp = results.get("corporate_intel", {})
        if corp and "assignee_resolutions" in corp:
            resolutions = corp["assignee_resolutions"]
            parent_companies = set()
            for r in resolutions:
                if r.get("resolved") and r.get("ultimate_parent_name"):
                    parent_companies.add(r["ultimate_parent_name"])

            sections.append({
                "title": "Corporate Intelligence",
                "summary": f"Resolved {corp.get('resolved_count', 0)} of {corp.get('total', 0)} assignees. Ultimate parent companies: {', '.join(parent_companies) or 'None identified'}.",
                "details": {"resolutions": resolutions},
            })

        # Validity/Prior Art section
        validity = results.get("validity_researcher", {})
        if validity and "prior_art_results" in validity:
            pa_results = validity["prior_art_results"]
            sections.append({
                "title": "Prior Art Analysis",
                "summary": f"Found {len(pa_results)} prior art candidates for patent {validity.get('patent_id', 'N/A')}.",
                "details": {"prior_art": pa_results},
            })

        # Landscape section
        landscape = results.get("landscaping", {})
        if landscape and "report" in landscape:
            lreport = landscape["report"]
            sections.append({
                "title": "Technology Landscape",
                "summary": lreport.get("summary", ""),
                "details": lreport,
            })

        # Product matching section
        market = results.get("market_analyst", {})
        if market and "matches" in market:
            sections.append({
                "title": "Product Matching",
                "summary": f"Found {market.get('total_matches', 0)} product matches.",
                "details": {"matches": market["matches"]},
            })

        # Scraper results (if standalone)
        scraper = results.get("scraper", {})
        if scraper and not fto and "patents" in scraper:
            sections.append({
                "title": "Patent Search Results",
                "summary": f"Found {scraper.get('total_found', 0)} patents.",
                "details": {"patents": scraper["patents"]},
            })

        # Build executive summary
        executive_summary = self._build_executive_summary(intent, sections)

        return {
            "query": intent.raw_query,
            "intent": intent.model_dump(),
            "executive_summary": executive_summary,
            "sections": sections,
            "agent_results": results,
            "confidence_score": 0.85,
        }

    def _build_executive_summary(self, intent: QueryIntent, sections: list[dict]) -> str:
        """Build a concise executive summary."""
        parts = [f"Analysis for: {intent.raw_query}\n"]

        for section in sections:
            parts.append(f"- {section['title']}: {section.get('summary', '')}")
            if 'recommendations' in section:
                for rec in section['recommendations']:
                    parts.append(f"  * {rec}")

        return "\n".join(parts)

    def _detect_goal(self, query: str) -> str:
        """Detect the primary goal from query text."""
        fto_keywords = ["fto", "freedom to operate", "infringement", "infringe", "risk", "commercialize", "commercializ"]
        landscape_keywords = ["landscape", "white space", "whitespace", "opportunity", "gap", "trend"]
        validity_keywords = ["prior art", "validity", "invalidate", "challenge", "novel"]
        corporate_keywords = ["parent company", "ownership", "subsidiary", "shell company", "who owns", "corporate"]
        product_keywords = ["product", "match", "link", "commercial", "market"]

        for kw in fto_keywords:
            if kw in query:
                return "fto_analysis"
        for kw in landscape_keywords:
            if kw in query:
                return "landscape"
        for kw in validity_keywords:
            if kw in query:
                return "validity"
        for kw in corporate_keywords:
            if kw in query:
                return "corporate_intel"
        for kw in product_keywords:
            if kw in query:
                return "product_match"

        return "patent_search"

    def _extract_entities(self, query: str) -> dict[str, list[str]]:
        """Extract entities from the query."""
        entities: dict[str, list[str]] = {
            "technologies": [],
            "products": [],
            "companies": [],
            "patents": [],
        }

        # Technology keywords
        tech_terms = [
            "iot", "internet of things", "temperature sensor", "temperature monitoring",
            "wireless sensor", "sensor network", "cloud", "analytics",
            "machine learning", "edge computing", "bluetooth", "underwater",
            "energy harvesting", "predictive maintenance", "digital twin",
            "cold chain", "environmental monitoring", "hvac",
        ]
        for term in tech_terms:
            if term in query:
                entities["technologies"].append(term)

        # If no tech terms found, extract nouns as potential technologies
        if not entities["technologies"]:
            # Simple extraction: split by common prepositions and take the nouns
            for phrase in re.split(r'\b(?:for|in|of|about|regarding|on)\b', query):
                words = phrase.strip().split()
                if 1 <= len(words) <= 4:
                    entities["technologies"].append(phrase.strip())

        # Patent IDs
        patent_patterns = re.findall(r'(?:US|EP|IN)\d+[A-Z]?\d*', query.upper())
        entities["patents"] = patent_patterns

        # Company names (from known list)
        known_companies = [
            "techglobal", "sensortech", "techshield", "datavault",
            "eurosense", "oceantech", "agrisense",
        ]
        for comp in known_companies:
            if comp in query:
                entities["companies"].append(comp)

        return entities

    def _extract_constraints(self, query: str) -> dict:
        """Extract constraints like jurisdictions and date ranges."""
        constraints: dict = {}

        # Jurisdictions
        jurisdictions = []
        jurisdiction_map = {
            "us": "US", "united states": "US", "usa": "US", "america": "US",
            "eu": "EU", "europe": "EU", "european": "EU",
            "india": "IN", "indian": "IN",
            "china": "CN", "chinese": "CN",
            "japan": "JP", "japanese": "JP",
        }
        for term, code in jurisdiction_map.items():
            if term in query:
                if code not in jurisdictions:
                    jurisdictions.append(code)
        if jurisdictions:
            constraints["jurisdictions"] = jurisdictions

        return constraints

    def _parse_only(self, payload: dict) -> dict:
        """Just parse the query without executing."""
        query = payload.get("query", "")
        intent = self.parse_query(query)
        plan = self.plan_execution(intent)
        return {
            "intent": intent.model_dump(),
            "plan": plan.model_dump(),
            "confidence_score": 0.9,
        }
