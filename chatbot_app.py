import streamlit as st
from openai import OpenAI

api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chatbot ai", page_icon="🤖", layout="centered")

st.title("🤖 Chatbot ai")
st.markdown("Tanya apa saja, aku siap bantu!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Prompt system untuk karakter AI yang lebih pintar, santai, dan berpengetahuan luas
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
    # Kirimkan pesan sistem plus seluruh riwayat pesan + user prompt terbaru
    messages = [SYSTEM_PROMPT] + st.session_state.messages + [{"role": "user", "content": user_prompt}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.5  # santai tapi informatif
    )
    return response.choices[0].message.content

# CSS styling mirip ChatGPT untuk chat bubble
st.markdown("""
<style>
.user-bubble {
    background-color: #10a37f;  /* hijau ChatGPT */
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
    background-color: #444654; /* abu gelap ChatGPT */
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

chat_container = st.container()

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ketik pesan kamu:", placeholder="Tulis sesuatu...", key="user_input")
    submit = st.form_submit_button("Kirim")

if submit and user_input.strip() != "":
    st.session_state.messages.append({"role": "user", "content": user_input})
    reply = send_message(user_input)
    st.session_state.messages.append({"role": "assistant", "content": reply})

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)