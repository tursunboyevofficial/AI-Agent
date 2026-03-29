"""
LLM modul — Claude API orqali o'zbek tilida javob beradi
"""

from anthropic import Anthropic


SYSTEM_PROMPT = """Sen o'zbek tilida gaplashadigan aqlli yordamchisan.

Qoidalar:
- Har doim o'zbek tilida javob ber
- Qisqa va aniq javob ber (1-3 gap)
- Samimiy va do'stona bo'l
- Agar savol tushunarsiz bo'lsa, qayta so'ra
"""


class LLMAgent:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []

    def chat(self, user_message: str) -> str:
        """Foydalanuvchi xabariga javob beradi."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
        })

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=self.conversation_history,
        )

        assistant_message = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message,
        })

        return assistant_message

    def reset(self):
        """Suhbat tarixini tozalaydi."""
        self.conversation_history = []
