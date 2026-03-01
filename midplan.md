# Plan: Deep Agent + Skills for Project Knot

## Context

Project Knot currently uses a `RouterAgent` with hardcoded execution pipelines per goal type (FTO → scraper → fto_analyst → corporate_intel → validity; landscape → landscaping only; etc.). This is rigid — no dynamic reasoning, no adaptive tool selection based on intermediate results.

**Goal**: Replace the manual orchestration with LangChain's `deepagents` library (`create_deep_agent()`). The deep agent provides: a planning tool (`write_todos`), progressive skill disclosure (SKILL.md files), subagent spawning for context isolation, and automatic context management — all built on LangGraph.

**Key constraint**: Do NOT modify `BaseAgent`. Keep `RouterAgent` as fallback.

---

## Architecture

**Backend choice**: Uses the default **StateBackend** — skill file contents are loaded into memory at startup via `create_file_data()` and passed to every `invoke()` call as `files={}`. This avoids filesystem access at runtime and keeps deployment simple (no `root_dir` needed). Alternative backends (FilesystemBackend, StoreBackend) are not needed since skills are static and bundled with the app.

```
POST /query
    |
    v (if deep_agent available)
+----------------------------------------------+
| Main Deep Agent (knot-orchestrator)          |
|  model: AzureChatOpenAI                      |
|  checkpointer: MemorySaver()                 |
|  skills: ["/skills/"]  (path prefix for      |
|           progressive disclosure discovery)  |
|  tools: search_patents, normalize_patent,    |
|         validate_patent_data, detect_dupes   |
|  built-in: write_todos, task                 |
+--------+-------------------------------------+
         |
    (task tool → subagents)
    /      |        |        \         \
   v       v        v         v         v
 fto-    landscape validity  market   corporate
 analyst -analyst  -researcher -analyst -intel
 skills:  skills:   skills:   skills:   skills:
 ["/skills ["/skills ["/skills ["/skills ["/skills
  /fto/"]  /land.."] /valid.."] /market/"] /corp.."]
   |       |        |         |         |
   v       v        v         v         v
 [domain tools calling agent.execute()]
```

Fallback: No credentials or deep agent exception → existing `RouterAgent`.

---

## New Files

### `backend/src/knot/deepagent/__init__.py`
Exports `build_deep_agent`, `load_skill_files`.

### `backend/src/knot/deepagent/tools.py`
15 `@tool` wrappers using closures over agent instances. Each calls `agent.execute(task_type, payload)` and returns `json.dumps(result)`.

| Maker Function | Tools | Wraps |
|---|---|---|
| `make_fto_tools(fto_agent)` | `analyze_fto`, `check_patent_risk` | FTOAnalystAgent |
| `make_landscape_tools(landscaping)` | `analyze_landscape`, `find_white_spaces` | LandscapingAgent |
| `make_validity_tools(validity)` | `find_prior_art`, `validate_patent` | ValidityResearcherAgent |
| `make_market_tools(market)` | `match_patent_to_products`, `find_product_matches` | MarketAnalystAgent |
| `make_corporate_tools(corporate)` | `resolve_parent_company`, `get_ownership_graph`, `resolve_assignees` | CorporateIntelAgent |
| `make_search_tools(scraper)` | `search_patents` | ScraperAgent |
| `make_data_tools(custodian, integration)` | `normalize_patent`, `validate_patent_data`, `detect_duplicates` | DataCustodianAgent, IntegrationAgent |

Top-level `make_all_tools(agents)` aggregates everything.

### `backend/src/knot/deepagent/subagents.py`
`build_subagents(agents) -> list[dict]` — 5 domain subagents:

| Subagent | Tools it gets | Purpose |
|---|---|---|
| `fto-analyst` | analyze_fto, check_patent_risk, search_patents, resolve_assignees, find_prior_art | Full FTO workflow with patent search + assignee resolution |
| `landscape-analyst` | analyze_landscape, find_white_spaces | Landscape + white space identification |
| `validity-researcher` | find_prior_art, validate_patent | Prior art + validity assessment |
| `market-analyst` | match_patent_to_products, find_product_matches | Patent-product matching |
| `corporate-intel` | resolve_parent_company, get_ownership_graph, resolve_assignees | Ownership chains |

