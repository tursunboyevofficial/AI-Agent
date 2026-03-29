"""
Tarjima modul — Google Translate orqali (BEPUL, API kalitsiz!)
"""

from deep_translator import GoogleTranslator
from config import get_lang_name


class Translator:
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Matnni bir tildan boshqa tilga tarjima qiladi."""
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
