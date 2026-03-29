"""
Martis — O'zbek tilida gaplashadigan ovozli AI Agent
Groq API (bepul, tez) yoki Gemini API ishlatadi
"""

AGENT_NAME = "Martis"

SYSTEM_PROMPT = f"""Sening isming {AGENT_NAME}. Sen o'zbek tilida gaplashadigan bilimdon yordamchisan.

MUHIM QOIDALAR:
- Har doim FAQAT o'zbek tilida javob ber
- HECH QACHON "internetdan qidiring", "saytlarga kiring", "mintaqangiz bo'yicha" dema
- HECH QACHON foydalanuvchini boshqa joyga yo'naltirma
- O'zing bilgan ma'lumotni TO'G'RIDAN-TO'G'RI aytib ber
- Agar aniq bilmasang, o'zing tahlil qilib, mantiqiy javob ber
- Qisqa, aniq va foydali javob ber (2-5 gap)
- Samimiy va do'stona bo'l
- Isming so'ralsa "{AGENT_NAME}" de

Misol:
Savol: "Toshkentda ob-havo qanday?"
NOTO'G'RI: "Ob-havo ma'lumotlari uchun saytlarga kiring"
TO'G'RI: "Toshkentda mart oyida odatda 15-20°C bo'ladi, bahorda iliq kunlar boshlanadi."

Savol: "Dollar kursi qancha?"
NOTO'G'RI: "Valyuta kursini bilish uchun bankka murojaat qiling"
TO'G'RI: "Dollar kursi taxminan 12,000-13,000 so'm atrofida."

Sen bilimdon sun'iy intellektsan — savolga o'zing javob ber, boshqa joyga yo'naltirma!"""


