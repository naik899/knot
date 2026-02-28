"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Project Knot"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    api_prefix: str = "/api/v1"

    # Rate limiting (simulated)
    max_requests_per_minute: int = 60

    # Agent timeouts (ms)
    default_agent_timeout_ms: int = 300000

    model_config = {"env_prefix": "KNOT_"}


settings = Settings()
