import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Personal Assistant", page_icon="⚡")
st.title("⚡ AI Personal Assistant")

api_key = st.sidebar.text_input("Groq API Key:", type="password")
task_type = st.sidebar.selectbox("Choose Task:", ["General QA & Search", "Draft Email", "Summarize Text"])

if not api_key:
    st.info("Enter your Groq API Key to start.")
    st.stop()

client = Groq(api_key=api_key)

# Web Speech API JS Snippet for Voice Input
st.components.v1.html("""
    <script>
    function record() {
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.onresult = function(e) {
            const text = e.results[0][0].transcript;
            const inputEl = window.parent.document.querySelector('textarea[aria-label="Enter your prompt/command:"]');
            if(inputEl) { inputEl.value = text; inputEl.dispatchEvent(new Event('input', { bubbles: true })); }
        }
        recognition.start();
    }
    </script>
    <button onclick="record()" style="padding: 8px 12px; border-radius: 5px; cursor: pointer;">🎙️ Speak Command</button>
""", height=50)

user_input = st.text_area("Enter your prompt/command:")

if st.button("Run Task") and user_input:
    prompts = {
        "General QA & Search": f"Answer concisely: {user_input}",
        "Draft Email": f"Draft a professional email based on this request: {user_input}",
        "Summarize Text": f"Provide a concise summary with key points for: {user_input}"
    }
    
    with st.spinner("Processing..."):
        res = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompts[task_type]}]
        )
        st.markdown("### Result:")
        st.write(res.choices[0].message.content)
