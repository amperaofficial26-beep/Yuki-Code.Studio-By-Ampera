import streamlit as st
from openai import OpenAI

# Konfigurasi Page
st.set_page_config(page_title="Yuki AI", page_icon="🌸")

# Inisialisasi Client OpenAI (Universal untuk Groq)
groq_key = st.secrets.get("GROQ_API_KEY")
client = OpenAI(
    api_key=groq_key,
    base_url="https://api.groq.com/openai/v1"
)

# UI Dasar
st.title("🌸 Yuki AI Studio")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Chat
if chat_input := st.chat_input("Ngobrol sama Yuki..."):
    if not groq_key:
        st.error("API Key belum diset di Streamlit Secrets!")
        st.stop()
        
    # Tambah pesan user
    st.session_state.messages.append({"role": "user", "content": chat_input})
    with st.chat_message("user"):
        st.markdown(chat_input)
    
    # Respon AI
    with st.chat_message("assistant"):
        with st.spinner("Yuki sedang berpikir..."):
            try:
                # Menggunakan model llama-3.3-70b-versatile (Sangat pintar & cepat)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Kamu adalah Yuki, asisten AI pribadi yang ramah, hangat, dan sedikit bergaya anime/cyberpunk."},
                        *st.session_state.messages
                    ]
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Waduh, Yuki pusing! {e}")