Each subagent has a focused `system_prompt` with step-by-step instructions and a `skills` path prefix pointing to its domain skill directory:

| Subagent | `skills` param |
|---|---|
| `fto-analyst` | `["/skills/fto/"]` |
| `landscape-analyst` | `["/skills/landscape/"]` |
| `validity-researcher` | `["/skills/validity/"]` |
| `market-analyst` | `["/skills/market/"]` |
| `corporate-intel` | `["/skills/corporate/"]` |

**Note**: Custom subagents do NOT auto-inherit the main agent's skills — each needs an explicit `skills` path list. The main agent uses `["/skills/"]` (all skills), while subagents get only their domain-specific prefix.

### `backend/src/knot/deepagent/skills/` — 6 SKILL.md files

Each follows the `deepagents` format: YAML frontmatter + markdown body with workflow steps.

**Frontmatter fields** (per docs):
- `name` — skill identifier (required)
- `description` — task-matching text, **max 1024 characters** (required; used for progressive disclosure matching)
- `allowed-tools` — comma-separated list of permitted tool names (required)
- `metadata.author`, `metadata.version` — optional but recommended for tracking skill iterations
- `license`, `compatibility` — optional

**Progressive disclosure**: The agent matches user prompts against `description` fields first (cheap), then reads the full SKILL.md only for matching skills (lazy-loading). This is why descriptions must be concise and specific.

| Skill | File | Description (≤1024 chars) | `allowed-tools` |
|---|---|---|---|
| FTO Analysis | `fto/SKILL.md` | "Freedom-to-Operate analysis for assessing patent infringement risk" | `analyze_fto, check_patent_risk, search_patents, resolve_assignees, find_prior_art` |
| Landscape | `landscape/SKILL.md` | "Patent landscape analysis to identify clusters, white spaces, opportunities" | `analyze_landscape, find_white_spaces` |
| Validity | `validity/SKILL.md` | "Patent validity research and prior art identification" | `find_prior_art, validate_patent` |
| Market | `market/SKILL.md` | "Patent-product matching and commercial application analysis" | `match_patent_to_products, find_product_matches` |
| Corporate | `corporate/SKILL.md` | "Corporate ownership resolution and assignee network mapping" | `resolve_parent_company, get_ownership_graph, resolve_assignees` |
| Patent Search | `patent-search/SKILL.md` | "Search patents by keywords, domain, or jurisdiction" | `search_patents` |

Each skill body contains: when to use, step-by-step tool calling instructions, and output format guidance.

Example SKILL.md structure:
```markdown
---
name: fto-analysis
description: Freedom-to-Operate analysis for assessing patent infringement risk
allowed-tools: analyze_fto, check_patent_risk, search_patents, resolve_assignees, find_prior_art
metadata:
  author: knot
  version: "1.0"
---

# FTO Analysis

## Overview
[When this skill applies]

## Instructions
### 1. Search relevant patents
[Step-by-step tool calling guidance]
### 2. Analyze infringement risk
...
### 3. Output format
[Expected response structure]
```

### `backend/src/knot/deepagent/skill_loader.py`
`load_skill_files() -> dict` — reads all SKILL.md files from disk at startup, returns a `StateBackend`-compatible files dict using `deepagents.backends.utils.create_file_data`. Called once at Container init, merged into every `invoke()` call via `initial_state["files"]`.

### `backend/src/knot/deepagent/agent_factory.py`
`build_deep_agent(settings, agents) -> tuple[CompiledStateGraph | None, dict | None]`

