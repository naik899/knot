"""FastAPI application with startup seed."""

import uvicorn
from fastapi import FastAPI

from knot.config import settings
from knot.api.routes import router
from knot.api.dependencies import get_container
from knot.mock_data.seed import seed_all


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Agentic IP Intelligence Mesh for Indian MSMEs/startups",
    )

    app.include_router(router, prefix=settings.api_prefix)

    @app.on_event("startup")
    async def startup():
        container = get_container()
        seed_all(container.patent_store, container.graph_store, container.search_store)
        print(f"Seeded {container.patent_store.count()} patents, "
              f"{container.graph_store.count()} companies, "
              f"{len(container.search_store.get_all_products())} products, "
              f"{len(container.search_store.get_all_prior_art())} prior art entries")

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("knot.main:app", host=settings.host, port=settings.port, reload=True)
