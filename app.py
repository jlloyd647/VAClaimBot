# app.py
import streamlit as st
import os
from m21_qa import get_response

# --- Access code setup ---
ACCESS_CODE = os.getenv("ACCESS_CODE", "va-beta-2025")

st.set_page_config(page_title="M21-1 Chatbot", layout="wide")
st.title("🔐 M21-1 Veteran Disability Claims Assistant")

# Session state for access control
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter access code to continue:")
    if password == ACCESS_CODE:
        st.session_state.authenticated = True
        st.rerun()  # restart the app after setting session state
    elif password:
        st.error("❌ Incorrect code.")
    st.stop()

# --- Legal disclaimer gate ---
if "agreed_to_disclaimer" not in st.session_state:
    st.session_state.agreed_to_disclaimer = False

if not st.session_state.agreed_to_disclaimer:
    with st.expander("📜 Click to read and accept the legal disclaimer", expanded=True):
        st.markdown("""
        ### Disclaimer

        This chatbot is powered by a local AI model and information from the VA’s M21-1 Adjudication Manual.

        - It is **not a substitute for professional legal, medical, or benefits advice.**
        - It is **not affiliated with the VA or any government agency.**
        - The information provided may be **incomplete, outdated, or incorrect.**

        By checking the box below and clicking **Continue**, you confirm that you understand and accept these terms.
        """)

        agree = st.checkbox("I understand and accept these terms.")

        if agree:
            if st.button("Continue"):
                st.session_state.agreed_to_disclaimer = True
                st.rerun()
        else:
            st.warning("You must agree to the disclaimer to continue.")

        st.stop()

# --- Main chatbot UI ---
query = st.text_input("Ask a question about VA disability claims:")

if query:
    with st.spinner("Searching M21-1 and generating response..."):
        result = get_response(query)

    st.subheader("Answer")
    st.write(result["answer"])

    with st.expander("🔍 Extracted Keywords"):
        st.write(", ".join(result["keywords"]))

    with st.expander("📚 Matching Chunks"):
        for chunk in result["citations"]:
            st.markdown(f"**{chunk['section']}** (Chunk ID: {chunk['chunk_id']})")
            st.code(chunk["text"], language="markdown")
