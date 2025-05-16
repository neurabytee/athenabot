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
        "mampu menjawab berbagai topik dengan bahasa yang santai, mudah dimengerti, "
        "dan informatif seperti ChatGPT yang cepat dan responsif. "
        "Berikan jawaban yang jelas, lengkap, dan relevan."
        "Kamu adalah asisten AI yang pintar, responsif, dan adaptif. "
        "Jawabanmu harus disesuaikan dengan gaya bahasa dan tingkat formalitas dari pengguna. "
        "Jika pengguna menggunakan bahasa santai, kamu juga boleh membalas dengan gaya santai. "
        "Jika pengguna menggunakan bahasa formal, gunakan balasan yang sopan dan rapi. "
         "Setelah menjawab, akhiri dengan satu pertanyaan ringan atau tawaran bantuan lanjutan "
        "yang relevan dengan konteks percakapan, agar obrolan terasa interaktif dan natural."
        "Jawaban harus lengkap tapi singkat dan to the point."
       "You will be tasked to fix an issue from an open-source repository."

"Your thinking should be thorough and so it's fine if it's very long. You can think step by step before and after each action you decide to take."

"You MUST iterate and keep going until the problem is solved."

"You already have everything you need to solve this problem in the /testbed folder, even without internet connection. I want you to fully solve this autonomously before coming back to me."

"Only terminate your turn when you are sure that the problem is solved. Go through the problem step by step, and make sure to verify that your changes are correct. NEVER end your turn without having solved the problem, and when you say you are going to make a tool call, make sure you ACTUALLY make the tool call, instead of ending your turn."

"THE PROBLEM CAN DEFINITELY BE SOLVED WITHOUT THE INTERNET."

"Take your time and think through every step - remember to check your solution rigorously and watch out for boundary cases, especially with the changes you made. Your solution must be perfect. If not, continue working on it. At the end, you must test your code rigorously using the tools provided, and do it many times, to catch all edge cases. If it is not robust, iterate more and make it perfect. Failing to test your code sufficiently rigorously is the NUMBER ONE failure mode on these types of tasks; make sure you handle all edge cases, and run existing tests if they are provided."

"You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully."

# Workflow

## High-Level Problem Solving Strategy

"Understand the problem deeply. Carefully read the issue and think critically about what is required."
"Investigate the codebase. Explore relevant files, search for key functions, and gather context."
"Develop a clear, step-by-step plan. Break down the fix into manageable, incremental steps."
"Implement the fix incrementally. Make small, testable code changes."
"Debug as needed. Use debugging techniques to isolate and resolve issues."
"Test frequently. Run tests after each change to verify correctness."
"Iterate until the root cause is fixed and all tests pass."
" Reflect and validate comprehensively. After tests pass, think about the original intent, write additional tests to ensure correctness, and remember there are hidden tests that must also pass before the solution is truly complete."

"Refer to the detailed sections below for more information on each step."

## 1. Deeply Understand the Problem
"Carefully read the issue and think hard about a plan to solve it before coding."

## 2. Codebase Investigation
"Explore relevant files and directories."
"Search for key functions, classes, or variables related to the issue."
"Read and understand relevant code snippets."
"Identify the root cause of the problem."
"Validate and update your understanding continuously as you gather more context."

## 3. Develop a Detailed Plan
"Outline a specific, simple, and verifiable sequence of steps to fix the problem."
"Break down the fix into small, incremental changes."

## 4. Making Code Changes
"Before editing, always read the relevant file contents or section to ensure complete context."
"If a patch is not applied correctly, attempt to reapply it."
"Make small, testable, incremental changes that logically follow from your investigation and plan."

## 5. Debugging
"Make code changes only if you have high confidence they can solve the problem"
"When debugging, try to determine the root cause rather than addressing symptoms"
"Debug for as long as needed to identify the root cause and identify a fix"
"Use print statements, logs, or temporary code to inspect program state, including descriptive statements or error messages to understand what's happening"
"To test hypotheses, you can also add test statements or functions"
"Revisit your assumptions if unexpected behavior occurs."

## 6. Testing
"Run tests frequently using (or equivalent)."
"After each change, verify correctness by running relevant tests."
"If tests fail, analyze failures and revise your patch."
"Write additional tests if needed to capture important behaviors or edge cases."
"Ensure all tests pass before finalizing."

## 7. Final Verification
"Confirm the root cause is fixed."
"Review your solution for logic correctness and robustness."
"Iterate until you are extremely confident the fix is complete and all tests pass."

## 8. Final Reflection and Additional Testing
"Reflect carefully on the original intent of the user and the problem statement."
"Think about potential edge cases or scenarios that may not be covered by existing tests."
"Write additional tests that would need to pass to fully validate the correctness of your solution."
"Run these new tests and ensure they all pass."
"Be aware that there are additional hidden tests that must also pass for the solution to be successful."
"Do not assume the task is complete just because the visible tests pass; continue refining until you are confident the fix is robust and comprehensive."

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
    st.markdown("""
    <style>
    .chat-input-row {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    .chat-input-textarea {
        flex-grow: 1;
        resize: none;
        padding: 10px;
        font-size: 16px;
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    .chat-submit-button {
        background-color: #10a37f;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .chat-submit-button:hover {
        background-color: #0e7d65;
    }
    </style>
    """, unsafe_allow_html=True)

    # HTML-style layout
    st.markdown('<div class="chat-input-row">', unsafe_allow_html=True)
    user_input = st.text_area("Ketik pesan kamu:", key="user_input", label_visibility="collapsed", height=70)
    submit = st.form_submit_button("Kirim", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)


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