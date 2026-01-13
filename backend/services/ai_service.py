import os
import google.generativeai as genai
from dotenv import load_dotenv

# Ładujemy zmienne środowiskowe
load_dotenv()

# Konfiguracja API key
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_ai_response(user_message, user_context=None):
    """
    Generuje odpowiedź z Gemini.
    user_context: Opcjonalny słownik z danymi o zdrowiu użytkownika (wiek, waga itp.)
    """
    try:
        # Budowanie promptu systemowego
        system_instruction = """
        Jesteś Asystentem Zdrowia (AI Health Assistant).
        Twoim celem jest edukacja zdrowotna i motywacja.
        
        Zasady:
        1. Nie jesteś lekarzem. Zawsze zalecaj kontakt ze specjalistą w poważnych sprawach.
        2. Odpowiadaj krótko, konkretnie i empatycznie.
        3. Opieraj się na naukowych faktach dotyczących cukrzycy i zdrowego stylu życia.
        """

        # Jeśli mamy dane o użytkowniku, dodajemy je do kontekstu dla modelu
        if user_context:
            context_str = f"\nKontekst pacjenta: Płeć: {user_context.get('sex')}, Wiek: {user_context.get('age')}"
            if user_context.get('high_bp'): context_str += ", Nadciśnienie: TAK"
            if user_context.get('high_chol'): context_str += ", Wysoki cholesterol: TAK"
            if user_context.get('bmi'): context_str += f", BMI: {user_context.get('bmi')}"
            
            system_instruction += context_str

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )

        response = model.generate_content(user_message)
        return response.text

    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Przepraszam, chwilowo nie mogę połączyć się z serwerem AI."