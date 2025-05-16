import streamlit as st
from openai import OpenAI

# API Key aman via st.secrets
api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=api_key)

# Konfigurasi halaman
st.set_page_config(page_title="Chatbot AI", page_icon="🤖", layout="centered")
st.title("🤖 Chatbot AI")
st.markdown("Tanya apa saja, aku siap bantu!")

# Inisialisasi state pesan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Prompt sistem (karakter AI)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Kamu adalah asisten AI yang pintar dan berpengetahuan luas, "
        "mampu menjawab berbagai topik dengan bahasa yang santai, mudah dimengerti, "
        "dan informatif seperti ChatGPT yang cepat dan responsif. "
        "Berikan jawaban yang jelas, lengkap, dan relevan."
    )
}

# Fungsi kirim prompt ke OpenAI
def send_message(prompt):
    messages = [SYSTEM_PROMPT] + st.session_state.messages + [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.5
    )
    return response.choices[0].message.content

# Styling chat bubble
st.markdown("""
<style>
.user-bubble {
    background-color: #10a37f;
    color: white;
    padding: 10px 15px;
    border-radius: 20px 20px 0 20px;
    max-width: 70%;
    margin: 5px 0;
    float: right;
    clear: both;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    word-wrap: break-word;
}
.bot-bubble {
    background-color: #444654;
    color: white;
    padding: 10px 15px;
    border-radius: 20px 20px 20px 0;
    max-width: 70%;
    margin: 5px 0;
    float: left;
    clear: both;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    word-wrap: break-word;
}
.chat-container {
    overflow-y: auto;
    max-height: 600px;
    padding-bottom: 10px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# Form input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ketik pesan kamu:", placeholder="Tulis sesuatu...", key="user_input")
    submitted = st.form_submit_button("Kirim")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Mengetik balasan..."):
        try:
            response = send_message(user_input)
        except Exception as e:
            response = f"⚠️ Error saat mengambil balasan: {e}"
    st.session_state.messages.append({"role": "assistant", "content": response})

# Tampilan chat
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)