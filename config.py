"""
Tarjimon Agent konfiguratsiyasi — qo'llab-quvvatlanadigan tillar
"""

# Qo'llab-quvvatlanadigan tillar
# format: {kod: (til_nomi, google_speech_kodi, gtts_kodi)}
LANGUAGES = {
    "uz": ("O'zbekcha", "uz-UZ", "tr"),  # gTTS o'zbekchani qo'llamaydi, turk tili o'xshash
    "ru": ("Ruscha", "ru-RU", "ru"),
    "en": ("Inglizcha", "en-US", "en"),
    "tr": ("Turkcha", "tr-TR", "tr"),
    "ar": ("Arabcha", "ar-SA", "ar"),
    "zh": ("Xitoycha", "zh-CN", "zh-CN"),
    "ko": ("Koreyscha", "ko-KR", "ko"),
    "de": ("Nemischa", "de-DE", "de"),
    "fr": ("Fransuzcha", "fr-FR", "fr"),
    "es": ("Ispancha", "es-ES", "es"),
    "ja": ("Yaponcha", "ja-JP", "ja"),
    "hi": ("Hindcha", "hi-IN", "hi"),
    "it": ("Italyancha", "it-IT", "it"),
}


def get_language_list() -> str:
    """Tillar ro'yxatini chiroyli formatda qaytaradi."""
    lines = []
    for code, (name, _, _) in LANGUAGES.items():
        lines.append(f"  {code} — {name}")
    return "\n".join(lines)


def get_speech_code(lang_code: str) -> str:
    """Google Speech Recognition uchun til kodini qaytaradi."""
    return LANGUAGES.get(lang_code, ("", "en-US", ""))[1]


def get_tts_code(lang_code: str) -> str:
    """Google TTS uchun til kodini qaytaradi."""
    return LANGUAGES.get(lang_code, ("", "", "en"))[2]


def get_lang_name(lang_code: str) -> str:
    """Til nomini qaytaradi."""
    return LANGUAGES.get(lang_code, ("Noma'lum", "", ""))[0]
