import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Personal Assistant", page_icon="🤖", layout="wide")
st.title("🤖 Enterprise AI Personal Assistant")

# Sidebar Controls & API Security
st.sidebar.header("⚙️ Configuration & Security")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not api_key:
    st.info("Please enter your Groq API Key in the sidebar to start chatting.")
    st.stop()

# Initialize Client
try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Authentication Setup Error: {str(e)}")
    st.stop()

# Hyperparameter Tuning Controls (from notes: Temperature & Tokens)
temperature = st.sidebar.slider("Temperature (Creativity):", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
max_tokens = st.sidebar.slider("Max Output Tokens:", min_value=100, max_value=2048, value=1024, step=100)

# Persona / System Prompt Setup
persona = st.sidebar.selectbox(
    "Select System Persona:",
    ["Senior Software Architect", "Data Science & ML Mentor", "Technical Interviewer", "General Assistant"]
)

persona_prompts = {
    "Senior Software Architect": "You are a Senior Software Architect. Provide clear, scalable, high-performance solution designs with clean code practices.",
    "Data Science & ML Mentor": "You are an expert Data Scientist. Explain ML models, evaluation metrics (precision/recall/F1), and math concepts clearly.",
    "Technical Interviewer": "You are a demanding Technical Interviewer. Ask follow-up probing questions and evaluate response logic critically.",
    "General Assistant": "You are a helpful, concise, and professional AI assistant."
}

# Chat Memory Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_input := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # API Execution & Response Generation
    with st.chat_message("assistant"):
        with st.spinner("Processing request..."):
            try:
                # Payload construction with explicit System Prompt
                payload_messages = [{"role": "system", "content": persona_prompts[persona]}] + st.session_state.messages
                
                res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=payload_messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                st.error(f"REST API Execution Error: {str(e)}")
