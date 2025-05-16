import streamlit as st
from openai import OpenAI

api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chatbot ai", page_icon="🤖", layout="centered")

st.title("Chatbot ai")
st.markdown("Tanya apa saja, aku siap bantu!")

if "messages" not in st.session_state:
    st.session_state.messages = []

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

st.markdown("""
<style>
/* General Styling */
body, html {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Chat bubbles */
.user-bubble, .bot-bubble {
    padding: 12px 16px;
    border-radius: 20px;
    max-width: 80%;
    margin: 8px 0;
    word-wrap: break-word;
    white-space: pre-wrap;
}

.user-bubble {
    background-color: #10a37f;
    color: white;
    border-bottom-right-radius: 0;
    margin-left: auto;
    text-align: left;
}

.bot-bubble {
    background-color: #2c2f36;
    color: white;
    border-bottom-left-radius: 0;
    margin-right: auto;
    text-align: left;
}

/* Container for scrolling */
.chat-container {
    overflow-y: auto;
    max-height: 70vh;
    padding-bottom: 20px;
    margin-bottom: 10px;
}

/* Textarea auto-resize */
textarea {
    min-height: 40px !important;
    resize: none !important;
    overflow-y: hidden !important;
}

/* Send button styling */
div[data-testid="stForm"] > div:last-child {
    display: flex;
    justify-content: flex-end;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


chat_container = st.container()

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("💬", placeholder="Tulis pesanmu di sini...", key="user_input", label_visibility="collapsed", height=40)
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