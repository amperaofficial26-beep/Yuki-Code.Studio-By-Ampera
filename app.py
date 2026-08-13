#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py
======
Yuki AI Studio & Chat - Powered by DeepAI, Pollinations, & Google Gemini
"""

import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO

# Konfigurasi Halaman
st.set_page_config(page_title="Yuki - AI Studio & Chat", page_icon="🌸", layout="centered")

# Inisialisasi API Gemini secara langsung ke model stabil
google_key = st.secrets.get("GOOGLE_API_KEY", "")
model_chat = None

if google_key:
    genai.configure(api_key=google_key)
    # Coba gunakan model yang stabil dan ramah akun baru
    for m_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
        try:
            model_chat = genai.GenerativeModel(m_name)
            break
        except Exception:
            continue
    
    # Fallback darurat jika pemindaian gagal
    if not model_chat:
        try:
            model_chat = genai.GenerativeModel('gemini-1.5-flash')
        except Exception:
            pass

# Styling Tema Cyberpunk Anime Glassmorphism
def set_ui_style():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #080514;
            background-image: radial-gradient(circle at 2px 2px, rgba(255, 0, 128, 0.25) 1.5px, transparent 0);
            background-size: 50px 50px;
        }
        [data-testid="stMainBlockContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab"] {
            background: rgba(20, 15, 35, 0.8) !important;
            border: 1px solid rgba(255, 0, 128, 0.3) !important;
            color: #ff0080 !important;
            border-radius: 10px !important;
        }
        div.stButton > button {
            background: rgba(25, 15, 40, 0.9) !important;
            border: 1px solid rgba(255, 0, 128, 0.5) !important;
            color: #ff0080 !important;
            border-radius: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Fungsi Helper untuk Memanggil DeepAI API
def call_deepai_api(endpoint: str, file_bytes: bytes) -> bytes | None:
    api_key = st.secrets.get("DEEPAI_API_KEY", "")
    if not api_key:
        st.error("DEEPAI_API_KEY belum diatur di Streamlit Secrets!")
        return None
        
    url = f"https://api.deepai.org/api/{endpoint}"
    headers = {'api-key': api_key}
    files = {'image': ('image.jpg', file_bytes)}
    
    try:
        response = requests.post(url, files=files, headers=headers, timeout=60)
        if response.status_code == 200:
            res_json = response.json()
            output_url = res_json.get("output_url")
            if output_url:
                img_resp = requests.get(output_url, timeout=30)
                return img_resp.content
        st.error(f"DeepAI Error: {response.text}")
        return None
    except Exception as e:
        st.error(f"Koneksi Error: {e}")
        return None

def main():
    set_ui_style()
    st.title("🌸 Yuki - AI Studio & Chat")
    
    tabs = st.tabs(["✨ Generate", "🎨 Transform", "⚡ Upscale", "✂️ Remove BG", "💬 Chat with Yuki"])

    # -------------------------------------------------------------
    # TAB 1: Generate Gambar dari Teks (Pollinations - Gratis)
    # -------------------------------------------------------------
    with tabs[0]:
        st.subheader("Buat Gambar dari Teks")
        prompt = st.text_input("Deskripsikan gambar impianmu:", key="gen_prompt")
        if st.button("✨ Generate Gambar", use_container_width=True) and prompt:
            with st.spinner("🌸 Yuki sedang meracik gambar..."):
                encoded = requests.utils.quote(prompt)
                img_url = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true"
                st.image(img_url, caption=f"Prompt: {prompt}", use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: Transform Gaya (DeepAI Style Transfer)
    # -------------------------------------------------------------
    with tabs[1]:
        st.subheader("Transformasi Gaya Foto")
        file = st.file_uploader("Upload foto kamu:", type=["jpg", "png", "jpeg"], key="trans_file")
        if file:
            st.image(file, caption="Foto Asli", width=300)
            if st.button("🎨 Ubah Gaya", use_container_width=True):
                with st.spinner("🌸 Yuki sedang mengubah gaya gambarmu..."):
                    result_bytes = call_deepai_api("style-transfer", file.getvalue())
                    if result_bytes:
                        res_img = Image.open(BytesIO(result_bytes))
                        st.success("Berhasil diubah!")
                        st.image(res_img, caption="Hasil Transformasi", use_container_width=True)

    # -------------------------------------------------------------
    # TAB 3: AI Upscaler (DeepAI Torch-SRGAN)
    # -------------------------------------------------------------
    with tabs[2]:
        st.subheader("AI Image Upscaler")
        file = st.file_uploader("Upload gambar buram/kecil:", type=["jpg", "png", "jpeg"], key="up_file")
        if file:
            st.image(file, caption="Sebelum Upscale", width=300)
            if st.button("⚡ Mulai Upscale", use_container_width=True):
                with st.spinner("🌸 Yuki sedang menjernihkan detail gambar..."):
                    result_bytes = call_deepai_api("torch-srgan", file.getvalue())
                    if result_bytes:
                        res_img = Image.open(BytesIO(result_bytes))
                        st.success("Upscale Selesai!")
                        st.image(res_img, caption="Hasil Lebih Tajam", use_container_width=True)

    # -------------------------------------------------------------
    # TAB 4: Remove Background (DeepAI Background Remover)
    # -------------------------------------------------------------
    with tabs[3]:
        st.subheader("Hapus Latar Belakang (Remove BG)")
        file = st.file_uploader("Upload foto untuk hapus background:", type=["jpg", "png", "jpeg"], key="bg_file")
        if file:
            st.image(file, caption="Gambar Asli", width=300)
            if st.button("✂️ Hapus Background", use_container_width=True):
                with st.spinner("🌸 Yuki sedang memotong background..."):
                    result_bytes = call_deepai_api("background-remover", file.getvalue())
                    if result_bytes:
                        res_img = Image.open(BytesIO(result_bytes))
                        st.success("Background Berhasil Dihapus!")
                        st.image(res_img, caption="Hasil Transparan", use_container_width=True)

    # -------------------------------------------------------------
    # TAB 5: Chat with Yuki (Google Gemini)
    # -------------------------------------------------------------
    with tabs[4]:
        st.subheader("💬 Ngobrol dengan Yuki")
        st.write("Tanya apa saja, minta ide gambar, atau ajak Yuki mengobrol santai!")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if chat_input := st.chat_input("Ketik pesan ke Yuki..."):
            if not google_key:
                st.error("GOOGLE_API_KEY belum diatur di Streamlit Secrets!")
            elif not model_chat:
                st.error("Model Gemini tidak dapat dimuat. Periksa kembali GOOGLE_API_KEY kamu.")
            else:
                st.session_state.messages.append({"role": "user", "content": chat_input})
                with st.chat_message("user"):
                    st.markdown(chat_input)
                
                with st.chat_message("assistant"):
                    with st.spinner("Yuki sedang mengetik..."):
                        try:
                            system_prompt = "Kamu adalah Yuki, asisten AI pribadi yang ramah, hangat, sedikit bergaya anime/cyberpunk, dan siap membantu pengguna dengan kreatif."
                            full_prompt = f"{system_prompt}\nPesan pengguna: {chat_input}"
                            response = model_chat.generate_content(full_prompt)
                            reply = response.text
                        except Exception as e:
                            reply = f"Maaf, Yuki lagi pusing nih: {e}"
                        st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()
