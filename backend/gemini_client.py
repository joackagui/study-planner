# backend/gemini_client.py
import os
from typing import List, Dict
from dotenv import load_dotenv
from duckduckgo_search import DDGS

from google import genai

load_dotenv()


def perform_web_search(query: str, max_results: int = 6) -> List[Dict[str, str]]:
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                if not isinstance(r, dict):
                    continue
                results.append({
                    "title": r.get("title", ""),
                    "href": r.get("href", ""),
                    "body": r.get("body", "")
                })
    except Exception as e:
        print("Search error:", e)
    return results


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        # MODELO ACTUAL Y SOPORTADO
        self.model = "gemini-2.0-flash"

    def generate_response(self, user_input: str) -> str:
        try:
            lower = user_input.lower().strip()

            if lower.startswith("search:"):
                query = user_input.split(":", 1)[1]
                results = perform_web_search(query)

                context = "\n\n".join(
                    f"{i+1}. {r['title']} ({r['href']})\n{r['body']}"
                    for i, r in enumerate(results)
                )

                prompt = f"""
                Usa la siguiente información para responder la pregunta del usuario.

                Pregunta:
                {query}

                Información:
                {context}
                """

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                return response.text

            response = self.client.models.generate_content(
                model=self.model,
                contents=user_input
            )
            return response.text

        except Exception as e:
            print("Gemini error:", e)
            return "Error al generar respuesta con Gemini."