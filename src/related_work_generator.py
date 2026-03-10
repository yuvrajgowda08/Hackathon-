import ollama
from src.llm_fallback import run_llm


def generate_related_work(papers_text):

    combined_text = "\n\n".join(papers_text)

    prompt = f"""
You are an academic research assistant.

Using the research papers below, generate a "Related Work" section
in IEEE style.

Guidelines:
- Use academic writing style
- Mention different approaches used in the papers
- Include citations like [1], [2], [3]
- Highlight key methods and datasets

Research Papers:
{combined_text}

Write a well-structured "Related Work" section.
"""

    return run_llm(prompt)