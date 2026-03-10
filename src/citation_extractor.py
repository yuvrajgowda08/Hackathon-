import ollama
from src.llm_fallback import run_llm


def extract_citations(text):

    prompt = f"""
From the research paper text below, extract the list of references or citations.

If a References section exists, list the citations.

Return them in a clean numbered list like:

[1] Author, Title, Year
[2] Author, Title, Year

Text:
{text}
"""

    return run_llm(prompt)