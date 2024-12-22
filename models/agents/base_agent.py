import asyncio
from functools import partial
from typing import Dict, Any

from groq import Groq

from models.roles.role import AgentRole


class BaseAgent:
    def __init__(self, api_key: str, role: AgentRole):
        self.client = Groq(api_key=api_key)
        self.role = role
        self.model = "llama3-8b-8192"
        self.conversation_history = []

    def _get_system_prompt(self) -> str:
        raise NotImplementedError

    async def _get_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get analysis from the LLM using async execution"""
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": prompt}
        ]

        # Run the synchronous Groq API call in a thread pool
        loop = asyncio.get_event_loop()
        completion = await loop.run_in_executor(
            None,
            partial(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
        )

        return completion.choices[0].message.content
