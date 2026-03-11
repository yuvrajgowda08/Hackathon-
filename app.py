import streamlit as st
import requests

from src.pdf_processor import extract_text_from_pdf
from src.rag_pipeline import summarize_paper
from src.bibtex import generate_bibtex
from src.citation_extractor import extract_citations
from src.related_work_generator import generate_related_work
from src.embeddings import create_embeddings, embed_query
from src.vector_store import build_vector_store, search
from src.chunker import chunk_text
from src.llm_fallback import run_llm
from src.paper_similarity import compute_similarity

# -----------------------------------
# CACHE DOCUMENT PROCESSING
# -----------------------------------
@st.cache_resource
def process_documents(uploaded_files):

    all_chunks = []
    all_papers_text = []

    for file in uploaded_files:

        file.seek(0)

        text = extract_text_from_pdf(file)

        all_papers_text.append(text)

        chunks = chunk_text(text)

        all_chunks.extend(chunks)

    embeddings = create_embeddings(all_chunks)

    build_vector_store(embeddings, all_chunks)

    return all_papers_text

# -------------------------------
# CACHE SUMMARY
# -------------------------------
@st.cache_data
def cached_summary(text):
    return summarize_paper(text)

@st.cache_data
def cached_citations(text):
    return extract_citations(text)

@st.cache_data
def cached_bibtex(text):
    return generate_bibtex(text)


# -----------------------------
# Check Ollama Status
# -----------------------------
def check_ollama_status():
    try:
        r = requests.get("http://localhost:11434")
        if r.status_code == 200:
            return True
    except:
        return False


# -----------------------------
# UI
# -----------------------------
st.title("Research Paper RAG Assistant")
st.write("Upload research papers and analyze them using AI.")


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("System Status")

ollama_running = check_ollama_status()

if ollama_running:
    st.sidebar.success("🟢 Ollama Running")
    st.sidebar.write("Model: Llama3")
else:
    st.sidebar.warning("🔴 Ollama Not Running")
    st.sidebar.write("Using Gemini Backup")


# -----------------------------
# Upload PDFs
# -----------------------------
uploaded_files = st.file_uploader(
    "Upload PDF Papers",
    type="pdf",
    accept_multiple_files=True
)

st.sidebar.write(f"📄 Papers Loaded: {len(uploaded_files)}")


# -----------------------------
# Process Documents
# -----------------------------
if uploaded_files:

    all_papers_text = process_documents(uploaded_files)

    st.success("Documents processed and vector database created")


    st.divider()

    # -----------------------------
    # Display Results Per Paper
    # -----------------------------
    for file in uploaded_files:

        file.seek(0)

        text = extract_text_from_pdf(file)

        st.markdown("---")
        st.subheader(f"Paper: {file.name}")

        # Summary
        with st.spinner("Generating summary..."):
            summary = cached_summary(text)

        st.write("### Summary")
        st.write(summary)

        # Citations
        with st.spinner("Extracting citations..."):
            citations = cached_citations(text)

        st.write("### Citations Found")
        st.write(citations)

        # BibTeX (AUTOMATIC)
        with st.spinner("Generating BibTeX..."):
            bibtex = cached_bibtex(text)

        st.write("### BibTeX Citation")
        st.code(bibtex)


# -----------------------------
# Literature Review
# -----------------------------
if uploaded_files:

    st.divider()

    if st.button("Generate Literature Review (Related Work)"):

     with st.spinner("Generating related work section..."):

        st.session_state.related_work = generate_related_work(all_papers_text)

if "related_work" in st.session_state:
    st.write("## Generated Related Work Section")
    st.write(st.session_state.related_work)


# -----------------------------
# Ask Question (RAG)
# -----------------------------
if uploaded_files:

    st.divider()

    question = st.text_input(
        "Ask a question about the uploaded documents",
        key="question_input"
    )

    if st.button("Ask Question"):

        if question:

            with st.spinner("Searching documents..."):

                query_embedding = embed_query(question)

                results = search(query_embedding)

            if results:

                context = "\n".join(results)

                prompt = f"""
Answer the question using the document context.

Context:
{context}

Question:
{question}
"""

                st.session_state.answer = run_llm(prompt)

            else:
                st.session_state.answer = "No relevant information found."

# display answer persistently
if "answer" in st.session_state:

    st.write("### Answer")
    st.write(st.session_state.answer)

# -----------------------------
# Paper Similarity
# -----------------------------
if uploaded_files:

    st.divider()

    st.subheader("Compare Papers")

    if len(uploaded_files) != 2:
        st.info("Upload exactly two papers to compare similarity.")

    else:

        if st.button("Compare Papers"):

            uploaded_files[0].seek(0)
            uploaded_files[1].seek(0)

            text1 = extract_text_from_pdf(uploaded_files[0])
            text2 = extract_text_from_pdf(uploaded_files[1])

            st.session_state.similarity = compute_similarity(text1, text2)

if "similarity" in st.session_state:

    similarity = st.session_state.similarity

    st.write("### Paper Similarity")
    st.write(f"Similarity Score:  **{similarity}%**")

    if similarity > 70:
        st.error("High similarity detected ⚠️ Possible plagiarism")

    elif similarity > 40:
        st.warning("Moderate similarity")

    else:
        st.success("Low similarity")