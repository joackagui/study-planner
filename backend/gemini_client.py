import os
from typing import List, Dict

import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()

def perform_web_search(query: str, max_results: int = 6) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                if not isinstance(r, dict):
                    continue
                title = r.get("title") or ""
                href = r.get("href") or ""
                body = r.get("body") or ""
                if title and href:
                    results.append({"title": title, "href": href, "body": body})
        return results
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return []

class GeminiClient:
    def __init__(self):
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            self.chat = self.model.start_chat(history=[])
        except Exception as e:
            print(f"Error configuring Gemini API: {e}")
            self.chat = None

    def generate_response(self, user_input: str) -> str:
        if not self.chat:
            return "AI service is not configured correctly."

        try:
            text = user_input or ""
            lower = text.strip().lower()

            search_query = None
            if lower.startswith("search:"):
                search_query = text.split(":", 1)[1].strip()
            elif lower.startswith("/search "):
                search_query = text.split(" ", 1)[1].strip()

            if search_query:
                web_results = perform_web_search(search_query, max_results=6)
                if not web_results:
                    return "I could not retrieve web results right now. Please try again."

                refs_lines = []
                for idx, item in enumerate(web_results, start=1):
                    refs_lines.append(
                        f"[{idx}] {item['title']} — {item['href']}\n{item['body']}"
                    )
                refs_block = "\n\n".join(refs_lines)

                system_prompt = (
                    "You are an AI research assistant. Use the provided web search results to answer the user query. "
                    "Synthesize concisely, cite sources inline like [1], [2] where relevant, and include a brief summary."
                )

                composed = (
                    f"<system>\n{system_prompt}\n</system>\n"
                    f"<user_query>\n{search_query}\n</user_query>\n"
                    f"<web_results>\n{refs_block}\n</web_results>"
                )
                response = self.chat.send_message(composed)
                return response.text

            response = self.chat.send_message(text)
            return response.text

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error processing your request."