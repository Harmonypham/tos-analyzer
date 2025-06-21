# app.py

import streamlit as st
from main import scan_tos  # Assumes your scan_tos function is in main.py

st.set_page_config(page_title="ToS Analyzer", layout="wide")

st.title("📄 Terms of Service Analyzer")
st.markdown("Paste or upload a Terms of Service document to check for legal red flags and risk level.")

# --- Option 1: Paste text ---
tos_input = st.text_area("📋 Paste the Terms of Service here:", height=300)

# --- Option 2: Upload a text file ---
uploaded_file = st.file_uploader("📂 Or upload a .txt file", type="txt")

tos_text = ""

if uploaded_file:
    bytes_data = uploaded_file.read()
    tos_text = bytes_data.decode("utf-8")
elif tos_input.strip():
    tos_text = tos_input

# --- Analyze Button ---
if st.button("🔍 Analyze ToS"):
    if tos_text:
        with st.spinner("Analyzing..."):
            # Reuse your scan_tos() logic and redirect output to Streamlit
            from io import StringIO
            import sys

            output_buffer = StringIO()
            sys.stdout = output_buffer  # Redirect print output

            scan_tos(tos_text)  # from your existing main.py

            sys.stdout = sys.__stdout__  # Reset output

            st.markdown("### 🧾 Analysis Results:")
            st.code(output_buffer.getvalue())
    else:
        st.warning("Please paste text or upload a file before analyzing.")