- Creates `AzureChatOpenAI` from existing `Settings` (same credentials as `LLMService`)
- Creates `checkpointer = MemorySaver()` for conversation state persistence
- Builds main agent tools (search + data quality only — domain tools go to subagents)
- Builds subagents via `build_subagents(agents)` — each with its own `skills` path prefix
- Calls:
  ```python
  agent = create_deep_agent(
      model=model,
      tools=main_tools,
      system_prompt=SYSTEM_PROMPT,
      subagents=subagent_configs,
      skills=["/skills/"],          # path prefix for skill discovery
      checkpointer=checkpointer,    # MemorySaver for state persistence
      name="knot-orchestrator",
  )
  ```
- Returns `(compiled_graph, skill_files)` or `(None, None)` on failure
- Lazy-imports `deepagents` so app starts even without the package installed

### `backend/src/knot/deepagent/response.py`
`extract_response(result, query) -> dict` — walks the deep agent's message history to extract:
- `executive_summary` from the final `AIMessage`
- `agent_results` from `ToolMessage` content (JSON-parsed)
- `sections` built from agent_results (FTO risk, landscape, validity, etc.)
- Returns dict matching existing `/query` response shape

---

## Modified Files

### `backend/pyproject.toml`
- Bump `requires-python` from `">=3.9"` to `">=3.11"` (deepagents requirement)
- Add dependencies: `deepagents>=0.4.0`, `langchain-openai>=0.3.0`

### `backend/requirements.txt`
- Add: `deepagents>=0.4.0`, `langchain-openai>=0.3.0`

### `backend/src/knot/config.py`
- Add one field: `deepagent_enabled: bool = True`

### `backend/src/knot/api/dependencies.py`
- Extract agents dict to `self._agents_dict` (used by both Router and deep agent)
- Add `self.deep_agent, self.skill_files = self._init_deep_agent()`
- `_init_deep_agent()` calls `build_deep_agent(settings, self._agents_dict)` with try/except ImportError

### `backend/src/knot/api/routes.py`
- Only `/query` endpoint changes:
  - Generate a `thread_id` per request (e.g., `uuid4().hex`) for checkpointer state tracking
  - If `container.deep_agent` is not None: invoke with:
    ```python
    result = container.deep_agent.invoke(
        {"messages": [{"role": "user", "content": query}], "files": container.skill_files},
        config={"configurable": {"thread_id": thread_id}},
    )
    ```
  - Extract response via `extract_response()`
  - On exception or empty result: fall through to existing RouterAgent path

---

## Implementation Order

| Step | Files | Depends on |
|---|---|---|
| 1 | `pyproject.toml`, `requirements.txt` | — |
| 2 | `config.py` (add `deepagent_enabled`) | — |
| 3 | `deepagent/__init__.py` | Step 1 |
| 4 | `deepagent/tools.py` (15 tool wrappers) | Step 1 |
| 5 | `deepagent/skills/*.md` (6 SKILL.md files) | — |
| 6 | `deepagent/skill_loader.py` | Steps 1, 5 |
| 7 | `deepagent/subagents.py` | Step 4 |
| 8 | `deepagent/agent_factory.py` | Steps 4, 6, 7 |
| 9 | `deepagent/response.py` | — |
| 10 | `api/dependencies.py` (modify) | Step 8 |
| 11 | `api/routes.py` (modify) | Steps 9, 10 |

---

## Verification

1. `pip install deepagents langchain-openai` succeeds
2. `python -c "from knot.deepagent import build_deep_agent; print('OK')"` — imports work
3. `pytest tests/` — all existing tests still pass (no existing files broken)
4. Tool wrapper unit tests: each `@tool` function returns valid JSON from `agent.execute()`
5. Skill loader test: `load_skill_files()` returns dict with all 6 `/skills/*/SKILL.md` paths
6. Subagent test: `build_subagents()` returns 5 dicts with required keys (name, description, system_prompt, tools)
7. With Azure keys: `POST /query` with "analyze FTO risk for IoT sensor in US market" → deep agent delegates to fto-analyst subagent → returns structured response with executive_summary and sections
8. Without Azure keys: same request → falls back to RouterAgent rule-based response
9. Response shape test: `extract_response()` produces dict with `executive_summary`, `sections`, `agent_results`, `orchestration: "deep_agent"`
