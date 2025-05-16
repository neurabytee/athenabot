import streamlit as st
from openai import OpenAI

api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chatbot AI", page_icon="🤖", layout="wide")

# ----- JS & CSS harus di awal -----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

body, .block-container {
    font-family: 'Inter', sans-serif;
    background-color: #0f111a;
    color: #d1d5db;
}

/* ... CSS styles kamu ... */

</style>

<script>
function copyToClipboard(id) {
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    });
}
window.onload = () => {
    const chatContainer = document.getElementById('chat-container');
    if(chatContainer){
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
};
</script>
""", unsafe_allow_html=True)

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

chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            msg_id = f"msg_{i}"
            st.markdown(f'''
                <div class="bot-bubble" id="{msg_id}">{msg["content"]}</div>
                <button class="copy-btn" onclick="copyToClipboard('{msg_id}')">Copy</button>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.form(key="chat_form"):
    col1, col2 = st.columns([8,1])
    user_input = col1.text_input("Ketik pesan kamu:", placeholder="Tulis sesuatu...", key="user_input")
    submit = col2.form_submit_button("Kirim")

clear = st.button("Clear Chat", help="Hapus semua chat dan mulai baru")

if clear:
    st.session_state.messages = []
    st.experimental_rerun()

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        reply = send_message(user_input)
    except Exception as e:
        reply = f"⚠️ Error: {e}"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.experimental_rerun()
