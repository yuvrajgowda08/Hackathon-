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

def check_ollama_status():
    try:
        r = requests.get("http://localhost:11434")
        if r.status_code == 200:
            return True
    except:
        return False


st.title("Research Paper RAG Assistant")

st.write("Upload research papers and get summaries.")


uploaded_files = st.file_uploader(
    "Upload PDF Papers",
    type="pdf",
    accept_multiple_files=True
)
all_papers_text = []
st.sidebar.title("System Status")

ollama_running = check_ollama_status()

if ollama_running:
    st.sidebar.success("🟢 Ollama Running")
    st.sidebar.write("Model: Llama3")
else:
    st.sidebar.warning("🔴 Ollama Not Running")
    st.sidebar.write("Using Gemini Backup")

st.sidebar.write(f"📄 Papers Loaded: {len(uploaded_files)}")

if uploaded_files:

    all_chunks = []

    for file in uploaded_files:

        text = extract_text_from_pdf(file)

        chunks = chunk_text(text)

        all_chunks.extend(chunks)

    embeddings = create_embeddings(all_chunks)

    build_vector_store(embeddings, all_chunks)
    

    st.success("Documents processed and vector database created")
        
    st.divider()

    st.subheader(f"Paper: {file.name}")

    with st.spinner("Generating summary..."):

            summary = summarize_paper(text)

    st.write("### Summary")

    st.write(summary)

    with st.spinner("Extracting citations..."):

            citations = extract_citations(text)

    st.write("### Citations Found")

    st.write(citations)

    with st.spinner("Generating BibTeX..."):

            bibtex = generate_bibtex(text)

    st.write("### BibTeX Citation")

    st.code(bibtex)


if uploaded_files:

    if st.button("Generate Literature Review (Related Work)"):

        with st.spinner("Generating related work section..."):

            related_work = generate_related_work(all_papers_text)

        st.write("## Generated Related Work Section")

        st.write(related_work)

question = st.text_input(
    "Ask a question about the uploaded documents",
    key="question_input"
)

if st.button("Ask Question"):


    if question:

        with st.spinner("Searching documents..."):

            query_embedding = embed_query(question)

            results = search(query_embedding)

            if not results:
                st.warning("No relevant information found.")
            else:

                context = "\n".join(results)

                prompt = f"""
Answer the question using the document context.

Context:
{context}

Question:
{question}
"""

                answer = run_llm(prompt)

                st.write("### Answer")
                st.write(answer)

    else:
        st.warning("Please enter a question.")

if uploaded_files and len(uploaded_files) == 2:

    if st.button("Compare Papers"):

        text1 = extract_text_from_pdf(uploaded_files[0])
        text2 = extract_text_from_pdf(uploaded_files[1])

        similarity = compute_similarity(text1, text2)

        st.write("### Paper Similarity")
        st.write(f"Similarity Score: **{similarity}%**")

        if similarity > 70:
            st.error("High similarity detected ⚠️ Possible plagiarism")

        elif similarity > 40:
            st.warning("Moderate similarity")

        else:
            st.success("Low similarity")