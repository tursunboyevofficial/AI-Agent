"""
Kino Agent moduli — Internetdan kino haqida ma'lumot topadi va o'zbekchaga tarjima qiladi
Wikipedia API (bepul, kalitsiz)
"""

import requests
import wikipediaapi
from deep_translator import GoogleTranslator


class MovieAgent:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia("TarjimonAgent/1.0", "en")
        self.wiki_ru = wikipediaapi.Wikipedia("TarjimonAgent/1.0", "ru")

    def _search_wikipedia(self, query: str, lang: str = "en") -> list:
        """Wikipedia search API orqali sahifa nomlarini topadi."""
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": query + " film",
            "limit": 10,
            "format": "json",
        }
        try:
            res = requests.get(url, params=params, timeout=10)
            return res.json()[1] if res.status_code == 200 else []
        except Exception:
            return []

    def _find_film_page(self, movie_name: str):
        """Kinoni topish — avval search, keyin to'g'ridan-to'g'ri."""
        # 1. Wikipedia Search API bilan qidirish
        results = self._search_wikipedia(movie_name, "en")

        # "film" so'zi bor natijalarni birinchi ko'rish
        film_results = [r for r in results if "film" in r.lower()]
        other_results = [r for r in results if "film" not in r.lower()]
        ordered = film_results + other_results

        for title in ordered:
            if "disambiguation" in title.lower():
                continue
            page = self.wiki.page(title)
            if page.exists() and len(page.summary) > 100:
                return page, "en"

        # 2. To'g'ridan-to'g'ri qidirish
        direct_queries = [
            f"{movie_name} (film)",
            f"{movie_name} (2024 film)",
            f"{movie_name} (2023 film)",
            movie_name,
        ]
        for q in direct_queries:
            page = self.wiki.page(q)
            if page.exists() and "disambiguation" not in page.title.lower() and len(page.summary) > 100:
                return page, "en"

        # 3. Ruscha qidirish
        results_ru = self._search_wikipedia(movie_name, "ru")
        film_ru = [r for r in results_ru if "фильм" in r.lower() or "film" in r.lower()]
        for title in film_ru + results_ru:
            page = self.wiki_ru.page(title)
            if page.exists() and len(page.summary) > 100:
                return page, "ru"

        return None, None

    def search_movie(self, movie_name: str) -> dict:
        """Kino haqida ma'lumot qidiradi va o'zbekchaga tarjima qiladi."""
        page, source_lang = self._find_film_page(movie_name)

        if not page:
            return {
                "found": False,
                "title": movie_name,
                "summary_uz": f"'{movie_name}' kino topilmadi. Inglizcha nomi bilan qidirib ko'ring (masalan: Inception, Titanic, Avatar).",
                "summary_original": "",
                "url": "",
            }

        # Qisqartirish (5 gap)
        summary = page.summary
        sentences = summary.split(". ")
        short_summary = ". ".join(sentences[:5]) + "."

        # O'zbekchaga tarjima
        try:
            summary_uz = GoogleTranslator(source=source_lang, target="uz").translate(short_summary)
        except Exception:
            summary_uz = short_summary

        return {
            "found": True,
            "title": page.title,
            "summary_uz": summary_uz,
            "summary_original": short_summary,
            "url": page.fullurl,
        }

    def get_popular_movies(self) -> list:
        """Mashhur kinolar ro'yxati."""
        return [
            {"name": "Inception", "year": 2010, "uz_name": "Tush ichida tush"},
            {"name": "The Shawshank Redemption", "year": 1994, "uz_name": "Shoushenk qo'rg'oni"},
            {"name": "Interstellar", "year": 2014, "uz_name": "Yulduzlararo"},
            {"name": "The Dark Knight", "year": 2008, "uz_name": "Qorong'u ritsar"},
            {"name": "Titanic", "year": 1997, "uz_name": "Titanik"},
            {"name": "Gladiator", "year": 2000, "uz_name": "Gladiator"},
            {"name": "The Matrix", "year": 1999, "uz_name": "Matriks"},
            {"name": "Forrest Gump", "year": 1994, "uz_name": "Forrest Gamp"},
            {"name": "Avatar", "year": 2009, "uz_name": "Avatar"},
            {"name": "Parasite", "year": 2019, "uz_name": "Parazit"},
        ]
