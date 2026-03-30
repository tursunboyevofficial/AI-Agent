# Martis — O'zbek tilida ishlaydigan AI Agent

O'zbek tilida ovozli suhbat, tarjima, kino ma'lumotlari va haqiqiy ma'lumotlar bilan ishlaydigan sun'iy intellekt yordamchi.

**Demo:** https://ai-agent-ruj2.onrender.com

## Imkoniyatlari

### 🗣 Ovozli Suhbat
- "Martis" deb chaqiring — agent "Labbay!" deydi va tinglaydi
- Har qanday savolga o'zbekcha javob beradi
- Toza o'zbek ovozida gapiradi (Microsoft Edge TTS — Sardor Neural)
- Groq API (Llama 3.3 70B) — aqlli va tez javoblar

### 🌐 Tarjimon (13 til)
- O'zbek, Rus, Ingliz, Turk, Arab, Xitoy, Koreys, Nemis, Fransuz, Ispan, Yapon, Hind, Italyan
- Matnli va ovozli tarjima
- Har bir til uchun alohida Neural ovoz

### 🎬 Kino
- Kino nomini yozing — o'zbekcha qisqacha mazmunini beradi
- Wikipedia API orqali ma'lumot oladi
- 10 ta mashhur kino tayyor ro'yxati
- Ovozda eshitish imkoniyati

### 📊 Haqiqiy Ma'lumotlar (jonli internet orqali)
- **Ob-havo** — istalgan shahar uchun (wttr.in API)
- **Dollar kursi** — O'zbekiston Markaziy banki (cbu.uz)
- **Vaqt va sana** — tizim soati

## Texnologiyalar

| Qism | Texnologiya | Vazifasi |
|------|------------|----------|
| Backend | Flask (Python) | Web server |
| LLM | Groq API (Llama 3.3 70B) | Aqlli javoblar |
| TTS | Microsoft Edge TTS | Ovozga aylantirish |
| STT | Web Speech API (brauzer) | Ovozni matnga |
| Tarjima | Google Translate (deep-translator) | 13 til tarjimasi |
| Kino | Wikipedia API | Kino ma'lumotlari |
| Ob-havo | wttr.in | Haqiqiy ob-havo |
| Valyuta | cbu.uz | Dollar/Evro/Rubl kursi |
| Deploy | Render.com | Hosting (bepul) |

## Loyiha Tuzilishi

```
AI-Agent/
├── app.py              # Flask web server (asosiy)
├── chatbot.py          # Martis suhbat agenti (Groq LLM)
├── translator.py       # Tarjima moduli (Google Translate)
├── movies.py           # Kino qidiruv moduli (Wikipedia)
├── tools.py            # Ob-havo, valyuta, vaqt asboblari
├── tts.py              # Text-to-Speech (Edge TTS, 13 ovoz)
├── stt.py              # Speech-to-Text (lokal mikrofon)
├── config.py           # Tillar konfiguratsiyasi
├── agent.py            # Terminal rejimi (lokal)
├── llm.py              # LLM modul (Claude/Gemini)
├── requirements.txt    # Python kutubxonalari
├── .env.example        # API kalitlari namunasi
├── .gitignore          # Git e'tiborsiz fayllar
└── templates/
    └── index.html      # Web UI (HTML/CSS/JS)
```

## O'rnatish

### 1. Reponi klonlash
```bash
git clone https://github.com/tursunboyevofficial/AI-Agent.git
cd AI-Agent
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. API kalitini sozlash
```bash
cp .env.example .env
```
`.env` faylga Groq API kalitini qo'shing:
```
GROQ_API_KEY=sizning_kalit
```
Groq kalitini bepul oling: https://console.groq.com/keys

### 4. Ishga tushirish
```bash
python app.py
```
Brauzerda oching: http://localhost:8080

## API Kalitlari

| API | Narx | Qayerdan olish |
|-----|------|----------------|
| **Groq** (majburiy) | Bepul | https://console.groq.com/keys |
| Gemini (ixtiyoriy) | Bepul | https://aistudio.google.com/apikey |

## Foydalanish

### Ovozli suhbat (Chrome brauzer kerak)
1. Sahifadagi doirani bosing
2. "Martis" deb ayting
3. Agent "Labbay!" deydi — savolingizni ayting
4. Martis o'zbekcha javob beradi + ovozda aytadi

### Tarjimon
1. Manba va maqsad tilni tanlang
2. Matn kiriting yoki 🎤 bosib gapiring
3. Tarjima + ovozda eshiting

### Kino
1. Kino nomini inglizcha yozing (masalan: Inception)
2. O'zbekcha mazmuni chiqadi
3. 🔊 bosib ovozda eshiting

## Muallif

**Tursunboyev** — [GitHub](https://github.com/tursunboyevofficial)

---

*Barcha API'lar bepul. Hech qanday pullik xizmat ishlatilmagan.*
