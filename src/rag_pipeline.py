import ollama
from src.llm_fallback import run_llm


def summarize_paper(text):

    prompt = f"""
You are an academic research assistant.

Summarize the following research paper clearly.

Include:
- Research problem
- Method used
- Dataset (if mentioned)
- Key results
- Contributions

Paper Text:
{text}

Write a clear academic summary.
"""

    summary = run_llm(prompt)

    return summary