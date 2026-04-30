import streamlit as st
import google.generativeai as genai

# -----------------------
# API KEY CONFIGURATION
# -----------------------
# Secrets se key uthayen ya direct paste karen (Lekin secrets behtar hain)
# st.secrets["GEMINI_API_KEY"] use karne ke liye .streamlit/secrets.toml file banani hogi
api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyCZr1o7irbtSfNXWo207cNIwXivhriTp8o")
genai.configure(api_key=api_key)

# -----------------------
# MODEL CONFIG
# -----------------------
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 500,
}

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash", # Flash fast hai aur chatbot ke liye best hai
    generation_config=generation_config,
    system_instruction="You are AI Mentor, an expert AI assistant. Help users with AI, ML, DL, and NLP topics. Be short, clear, and under 100 words."
)

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="AI Mentor Chatbot", page_icon="🤖")
st.title("AI Mentor 🤖")

# -----------------------
# SESSION STATE (Chat History)
# -----------------------
if "chat_session" not in st.session_state:
    # Gemini ki native chat history start kar rahe hain
    st.session_state.chat_session = model.start_chat(history=[])

# -----------------------
# DISPLAY CHAT HISTORY
# -----------------------
# Purani baaton ko screen par dikhana
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# -----------------------
# CHAT INPUT & LOGIC
# -----------------------
if prompt := st.chat_input("Puchiye AI ke baare mein kuch bhi..."):
    
    # 1. User ka message screen par dikhayen
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Gemini se response mangwayen
    try:
        response = st.session_state.chat_session.send_message(prompt)
        
        # 3. AI ka response screen par dikhayen
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Error: {e}")