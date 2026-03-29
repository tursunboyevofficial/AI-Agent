"""
🌐 O'zbek Tarjimon AI Agent (Bepul — Gemini API)

Ovozda gapiring — istalgan tilga tarjima qilib aytadi!
13 ta til qo'llab-quvvatlanadi.

Ishlatish: python3 agent.py
"""

from config import LANGUAGES, get_language_list, get_lang_name
from stt import SpeechToText
from translator import Translator
from tts import TextToSpeech


def show_menu():
    """Asosiy menyuni ko'rsatadi."""
    print("\n" + "=" * 50)
    print("🌐 TARJIMON AI AGENT")
    print("=" * 50)
    print("\nRejimni tanlang:\n")
    print("  1 — 🎤 Ovozli tarjima (gapiring → tarjima)")
    print("  2 — ⌨️  Matnli tarjima (yozing → tarjima)")
    print("  3 — 🔄 Suhbat rejimi (ikki kishi o'rtasida)")
    print("  4 — 📋 Tillar ro'yxati")
    print("  0 — ❌ Chiqish")
    print()


def select_languages() -> tuple:
    """Foydalanuvchidan manba va maqsad tilni so'raydi."""
    print("\n📋 Tillar:")
    print(get_language_list())

    source = input("\n➡️  Qaysi tildan? (masalan: uz): ").strip().lower()
    if source not in LANGUAGES:
        print("❌ Noto'g'ri til kodi!")
        return None, None

    target = input("➡️  Qaysi tilga? (masalan: en): ").strip().lower()
    if target not in LANGUAGES:
        print("❌ Noto'g'ri til kodi!")
        return None, None

    if source == target:
        print("❌ Manba va maqsad til bir xil bo'lmasligi kerak!")
        return None, None

    print(f"\n✅ {get_lang_name(source)} → {get_lang_name(target)}")
    return source, target


def voice_translate(stt, translator, tts):
    """Ovozli tarjima rejimi."""
    source, target = select_languages()
    if not source:
        return

    print(f"\n🎤 {get_lang_name(source)} tilida gapiring — {get_lang_name(target)} tiliga tarjima qilinadi")
    print("⏹  Menyuga qaytish uchun Ctrl+C bosing\n")

    try:
        while True:
            text = stt.listen(lang_code=source)
            if not text:
                continue

            print("🧠 Tarjima qilmoqda...")
            translation = translator.translate(text, source, target)
            print(f"💬 Tarjima: {translation}")

            tts.speak(translation, lang_code=target)
            print("-" * 40)
    except KeyboardInterrupt:
        print("\n⬅️  Menyuga qaytildi")


def text_translate(translator, tts):
    """Matnli tarjima rejimi."""
    source, target = select_languages()
    if not source:
        return

    print(f"\n⌨️  {get_lang_name(source)} tilida yozing — {get_lang_name(target)} tiliga tarjima qilinadi")
    print("⏹  Menyuga qaytish uchun 'q' yozing\n")

    while True:
        text = input(f"📝 [{get_lang_name(source)}]: ").strip()
        if text.lower() == "q":
            print("⬅️  Menyuga qaytildi")
            break
        if not text:
            continue

        print("🧠 Tarjima qilmoqda...")
        translation = translator.translate(text, source, target)
        print(f"💬 [{get_lang_name(target)}]: {translation}")

        tts.speak(translation, lang_code=target)
        print("-" * 40)


def conversation_mode(stt, translator, tts):
    """Suhbat rejimi — ikki kishi o'rtasida tarjimonlik."""
    print("\n🔄 SUHBAT REJIMI")
    print("Ikki kishi gapiradi — agent o'rtada tarjimon bo'ladi\n")

    print("📋 Tillar:")
    print(get_language_list())

    lang1 = input("\n👤 1-kishi tili (masalan: uz): ").strip().lower()
    lang2 = input("👤 2-kishi tili (masalan: en): ").strip().lower()

    if lang1 not in LANGUAGES or lang2 not in LANGUAGES:
        print("❌ Noto'g'ri til kodi!")
        return

    print(f"\n✅ {get_lang_name(lang1)} ↔ {get_lang_name(lang2)}")
    print("⏹  To'xtatish uchun Ctrl+C bosing\n")

    current_speaker = 1
    try:
        while True:
            if current_speaker == 1:
                src, tgt = lang1, lang2
                print(f"\n👤 1-kishi ({get_lang_name(src)}) gapirsin:")
            else:
                src, tgt = lang2, lang1
                print(f"\n👤 2-kishi ({get_lang_name(src)}) gapirsin:")

            text = stt.listen(lang_code=src)
            if not text:
                continue

            print("🧠 Tarjima qilmoqda...")
            translation = translator.translate(text, src, tgt)
            print(f"💬 Tarjima ({get_lang_name(tgt)}): {translation}")

            tts.speak(translation, lang_code=tgt)
            print("-" * 40)

            current_speaker = 2 if current_speaker == 1 else 1

    except KeyboardInterrupt:
        print("\n⬅️  Menyuga qaytildi")


def main():
    print("⏳ Tarjimon agent yuklanmoqda...")
    stt = SpeechToText()
    translator = Translator()
    tts = TextToSpeech()
    print("✅ Tayyor!\n")

    try:
        while True:
            show_menu()
            choice = input("Tanlang (0-4): ").strip()

            if choice == "1":
                voice_translate(stt, translator, tts)
            elif choice == "2":
                text_translate(translator, tts)
            elif choice == "3":
                conversation_mode(stt, translator, tts)
            elif choice == "4":
                print("\n📋 Qo'llab-quvvatlanadigan tillar:\n")
                print(get_language_list())
            elif choice == "0":
                print("\n👋 Xayr! Tarjimon agent to'xtatildi.")
                break
            else:
                print("❌ Noto'g'ri tanlov!")

    except KeyboardInterrupt:
        print("\n\n👋 Xayr!")


if __name__ == "__main__":
    main()
