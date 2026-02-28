# Project Knot — Development Guide

## Project Structure

```
knot/
├── backend/
│   ├── pyproject.toml          # Python project config, dependencies
│   ├── requirements.txt        # Flat dependency list
│   ├── uv.lock                 # Lock file (auto-generated)
│   ├── src/knot/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── config.py           # Pydantic settings
│   │   ├── agents/             # 9 agent implementations
│   │   │   ├── base.py         # BaseAgent abstract class
│   │   │   ├── router.py       # RouterAgent (orchestrator)
│   │   │   ├── fto_analyst.py
│   │   │   ├── corporate_intel.py
│   │   │   ├── landscaping.py
│   │   │   ├── validity_researcher.py
│   │   │   ├── market_analyst.py
│   │   │   ├── data_custodian.py
│   │   │   ├── scraper.py
│   │   │   └── integration.py
│   │   ├── api/
│   │   │   ├── routes.py       # FastAPI route handlers
│   │   │   └── dependencies.py # DI container
│   │   ├── models/             # Pydantic data models
│   │   │   ├── patent.py
│   │   │   ├── company.py
│   │   │   ├── fto.py
│   │   │   ├── landscape.py
│   │   │   ├── validity.py
│   │   │   ├── product.py
│   │   │   ├── query.py
│   │   │   └── messages.py
│   │   ├── services/           # Reusable algorithms
│   │   │   ├── text_processing.py
│   │   │   ├── similarity.py
│   │   │   ├── clustering.py
│   │   │   └── graph_traversal.py
│   │   ├── stores/             # In-memory data stores
│   │   │   ├── patent_store.py
│   │   │   ├── graph_store.py
│   │   │   └── search_store.py
│   │   └── mock_data/          # Seed data for MVP
│   └── tests/
│       ├── conftest.py
│       ├── unit/               # Unit tests for agents, services, stores
│       ├── integration/        # API endpoint tests
│       └── property/           # Property-based tests (Hypothesis)
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/index.js
│       ├── api/                # API service files (one per domain)
│       ├── views/              # 7 page components
│       └── components/         # Reusable UI components
└── docs/                       # Documentation
```

## Setup

### Backend

```bash
cd backend
uv sync --all-extras    # Install all dependencies including dev
```

### Frontend

```bash
cd frontend
npm install
```

## Running

### Backend Server

```bash
cd backend
uv run python -m knot.main
# Starts on http://localhost:8000
```

### Frontend Dev Server

```bash
cd frontend
npm run dev
# Starts on http://localhost:5173, proxies /api to backend
```

## Testing

### Run All Tests

```bash
cd backend
uv run python -m pytest tests/ -v
```

### Run by Category

```bash
# Unit tests only
uv run python -m pytest tests/unit/ -v

# Integration (API) tests
uv run python -m pytest tests/integration/ -v

# Property-based tests
uv run python -m pytest tests/property/ -v
```

### Test Structure

- **Unit tests** (`tests/unit/`): Test agents, services, and stores in isolation
- **Integration tests** (`tests/integration/`): Test API endpoints with TestClient
- **Property tests** (`tests/property/`): Hypothesis-based tests for mathematical properties (symmetry, idempotency, boundedness)

## Key Dependencies

### Backend
- **FastAPI** — REST API framework
- **Pydantic** — Data validation and settings
- **uvicorn** — ASGI server
- **pytest** — Testing framework
- **hypothesis** — Property-based testing

### Frontend
- **Vue 3** — UI framework
- **Vue Router** — Client-side routing
- **Axios** — HTTP client
- **Tailwind CSS** — Utility-first CSS
- **Vite** — Build tool and dev server

## Adding a New Agent

1. Create `backend/src/knot/agents/your_agent.py`
2. Extend `BaseAgent`, implement `execute(task_type, payload)`
3. Register in `backend/src/knot/api/dependencies.py` Container
4. Add API route in `backend/src/knot/api/routes.py`
5. Add tests in `backend/tests/unit/`

## Adding a New Frontend View

1. Create `frontend/src/views/YourView.vue`
2. Add API service in `frontend/src/api/your_service.js`
3. Add route in `frontend/src/router/index.js`
4. Add nav item in `frontend/src/components/AppLayout.vue`
