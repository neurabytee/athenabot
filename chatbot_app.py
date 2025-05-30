import streamlit as st
from openai import OpenAI

api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chatbot ai", page_icon="🤖", layout="centered")

st.title("Chatbot ai")
st.markdown("Tanya apa saja, aku siap bantu!")

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Kamu adalah asisten AI yang cerdas, responsif, dan adaptif. "
        "Gunakan gaya bahasa yang menyesuaikan dengan pengguna: santai jika santai, formal jika formal. "
        "Jawaban harus jelas, informatif, relevan, dan singkat tapi padat. "
        "Akhiri dengan pertanyaan ringan atau tawaran bantuan yang sesuai konteks agar percakapan terasa natural. "

        "Tugasmu adalah memperbaiki masalah dari repositori open-source. "
        "Pahami masalah secara menyeluruh, pikirkan langkah demi langkah, dan terus iterasi sampai tuntas. "
        "Semua yang dibutuhkan ada di folder /testbed, tanpa perlu koneksi internet. "

        "Jangan akhiri sebelum yakin masalah selesai dan perbaikannya benar. "
        "Pastikan solusi diuji menyeluruh, tangani semua edge case, dan jangan asal tool call—buatlah dengan sadar dan tuntas. "

        "Strategimu: pahami masalah, telusuri kode, buat rencana, ubah kode sedikit demi sedikit, debug, uji, ulangi sampai berhasil. "
        "Rencanakan sebelum fungsi dipanggil, dan refleksi setelahnya. Pastikan solusi benar-benar kuat dan lulus semua tes, termasuk yang tersembunyi."
    )
}

if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

def send_message(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages + [{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error API: {str(e)}"

# CSS styling sama seperti sebelumnya
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

chat_container = st.container()

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ketik pesan kamu:", placeholder="Tulis sesuatu...", key="user_input")
    submit = st.form_submit_button("Kirim")

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    reply = send_message(user_input)
    st.session_state.messages.append({"role": "assistant", "content": reply})

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        # jangan tampilkan system prompt
