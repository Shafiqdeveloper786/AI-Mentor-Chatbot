import streamlit as st
from groq import Groq

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI Mentor Elite",
    page_icon="🤖",
    layout="centered"
)

# ==========================================
# 🔥 ULTRA-CLEAR UI & STYLISH AVATARS
# ==========================================
st.markdown("""
<style>
/* Main Background */
.stApp {
    background: linear-gradient(-45deg, #050a18, #0c122b, #111a36, #050505);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #ffffff;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Chat Message Styling */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(0, 245, 255, 0.1) !important;
    border-radius: 15px !important;
    padding: 15px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
}

/* Avatar Border & Glow */
[data-testid="stChatMessage"] img, [data-testid="stChatMessageContent"] {
    border-radius: 50% !important;
}

/* ⚪ ALL GENERATED TEXT COLOR: PURE WHITE */
[data-testid="stChatMessage"] .stMarkdown p, 
[data-testid="stChatMessage"] .stMarkdown li, 
[data-testid="stChatMessage"] .stMarkdown span,
[data-testid="stChatMessage"] .stMarkdown strong {
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    text-shadow: 0px 1px 2px rgba(0,0,0,0.5) !important;
}

/* Stylish Bullet Points */
[data-testid="stChatMessage"] .stMarkdown li::marker {
    color: #ff00c8 !important;
}

/* ✍️ INPUT BOX: BLACK TEXT */
.stChatInputContainer {
    background: #ffffff !important;
    border: 2px solid #00f5ff !important;
    border-radius: 50px !important;
}

.stChatInput textarea {
    color: #000000 !important;
}

/* Footer Styling */
.footer-text {
    text-align: center;
    font-weight: bold;
    background: linear-gradient(90deg, #ff00c8, #00f5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 3.5rem; font-weight: 900; background: linear-gradient(90deg, #00f5ff, #ff00c8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI MENTOR</h1>
    <p style="color: #00f5ff; letter-spacing: 3px; font-weight: bold;">⚡ QUANTUM KNOWLEDGE CORE ⚡</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 API & SESSION STATE
# ==========================================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# AVATAR LINKS (High Quality Icons)
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/3177/3177440.png" # Stylish User
AI_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"   # Futuristic Robot

# ==========================================
# DISPLAY CHAT
# ==========================================
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        avatar = USER_AVATAR if msg["role"] == "user" else AI_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# ==========================================
# CHAT LOGIC
# ==========================================
if prompt := st.chat_input("Ask me anything..."):

    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

    # 2. AI Response
    with chat_container:
        with st.chat_message("assistant", avatar=AI_AVATAR):
            with st.spinner("⚡ AI Mentor is Thinking..."):
                response_placeholder = st.empty()
                
                try:
                    system_instruction = """
                    You are AI Mentor, an elite AI assistant. 
                    - Developed by: Shafiq Chohan.
                    - If asked about developer, tell them: 'I was developed by Shafiq Chohan'.
                    - Maintain a professional tone. Refuse inappropriate content.
                    """

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": system_instruction}, *st.session_state.messages],
                        max_tokens=1024,
                        temperature=0.6
                    )

                    full_reply = response.choices[0].message.content
                    response_placeholder.markdown(full_reply)
                    st.session_state.messages.append({"role": "assistant", "content": full_reply})
                    
                    st.components.v1.html(
                        """<script>window.parent.document.querySelector('.main').scrollTo(0, window.parent.document.querySelector('.main').scrollHeight);</script>""", 
                        height=0
                    )

                except Exception as e:
                    st.error(f"Error: {e}")

# Footer
st.markdown(f"<div class='footer-text'>CORE v4.0.2 | CREATED BY SHAFIQ CHOHAN</div>", unsafe_allow_html=True)