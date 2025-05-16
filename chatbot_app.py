import streamlit as st
from openai import OpenAI
import json

api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chatbot AI", page_icon="🤖", layout="wide")

st.title("🤖 Chatbot AI")
st.markdown("Tanya apa saja, aku siap bantu!")

if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Kamu adalah asisten AI yang pintar dan berpengetahuan luas, "
        "mampu menjawab berbagai topik dengan bahasa yang santai, mudah dimengerti, "
        "dan informatif seperti ChatGPT yang cepat dan responsif. "
        "Berikan jawaban yang jelas, lengkap, dan relevan."
    )
}

def send_message(user_prompt):
    messages = [SYSTEM_PROMPT] + st.session_state.messages + [{"role": "user", "content": user_prompt}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.5
    )
    return response.choices[0].message.content

# CSS Styling & Animasi
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

body, .block-container {
    font-family: 'Inter', sans-serif;
    background-color: #0f111a;
    color: #d1d5db;
}

.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 15px;
    border-radius: 12px;
    background-color: #20232a;
    box-shadow: 0 4px 8px rgb(0 0 0 / 0.3);
    margin-bottom: 10px;
}

.user-bubble, .bot-bubble {
    padding: 12px 18px;
    border-radius: 20px;
    max-width: 70%;
    margin-bottom: 10px;
    animation: fadeInUp 0.3s ease forwards;
    word-wrap: break-word;
    line-height: 1.4;
    font-size: 16px;
}

.user-bubble {
    background-color: #10a37f;
    color: white;
    margin-left: auto;
    border-radius: 20px 20px 0 20px;
}

.bot-bubble {
    background-color: #444654;
    color: white;
    margin-right: auto;
    border-radius: 20px 20px 20px 0;
}

.chat-input-container {
    display: flex;
    gap: 8px;
}

input[type="text"] {
    flex-grow: 1;
    padding: 12px 16px;
    border-radius: 20px;
    border: none;
    font-size: 16px;
    outline: none;
    background-color: #2a2d3e;
    color: white;
}

button {
    background-color: #10a37f;
    border: none;
    border-radius: 20px;
    padding: 0 20px;
    font-weight: bold;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #0c8267;
}

.clear-btn {
    background-color: #ef4444;
}

.clear-btn:hover {
    background-color: #b91c1c;
}

.copy-btn {
    background-color: #3b82f6;
    margin-left: 8px;
}

.copy-btn:hover {
    background-color: #1e40af;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""", unsafe_allow_html=True)

chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            # Tambah tombol copy di setiap balasan bot
            msg_id = f"msg_{i}"
            st.markdown(f'''
                <div class="bot-bubble" id="{msg_id}">{msg["content"]}</div>
                <button class="copy-btn" onclick="copyToClipboard('{msg_id}')">Copy</button>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Form input & tombol kirim
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([8,1,1])
    user_input = col1.text_input("Ketik pesan kamu:", placeholder="Tulis sesuatu...", key="user_input")
    submit = col2.form_submit_button("Kirim")
    clear = col3.form_submit_button("Clear Chat")

if clear:
    st.session_state.messages = []

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        reply = send_message(user_input)
    except Exception as e:
        reply = f"⚠️ Error: {e}"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.experimental_rerun()

# JavaScript untuk copy ke clipboard dan scroll otomatis
st.markdown("""
<script>
function copyToClipboard(id) {
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    });
}
const chatContainer = document.getElementById('chat-container');
if(chatContainer){
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
</script>
""", unsafe_allow_html=True)
