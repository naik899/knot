"""Azure OpenAI LLM service with graceful fallback."""

import json
import logging

from knot.config import Settings

logger = logging.getLogger(__name__)


class LLMService:
    """Wraps Azure OpenAI for chat completions and embeddings.

    Returns None from all methods when credentials are not configured,
    allowing agents to fall back to rule-based logic.
    """

    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = None

        if self.is_available:
            try:
                from openai import AzureOpenAI

                self._client = AzureOpenAI(
                    azure_endpoint=settings.azure_openai_endpoint,
                    api_key=settings.azure_openai_api_key,
                    api_version=settings.azure_openai_api_version,
                )
                logger.info("Azure OpenAI client initialized successfully.")
            except Exception as exc:
                logger.warning("Failed to initialise Azure OpenAI client: %s", exc)
                self._client = None

    # ------------------------------------------------------------------
    # Availability
    # ------------------------------------------------------------------

    @property
    def is_available(self) -> bool:
        """True when LLM is enabled and Azure credentials are configured."""
        s = self._settings
        return bool(
            s.llm_enabled
            and s.azure_openai_endpoint
            and s.azure_openai_api_key
            and s.azure_openai_chat_deployment
        )

    # ------------------------------------------------------------------
    # Chat completions
    # ------------------------------------------------------------------

    def chat(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int | None = None,
    ) -> str | None:
        """Send a chat completion request. Returns None on failure or if unavailable."""
        if not self.is_available or self._client is None:
            return None

        try:
            response = self._client.chat.completions.create(
                model=self._settings.azure_openai_chat_deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=max_tokens or self._settings.llm_max_tokens,
                temperature=self._settings.llm_temperature,
            )
            return response.choices[0].message.content
        except Exception as exc:
            logger.warning("LLM chat call failed: %s", exc)
            return None

    def chat_json(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int | None = None,
    ) -> dict | None:
        """Chat completion that parses the response as JSON.

        The system prompt should instruct the model to return valid JSON.
        Returns None on failure or if unavailable.
        """
        raw = self.chat(system_prompt, user_message, max_tokens)
        if raw is None:
            return None

        # Strip markdown code fences if present
        text = raw.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first and last fence lines
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM response as JSON: %.200s", text)
            return None

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    def embed(self, texts: list[str]) -> list[list[float]] | None:
        """Generate embeddings for a list of texts. Returns None if unavailable."""
        if (
            not self.is_available
            or self._client is None
            or not self._settings.azure_openai_embedding_deployment
        ):
            return None

        try:
            response = self._client.embeddings.create(
                model=self._settings.azure_openai_embedding_deployment,
                input=texts,
            )
            return [item.embedding for item in response.data]
        except Exception as exc:
            logger.warning("LLM embed call failed: %s", exc)
            return None
