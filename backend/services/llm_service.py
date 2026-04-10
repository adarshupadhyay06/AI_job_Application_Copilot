import json
import os
from typing import Any

from dotenv import load_dotenv

try:
    from langchain_groq import ChatGroq
except ImportError:  # pragma: no cover - depends on local environment
    ChatGroq = None


load_dotenv()


class LLMService:
    def __init__(self) -> None:
        self.model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.api_key = os.getenv("GROQ_API_KEY")
        self.enabled = bool(self.api_key) and ChatGroq is not None
        self.llm = ChatGroq(model=self.model_name, temperature=0.2) if self.enabled else None

    def invoke_json(self, prompt: str, fallback: dict[str, Any]) -> dict[str, Any]:
        if not self.llm:
            return fallback

        response = self.llm.invoke(
            prompt
            + "\n\nReturn only valid JSON. Do not wrap it in markdown fences."
        )
        content = response.content if isinstance(response.content, str) else str(response.content)

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return fallback

    def invoke_text(self, prompt: str, fallback: str) -> str:
        if not self.llm:
            return fallback

        response = self.llm.invoke(prompt)
        return response.content if isinstance(response.content, str) else fallback


llm_service = LLMService()
