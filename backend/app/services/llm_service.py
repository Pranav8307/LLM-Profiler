# app/services/llm_service.py

import time
from typing import Dict
from groq import Groq
from app.core.config import get_settings

settings = get_settings()

MODEL_PRICING = {
    "llama-3.1-8b-instant": {
        "input": 0.0000002,
        "output": 0.0000006,
    },
    "llama-3.1-70b-versatile": {
        "input": 0.0000008,
        "output": 0.0000024,
    }
}

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "llama-3.1-8b-instant"

    def _estimate_tokens(self, text: str) -> int:
        return int(len(text.split()) * 1.3)

    def generate(self, prompt: str) -> Dict:
        start = time.time()

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )

            answer = completion.choices[0].message.content
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            tokens = completion.usage.total_tokens

        except Exception as e:
            print("GROQ ERROR:", repr(e))

            answer = f"[FALLBACK MOCK]: {prompt[::-1]}"
            tokens = self._estimate_tokens(answer)
            cost = 0.0

        latency = round((time.time() - start) * 1000, 2)

        pricing = MODEL_PRICING.get(self.model, {"input": 0, "output": 0})

        cost = (
            prompt_tokens * pricing["input"] +
            completion_tokens * pricing["output"]
        )
        cost = round(cost, 6)

        return {
            "answer": answer,
            "latency_ms": latency,
            "tokens": tokens,
            "cost": round(cost, 6) if cost else 0.0
        }