class ChatBot:
    """Martis — aqlli o'zbek yordamchi."""

    def __init__(self, groq_key: str = None, gemini_key: str = None):
        self.groq_client = None
        self.gemini_client = None
        self.history = []

        # 1. Groq (bepul, tez)
        if groq_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=groq_key)
                print("✅ Groq API ulandi")
            except Exception:
                pass

        # 2. Gemini (bepul)
        if not self.groq_client and gemini_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=gemini_key)
                print("✅ Gemini API ulandi")
            except Exception:
                pass

        if not self.groq_client and not self.gemini_client:
            print("⚠️  LLM API topilmadi — oddiy javoblar rejimi")

    def chat(self, user_message: str) -> str:
        """Foydalanuvchi xabariga javob beradi."""
        from tools import process_with_tools

        # 1. Avval asboblar bilan haqiqiy ma'lumot olishga harakat
        tool_result = process_with_tools(user_message)

        if tool_result:
            # Haqiqiy ma'lumot bilan LLM ga yuborish
            if self.groq_client:
                return self._chat_with_data(user_message, tool_result)
            return tool_result

        # 2. Oddiy savol — LLM ga yuborish
        if self.groq_client:
            return self._chat_groq(user_message)
        if self.gemini_client:
            return self._chat_gemini(user_message)
        return self._chat_simple(user_message)

    def _chat_with_data(self, user_message: str, data: str) -> str:
        """Haqiqiy ma'lumot bilan LLM dan chiroyli javob olish."""
        self.history.append({"role": "user", "content": user_message})

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": (
                        f"Foydalanuvchi savoli: {user_message}\n\n"
                        f"Haqiqiy ma'lumot (internetdan olingan): {data}\n\n"
                        "Shu ma'lumot asosida o'zbek tilida samimiy javob ber. "
                        "Faqat berilgan ma'lumotdan foydalaning."
                    )},
                ],
                max_tokens=300,
                temperature=0.7,
            )
            answer = response.choices[0].message.content.strip()
            self.history.append({"role": "assistant", "content": answer})
            return answer
        except Exception:
            return data  # LLM ishlamasa, xom ma'lumotni qaytarish

    def _chat_groq(self, user_message: str) -> str:
        """Groq API orqali javob (Llama modeli, juda tez)."""
        self.history.append({"role": "user", "content": user_message})

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *self.history[-10:],  # Oxirgi 10 xabar
                ],
                max_tokens=300,
                temperature=0.7,
            )
            answer = response.choices[0].message.content.strip()
            self.history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            print(f"Groq xatolik: {e}")
            return self._chat_simple(user_message)

    def _chat_gemini(self, user_message: str) -> str:
        """Gemini API orqali javob."""
        try:
            response = self.gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[{
                    "role": "user",
                    "parts": [{"text": SYSTEM_PROMPT + f"\n\nFoydalanuvchi: {user_message}"}]
                }],
            )
            return response.text.strip()
        except Exception as e:
            print(f"Gemini xatolik: {e}")
            return self._chat_simple(user_message)

    def _chat_simple(self, user_message: str) -> str:
        """API ishlamasa, oddiy javoblar."""
        msg = user_message.lower().strip()

        # Salomlashish
        if any(w in msg for w in ["salom", "assalom", "hayrli kun", "hayrli tong"]):
            return f"Assalomu alaykum! Men {AGENT_NAME}man. Sizga qanday yordam bera olaman?"

        # Ahvol so'rash
        if any(w in msg for w in ["qanday", "yaxshi", "ahvol", "qalaysi"]):
            return "Rahmat, yaxshi! Sizning ahvolingiz qalaydir? Savolingiz bo'lsa bemalol so'rang."

        # Ism
        if any(w in msg for w in ["ism", "nom", "kimsan", "kim sen", "nima ism"]):
            return f"Mening ismim {AGENT_NAME}. Men sun'iy intellekt yordamchisiman!"

        # Imkoniyatlar
        if any(w in msg for w in ["nima qila", "imkoniyat", "qila olasan", "yordam"]):
            return (f"Men {AGENT_NAME}man! Savollaringizga javob beraman, tarjima qilaman, "
                    "kinolar haqida gapirib beraman — hammasi o'zbek tilida!")

        # Rahmat
        if any(w in msg for w in ["rahmat", "tashakkur", "raxmat"]):
            return "Arzimaydi! Yana savol bo'lsa, bemalol so'rang."

        # Xayrlashish
        if any(w in msg for w in ["xayr", "ko'rishguncha", "hayr", "salomat"]):
            return "Xayr! Ko'rishguncha, yaxshi kuningiz bo'lsin!"

        # Vaqt
        if any(w in msg for w in ["vaqt", "soat", "bugun", "kun"]):
            from datetime import datetime
            now = datetime.now()
            return f"Hozir soat {now.strftime('%H:%M')}, bugun {now.strftime('%Y-yil %d-%B')}."

        # Ob-havo
        if any(w in msg for w in ["ob-havo", "havo", "sovuq", "issiq"]):
            return "Kechirasiz, hozircha ob-havo ma'lumotlariga kirishim yo'q. Lekin boshqa savollaringizga javob bera olaman!"

        # Matematika
        if any(w in msg for w in ["nechta", "qancha", "hisob", "plus", "minus"]):
            try:
                import re
                nums = re.findall(r'\d+', msg)
                if len(nums) >= 2:
                    a, b = int(nums[0]), int(nums[1])
                    if "plus" in msg or "qo'sh" in msg or "+" in msg:
                        return f"{a} + {b} = {a+b}"
                    if "minus" in msg or "ayir" in msg or "-" in msg:
                        return f"{a} - {b} = {a-b}"
                    if "ko'pay" in msg or "x" in msg or "*" in msg:
                        return f"{a} × {b} = {a*b}"
                    return f"{a} + {b} = {a+b}"
            except Exception:
                pass

        # Hech narsaga mos kelmasa
        return (f"Kechirasiz, bu savolga hozir javob bera olmayman. "
                f"Groq API kalitini qo'shsangiz, men har qanday savolga javob beraman! "
                f"console.groq.com dan bepul oling.")

    def reset(self):
        """Suhbat tarixini tozalash."""
        self.history = []
