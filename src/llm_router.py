from langgraph.graph import StateGraph
import ollama
from src.gemini_model import gemini_generate


def ollama_node(state):

    prompt = state["prompt"]

    try:

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        return {"result": response["message"]["content"]}

    except:

        return {"error": "ollama_failed"}


def gemini_node(state):

    prompt = state["prompt"]

    result = gemini_generate(prompt)

    return {"result": result}


def router(state):

    if "error" in state:

        return "gemini"

    return "end"


workflow = StateGraph(dict)

workflow.add_node("ollama", ollama_node)
workflow.add_node("gemini", gemini_node)

workflow.set_entry_point("ollama")

workflow.add_conditional_edges(
    "ollama",
    router,
    {
        "gemini": "gemini",
        "end": "__end__"
    }
)

app = workflow.compile()