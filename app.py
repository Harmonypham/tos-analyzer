import streamlit as st
from main import scan_tos  # your existing scan function
import openai
from io import StringIO
import sys

# 🔐 Load OpenAI API key from Streamlit Secrets (must be set in Cloud settings)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 💡 GPT Summary Function
def generate_gpt_summary(text):
    prompt = f"""
You are a legal assistant. Summarize this Terms of Service in plain English.
Focus especially on:
- If users waive legal rights (e.g. arbitration)
- If the company collects or shares data
- Any high-risk or one-sided clauses

Text:
{text[:3000]}
"""

    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# --- Streamlit App Layout ---
st.set_page_config(page_title="ToS Analyzer", layout="wide")
st.title("📄 Terms of Service Analyzer")
st.markdown("Paste or upload a Terms of Service document to check for legal red flags and get an AI-powered summary.")

# --- User Input ---
tos_input = st.text_area("📋 Paste the Terms of Service here:", height=300)
uploaded_file = st.file_uploader("📂 Or upload a .txt file", type="txt")

tos_text = ""
if uploaded_file:
    bytes_data = uploaded_file.read()
    tos_text = bytes_data.decode("utf-8")
elif tos_input.strip():
    tos_text = tos_input

# --- Red Flag Analysis ---
if st.button("🔍 Analyze ToS"):
    if tos_text:
        with st.spinner("Analyzing..."):
            output_buffer = StringIO()
            sys.stdout = output_buffer  # Redirect print
            scan_tos(tos_text)
            sys.stdout = sys.__stdout__  # Reset
            st.markdown("### 🧾 Analysis Results:")
            st.code(output_buffer.getvalue())
    else:
        st.warning("Please paste text or upload a file before analyzing.")

# --- GPT Summary ---
if st.button("🧠 Generate GPT Summary"):
    if tos_text:
        with st.spinner("Asking GPT..."):
            summary = generate_gpt_summary(tos_text)
            st.markdown("### 🧠 GPT Summary")
            st.write(summary)
    else:
        st.warning("Paste or upload a Terms of Service first.")

