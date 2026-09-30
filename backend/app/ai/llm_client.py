import json
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger("skillpath.ai")

class LLMClient:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {e}")

    def generate_json(self, prompt: str, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempts to generate JSON using OpenAI. If key is missing or call fails, returns fallback_data.
        """
        if not self.client:
            return fallback_data
        
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
            logger.info(f"LLM call fallback triggered: {e}")
            return fallback_data

    def chat_response(self, system_prompt: str, user_message: str, fallback_text: str) -> str:
        """
        Attempts a chat completion using OpenAI. Returns fallback_text if fails.
        """
        if not self.client:
            return fallback_text
            
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
            logger.info(f"LLM chat fallback triggered: {e}")
            return fallback_text

llm_client = LLMClient()
