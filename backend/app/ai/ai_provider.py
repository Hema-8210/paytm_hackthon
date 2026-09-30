from abc import ABC, abstractmethod
import json
import logging
from typing import Dict, Any, List
from app.core.config import settings

logger = logging.getLogger("skillpath.ai")

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_json(self, prompt: str, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def chat_response(self, system_prompt: str, user_message: str, fallback_text: str) -> str:
        pass


class LocalFallbackProvider(BaseAIProvider):
    def generate_json(self, prompt: str, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Using LocalFallbackProvider for JSON generation.")
        return fallback_data

    def chat_response(self, system_prompt: str, user_message: str, fallback_text: str) -> str:
        logger.info("Using LocalFallbackProvider for Chat response.")
        return fallback_text


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)

    def generate_json(self, prompt: str, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a software career and skill gap analysis AI. Return output strictly in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            logger.warning(f"OpenAIProvider generate_json failed: {e}. Falling back.")
            return fallback_data

    def chat_response(self, system_prompt: str, user_message: str, fallback_text: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"OpenAIProvider chat_response failed: {e}. Falling back.")
            return fallback_text


def get_ai_provider() -> BaseAIProvider:
    if settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY.strip()) > 10:
        try:
            return OpenAIProvider(settings.OPENAI_API_KEY)
        except Exception as e:
            logger.warning(f"Failed to instantiate OpenAIProvider: {e}")
            return LocalFallbackProvider()
    return LocalFallbackProvider()
