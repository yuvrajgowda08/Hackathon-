import ollama
from src.llm_fallback import run_llm


def generate_bibtex(text):

    prompt = f"""
Extract citation information from the research paper text.

Find if possible:
- Title
- Authors
- Year
- Journal / Conference

Then generate a BibTeX entry.

Paper text:
{text}

Return only the BibTeX entry.
"""

    bibtex = run_llm(prompt)

    return bibtex