"""
🤖 AI Agent — Tarjimon, Kino, Suhbat
Ishga tushirish: python3 app.py
Brauzerda: http://localhost:8080
"""

import os
import io
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from translator import Translator
from movies import MovieAgent
from chatbot import ChatBot
from tts import TextToSpeech
from config import LANGUAGES, get_lang_name

load_dotenv()

app = Flask(__name__)
translator = Translator()
movie_agent = MovieAgent()
tts = TextToSpeech()
chatbot = ChatBot(
    groq_key=os.getenv("GROQ_API_KEY"),
    gemini_key=os.getenv("GEMINI_API_KEY"),
)


@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)


@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.json
    text = data.get("text", "").strip()
    source = data.get("source", "uz")
    target = data.get("target", "en")

    if not text:
        return jsonify({"error": "Matn kiritilmagan"}), 400

    try:
        translation = translator.translate(text, source, target)
        return jsonify({
            "translation": translation,
            "source_name": get_lang_name(source),
            "target_name": get_lang_name(target),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "uz")

    try:
        audio_bytes = tts.speak_to_file(text, lang_code=lang)
        return send_file(io.BytesIO(audio_bytes), mimetype="audio/mp3")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/movie/search", methods=["POST"])
def movie_search():
    data = request.json
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Kino nomi kiritilmagan"}), 400

    try:
        result = movie_agent.search_movie(name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/movie/popular")
def popular_movies():
    return jsonify(movie_agent.get_popular_movies())


@app.route("/chat", methods=["POST"])
def chat():
    """Ovozli suhbat — foydalanuvchi yozadi/gapiradi, agent o'zbekcha javob beradi."""
    data = request.json
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Xabar kiritilmagan"}), 400

    try:
        response = chatbot.chat(message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat/reset", methods=["POST"])
def chat_reset():
    chatbot.reset()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI AGENT — Tarjimon | Kino | Suhbat")
    print("=" * 50)
    print("🚀 Brauzerda oching: http://localhost:8080")
    print("⏹  To'xtatish: Ctrl+C")
    print("=" * 50)
    app.run(debug=True, port=8080)
