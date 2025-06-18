from find_relevant_chunks import (
    load_documents,
    extract_keywords_with_ollama,
    find_relevant_chunks_by_keywords
)
from langchain_community.llms import Ollama

# --- Load M21-1 chunk data once ---
documents = load_documents("data/chunks/")
print(f"✅ Loaded {len(documents)} chunks.")

# --- Ask the LLM with selected context ---
def ask_llm(query, relevant_docs):
    llm = Ollama(model="mistral")

    print(f"\n📦 Sending {len(relevant_docs)} chunks to the model.")
    for doc in relevant_docs[:10]:  # Log the first few
        print(f"- {doc.metadata.get('chunk_id')} | {doc.metadata.get('title')}")

    # Soft cap on total word count
    max_words = 3000
    word_count = 0
    safe_chunks = []

    for doc in relevant_docs:
        words = doc.page_content.split()
        if word_count + len(words) > max_words:
            break
        safe_chunks.append(doc)
        word_count += len(words)

    context = "\n\n---\n\n".join(doc.page_content for doc in safe_chunks)

    prompt = f"""
You are a helpful assistant answering questions about VA benefits using the M21-1 Adjudication Manual.

Use only the following context to answer the question. If the answer is not in the context, say "I don't know."

<<CONTEXT BEGINS>>
{context}
<<CONTEXT ENDS>>

Question: {query}

Answer:"""

    print(f"\n🧠 Prompt length: {len(prompt)} characters")
    return llm.invoke(prompt)

# --- Wrap everything in a callable response function ---
def get_response(query: str) -> dict:
    search_terms = extract_keywords_with_ollama(query)

    matches = find_relevant_chunks_by_keywords(
        documents,
        search_terms,
        allowed_parts=["part iii", "part v", "part vi", "part x"]
    )

    if not matches:
        return {
            "answer": "❌ No matching documents found.",
            "keywords": search_terms,
            "citations": []
        }

    answer = ask_llm(query, matches)

    citations = [
        {
            "section": doc.metadata.get("title", "Unknown Section"),
            "chunk_id": doc.metadata.get("chunk_id", "N/A"),
            "text": doc.page_content[:500]  # Preview
        }
        for doc in matches
    ]

    return {
        "answer": answer,
        "keywords": search_terms,
        "citations": citations
    }

# --- Optional: keep CLI functionality for testing ---
if __name__ == "__main__":
    while True:
        query = input("\nAsk a VA question (or type 'exit'): ")
        if query.strip().lower() == "exit":
            break

        result = get_response(query)
        print(f"\n🧠 Extracted keywords: {result['keywords']}")
        print(f"\n✅ Found {len(result['citations'])} matching chunks.")
        print("\nAnswer:", result["answer"])
