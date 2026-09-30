from typing import Dict, Any
from app.ai.ai_provider import get_ai_provider

class LLMClient:
    def generate_json(self, prompt: str, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        provider = get_ai_provider()
        return provider.generate_json(prompt, fallback_data)

    def chat_response(self, system_prompt: str, user_message: str, fallback_text: str) -> str:
        provider = get_ai_provider()
        return provider.chat_response(system_prompt, user_message, fallback_text)

llm_client = LLMClient()
