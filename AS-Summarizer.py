import streamlit as st
from openai import OpenAI

# ------------------------- Configuration -------------------------
st.set_page_config(page_title="AS Summarizer for CA Students")
st.title("📘 Accounting Standards (AS) Summarizer")
st.markdown("Get quick summaries of ICAI Accounting Standards (AS). Ask questions like 'Summarize AS 10' or 'Explain AS 12 with example'.")

# Optional: Set your OpenAI API key here (if running locally)
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""
client = OpenAI(api_key=api_key)

# ------------------------- Prompt Template -------------------------
def generate_prompt(user_query):
    system_msg = (
        "You are a qualified Chartered Accountant who helps CA students understand ICAI Accounting Standards (AS). "
        "Provide clear, concise summaries of Accounting Standards AS 1 to AS 29 as per CA Intermediate and Final syllabus. "
        "Keep the language simple. If the user asks for an example, include a relevant example. "
        "DO NOT hallucinate or make up standards that don't exist."
    )
    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_query}
    ]

# ------------------------- AI Response Function -------------------------
def get_as_summary(query):
    try:
        messages = generate_prompt(query)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ------------------------- UI -------------------------
user_input = st.text_input("📥 Ask about an Accounting Standard:", placeholder="e.g. Summarize AS 9")

if st.button("🧠 Get Summary") and user_input:
    with st.spinner("Generating summary..."):
        result = get_as_summary(user_input)
        st.markdown("---")
        st.markdown(result)

# ------------------------- Footer -------------------------
st.markdown("---")
st.caption("Made for CA Students | Phase 1: AS Summarizer | Ind AS & Comparisons coming soon")
