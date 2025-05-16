import streamlit as st
import google.generativeai as genai

# Konfigurasi API Key dari Streamlit Secrets
genai.configure(api_key=st.secrets["gemini_api_key"])

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Chatbot AI Gemini", page_icon="🤖", layout="centered")
st.title("Chatbot AI Gemini")
st.markdown("Tanya apa saja, aku siap bantu!")

# Inisialisasi chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ini adalah prompt awal setara dengan 'system' di OpenAI
SYSTEM_PROMPT = (
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

# Fungsi kirim dan terima pesan
def send_message(prompt):
    # Susun ulang history (mulai dari system prompt sebagai user pertama)
    chat = genai.GenerativeModel("gemini-pro").start_chat(history=[
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        *[
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages
        ]
    ])
    response = chat.send_message(prompt)
    return response.text

# Styling bubble chat
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

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ketik pesan kamu:", placeholder="Tulis sesuatu...")
    submit = st.form_submit_button("Kirim")

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        reply = send_message(user_input)
        st.session_state.messages.append({"role": "model", "content": reply})
    except Exception as e:
        st.session_state.messages.append({
            "role": "model",
            "content": f"⚠️ Terjadi error saat menghubungi Gemini API: {str(e)}"
        })

# Tampilkan chat
with chat_container:
    for msg in st.session_state.messages:
        bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
        st.markdown(f'<div class="{bubble_class}">{msg["content"]}</div>', unsafe_allow_html=True)
