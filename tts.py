"""
Text-to-Speech modul — Toza o'zbek ovozi (Microsoft Edge TTS)
Qo'llab-quvvatlanadigan ovozlar:
  - uz-UZ-SardorNeural (erkak)
  - uz-UZ-MadinaNeural (ayol)
"""

import asyncio
import tempfile
import os
import edge_tts
import pygame

# Har bir til uchun ovoz
VOICE_MAP = {
    "uz": "uz-UZ-SardorNeural",
    "ru": "ru-RU-DmitryNeural",
    "en": "en-US-ChristopherNeural",
    "tr": "tr-TR-AhmetNeural",
    "ar": "ar-SA-HamedNeural",
    "zh": "zh-CN-YunxiNeural",
    "ko": "ko-KR-InJoonNeural",
    "de": "de-DE-ConradNeural",
    "fr": "fr-FR-HenriNeural",
    "es": "es-ES-AlvaroNeural",
    "ja": "ja-JP-KeitaNeural",
    "hi": "hi-IN-MadhurNeural",
    "it": "it-IT-DiegoNeural",
}


class TextToSpeech:
    def __init__(self):
        pygame.mixer.init()

    def speak(self, text: str, lang_code: str = "uz"):
        """Matnni toza ovozda aytadi."""
        voice = VOICE_MAP.get(lang_code, "uz-UZ-SardorNeural")
        asyncio.run(self._speak_async(text, voice))

    async def _speak_async(self, text: str, voice: str):
        """Edge TTS orqali ovoz yaratish va play qilish."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            temp_path = f.name

        try:
            tts = edge_tts.Communicate(text, voice)
            await tts.save(temp_path)

            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
        finally:
            pygame.mixer.music.unload()
            os.remove(temp_path)

    def speak_to_file(self, text: str, lang_code: str = "uz") -> bytes:
        """Matnni ovozga aylantirib, bytes qaytaradi (web uchun)."""
        voice = VOICE_MAP.get(lang_code, "uz-UZ-SardorNeural")
        return asyncio.run(self._speak_to_bytes(text, voice))

    async def _speak_to_bytes(self, text: str, voice: str) -> bytes:
        """Edge TTS orqali ovoz yaratib bytes qaytaradi."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            temp_path = f.name

        try:
            tts = edge_tts.Communicate(text, voice)
            await tts.save(temp_path)
            with open(temp_path, "rb") as f:
                return f.read()
        finally:
            os.remove(temp_path)
