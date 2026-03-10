import ollama
from src.gemini_model import generate_with_gemini


def run_llm(prompt):

    try:

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    except Exception as e:

        print("⚠️ Ollama failed, switching to Gemini")

        return generate_with_gemini(prompt)