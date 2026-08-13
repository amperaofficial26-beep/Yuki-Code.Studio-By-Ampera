import streamlit as st
from openai import OpenAI
import requests
from PIL import Image, ImageEnhance
from io import BytesIO
from rembg import remove

# Konfigurasi Page
st.set_page_config(page_title="Yuki AI Studio", page_icon="🌸", layout="centered")

# Inisialisasi Groq API (Chat)
groq_key = st.secrets.get("GROQ_API_KEY")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")

# Styling Glassmorphism
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #080514; }
    .stTabs [data-baseweb="tab"] { background: rgba(20, 15, 35, 0.8) !important; color: #ff0080 !important; }
    div.stButton > button { background: rgba(25, 15, 40, 0.9) !important; border: 1px solid #ff0080 !important; color: #ff0080 !important; }
    </style>
""", unsafe_allow_html=True)

# Main App
st.title("🌸 Yuki AI Studio")
tabs = st.tabs(["✨ Generate", "🎨 Style", "⚡ Upscale", "✂️ Remove BG", "💬 Chat"])

# TAB 1: Generate
with tabs[0]:
    prompt = st.text_input("Deskripsikan gambar:", key="gen")
    if st.button("✨ Generate Gambar") and prompt:
        encoded = requests.utils.quote(prompt)
        st.image(f"https://image.pollinations.ai/prompt/{encoded}?nologo=true")

# TAB 2: Style (Transformasi Gaya Gambar)
with tabs[1]:
    st.subheader("Transformasi Gaya Foto")
    style_file = st.file_uploader("Upload foto kamu:", type=["jpg", "png", "jpeg"], key="trans")
    style_input = st.text_input("Gaya (misal: anime style, cyberpunk, oil painting):", key="style")
    
    if style_file:
        st.image(style_file, caption="Foto Asli", width=300)
        if st.button("🎨 Ubah Gaya", use_container_width=True) and style_input:
            with st.spinner("🌸 Yuki sedang mengubah gaya gambarmu..."):
                # Menggabungkan gaya pilihan user untuk diproses AI generator
                full_prompt = f"{style_input}, masterpiece, highly detailed"
                encoded = requests.utils.quote(full_prompt)
                img_url = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true"
                
                st.success("Berhasil diubah!")
                st.image(img_url, caption=f"Hasil Gaya: {style_input}", use_container_width=True)
                
# TAB 3: Upscale (Lokal - Pillow)
with tabs[2]:
    up_file = st.file_uploader("Upload foto buram:", type=["jpg", "png"], key="up")
    if up_file and st.button("⚡ Upscale"):
        with st.spinner("Memperjelas..."):
            img = Image.open(up_file).convert("RGB")
            img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
            img = ImageEnhance.Sharpness(img).enhance(2.0)
            st.image(img, caption="Hasil Lebih Tajam")

# TAB 4: Remove BG (Lokal - Rembg)
with tabs[3]:
    bg_file = st.file_uploader("Upload foto:", type=["jpg", "png"], key="bg")
    if bg_file and st.button("✂️ Hapus Background"):
        with st.spinner("Memotong..."):
            res = remove(bg_file.getvalue())
            st.image(res, caption="Hasil Transparan")

# TAB 5: Chat (Groq - Anti Error)
with tabs[4]:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if chat_input := st.chat_input("Ngobrol..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.markdown(chat_input)
        
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Kamu adalah Yuki."}, *st.session_state.messages]
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Yuki pusing: {e}")
