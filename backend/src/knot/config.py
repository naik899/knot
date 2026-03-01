"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Project Knot"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    api_prefix: str = "/api/v1"

    # Azure OpenAI
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_chat_deployment: str = ""
    azure_openai_embedding_deployment: str = ""
    llm_enabled: bool = True
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.1

    # Deep Agent orchestration
    deepagent_enabled: bool = True

    # Rate limiting (simulated)
    max_requests_per_minute: int = 60

    # Agent timeouts (ms)
    default_agent_timeout_ms: int = 300000

    model_config = {"env_prefix": "KNOT_"}


settings = Settings()
