import os
import json
import sys
import re
from collections import Counter
from langchain.schema import Document
from langchain_community.llms import Ollama

# --- Load M21-1 Documents from JSON chunks ---
def load_documents(chunk_dir="data/chunks/"):
    documents = []
    for filename in os.listdir(chunk_dir):
        if filename.endswith(".json"):
            with open(os.path.join(chunk_dir, filename), "r", encoding="utf-8") as f:
                chunk = json.load(f)
                doc = Document(
                    page_content=chunk.get("content", ""),
                    metadata={
                        "chunk_id": chunk.get("chunk_id"),
                        "title": chunk.get("title"),
                        "citation": chunk.get("citation"),
                        "url": chunk.get("source_url"),
                        "updated": chunk.get("updated")
                    }
                )
                documents.append(doc)
    return documents

# --- Match chunks based on keyword list ---
def find_relevant_chunks_by_keywords(documents, keywords, allowed_parts=None):
    keywords = [kw.lower() for kw in keywords]
    matches = []

    for doc in documents:
        content = doc.page_content.lower()
        citation = doc.metadata.get("citation", "").lower()

        # Optional: restrict to specific parts of the manual
        if allowed_parts:
            if not any(part in citation for part in allowed_parts):
                continue

        # Match if any keyword appears
        if any(kw in content for kw in keywords):
            matches.append(doc)

    return matches

# --- LLM-based keyword extractor ---
def extract_keywords_with_ollama(prompt_text, model_name="llama3"):
    llm = Ollama(model=model_name)

    instruction = (
        "Extract 5 to 10 medically or procedurally relevant keywords or phrases from the following question "
        "about veterans' disability claims. Focus on specific conditions, procedures, or benefits mentioned. "
        "Exclude general terms like about the Veterans Association (VA), the VA procedures, and other terms that may not relate to a veterans medical condition. "
        "Return only a comma-separated list.\n\n"
        f"Question: {prompt_text}\n\nKeywords:"
    )

    response = llm.invoke(instruction).strip()
    keywords = [kw.strip().lower() for kw in response.split(",") if kw.strip()]
    return keywords

# --- CLI entry point ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage:")
        print("   python find_relevant_chunks.py <keyword1> [keyword2] [...]")
        print("   OR")
        print("   python find_relevant_chunks.py --prompt \"What does the M21-1 say about PTSD claims?\"")
        sys.exit(1)

    if sys.argv[1] == "--prompt":
        prompt_text = " ".join(sys.argv[2:])
        print(f"\n💬 Prompt: {prompt_text}")
        search_terms = extract_keywords_with_ollama(prompt_text)
        print(f"\n🧠 Extracted keywords from LLM: {search_terms}")
    else:
        search_terms = sys.argv[1:]

    allowed_parts = ["part iii", "part v", "part vi", "part x"]

    print(f"\n🔍 Searching for chunks with: {search_terms}")
    print(f"📚 Allowed parts: {', '.join(allowed_parts)}")

    documents = load_documents("data/chunks/")
    results = find_relevant_chunks_by_keywords(documents, search_terms, allowed_parts)

    print(f"\n✅ Found {len(results)} matching chunks.\n")
