"""
Martis uchun asboblar — haqiqiy ma'lumotlarni internetdan oladi
"""

import requests
from datetime import datetime


def get_weather(city: str = "Tashkent") -> str:
    """Haqiqiy ob-havo ma'lumotini oladi (wttr.in — bepul, kalitsiz)."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        res = requests.get(url, timeout=10)
        data = res.json()

        current = data["current_condition"][0]
        temp = current["temp_C"]
        feels = current["FeelsLikeC"]
        humidity = current["humidity"]
        desc_uz = _translate_weather(current["weatherDesc"][0]["value"])
        wind = current["windspeedKmph"]

        # Bugungi prognoz
        today = data["weather"][0]
        max_temp = today["maxtempC"]
        min_temp = today["mintempC"]

        return (
            f"{city} shahrida hozir: {temp}°C ({desc_uz}). "
            f"His qilish: {feels}°C. Namlik: {humidity}%. Shamol: {wind} km/s. "
            f"Bugun: {min_temp}°C dan {max_temp}°C gacha."
        )
    except Exception as e:
        return f"{city} uchun ob-havo ma'lumotini olishda xatolik: {str(e)}"


def get_time_info() -> str:
    """Hozirgi vaqt va sana."""
    now = datetime.now()
    days_uz = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    months_uz = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
                 "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
    day_name = days_uz[now.weekday()]
    month_name = months_uz[now.month - 1]
    return f"Hozir soat {now.strftime('%H:%M')}. Bugun {day_name}, {now.day}-{month_name} {now.year}-yil."


def get_currency() -> str:
    """Dollar/So'm kursini oladi."""
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        res = requests.get(url, timeout=10)
        data = res.json()

        rates = {}
        for item in data:
            if item["Ccy"] in ["USD", "EUR", "RUB"]:
                rates[item["Ccy"]] = item["Rate"]

        parts = []
        if "USD" in rates:
            parts.append(f"1 USD = {rates['USD']} so'm")
        if "EUR" in rates:
            parts.append(f"1 EUR = {rates['EUR']} so'm")
        if "RUB" in rates:
            parts.append(f"1 RUB = {rates['RUB']} so'm")

        return "Bugungi kurs: " + ", ".join(parts) + "."
    except Exception:
        return "Valyuta kursini olishda xatolik yuz berdi."


def _translate_weather(desc: str) -> str:
    """Ob-havo tavsifini o'zbekchaga tarjima."""
    translations = {
        "sunny": "quyoshli", "clear": "ochiq", "partly cloudy": "qisman bulutli",
        "cloudy": "bulutli", "overcast": "to'liq bulutli", "mist": "tuman",
        "fog": "tuman", "rain": "yomg'ir", "light rain": "yengil yomg'ir",
        "heavy rain": "kuchli yomg'ir", "snow": "qor", "light snow": "yengil qor",
        "thunderstorm": "momaqaldiroq", "drizzle": "mayda yomg'ir",
        "patchy rain possible": "ba'zan yomg'ir mumkin",
        "patchy snow possible": "ba'zan qor mumkin",
        "patchy rain nearby": "atrofda yomg'ir",
        "light drizzle": "maydalab yomg'ir",
        "moderate rain": "o'rtacha yomg'ir",
    }
    return translations.get(desc.lower().strip(), desc)


def process_with_tools(message: str) -> str:
    """Xabardagi so'rovni aniqlaydi va mos asbobni ishlatadi."""
    msg = message.lower()

    # Ob-havo
    if any(w in msg for w in ["ob-havo", "havo", "harorat", "temperatura", "sovuq", "issiq", "yomg'ir", "qor"]):
        # Shaharni aniqlash
        cities = {
            "toshkent": "Tashkent", "samarqand": "Samarkand", "buxoro": "Bukhara",
            "xiva": "Khiva", "farg'ona": "Fergana", "andijon": "Andijan",
            "namangan": "Namangan", "navoiy": "Navoi", "qarshi": "Qarshi",
            "nukus": "Nukus", "jizzax": "Jizzakh", "termiz": "Termez",
            "moskva": "Moscow", "istanbul": "Istanbul", "dubai": "Dubai",
            "london": "London", "new york": "New York", "tokyo": "Tokyo",
            "seoul": "Seoul", "pekin": "Beijing", "berlin": "Berlin",
        }
        city = "Tashkent"  # standart
        for uz_name, en_name in cities.items():
            if uz_name in msg:
                city = en_name
                break
        return get_weather(city)

    # Vaqt/sana
    if any(w in msg for w in ["soat", "vaqt", "sana", "bugun", "kun"]):
        return get_time_info()

    # Valyuta
    if any(w in msg for w in ["dollar", "kurs", "valyuta", "som", "so'm", "evro", "rubl"]):
        return get_currency()

    return None  # Mos asbob topilmadi
