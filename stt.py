"""
Speech-to-Text modul — Ovozni matnga aylantiradi
Google Speech Recognition (bepul) + sounddevice (mikrofon)
"""

import speech_recognition as sr
import sounddevice as sd
import numpy as np
from config import get_speech_code


class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000

    def listen(self, lang_code: str = "uz", duration: int = 7) -> str:
        """
        Mikrofondan ovoz yozib oladi va matnga aylantiradi.
        lang_code: til kodi (uz, ru, en, tr, ...)
        duration: necha soniya tinglash
        """
        speech_code = get_speech_code(lang_code)

        print(f"\n🎤 Gapiring... ({duration} soniya)")

        # Ovoz yozib olish
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
        )
        sd.wait()
        print("✅ Ovoz yozib olindi!")

        # SpeechRecognition formatiga aylantirish
        audio_bytes = audio_data.tobytes()
        audio = sr.AudioData(audio_bytes, self.sample_rate, 2)

        try:
            text = self.recognizer.recognize_google(audio, language=speech_code)
            print(f"📝 Aniqlandi: {text}")
            return text
        except sr.UnknownValueError:
            print("⚠️  Ovoz tushunilmadi, qayta gapiring...")
            return ""
        except sr.RequestError as e:
            print(f"❌ Xatolik: {e}")
            return ""
