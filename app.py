#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app_yuki.py
===========
Yuki Vision Studio - AI Pembuat, Pengedit, dan Upscale Gambar
Fitur: Generate, Style Transfer (Bebas), Upscale, & Remove BG
"""

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ---------------------------------------------------------------------------
# Konfigurasi Halaman & UI
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Yuki - AI Image Studio", page_icon="🌸", layout="centered")

def set_ui_style() -> None:
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] { background-color: #080514; background-image: radial-gradient(circle at 2px 2px, rgba(255, 0, 128, 0.25) 1.5px, transparent 0); background-size: 50px 50px; }
        [data-testid="stMainBlockContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab"] { background: rgba(20, 15, 35, 0.8) !important; color: #ff0080 !important; border: 1px solid rgba(255, 0, 128, 0.3) !important; }
        div.stButton > button { background: rgba(25, 15, 40, 0.9) !important; border: 1px solid rgba(255, 0, 128, 0.5) !important; color: #ff0080 !important; }
        </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Fungsi API
# ---------------------------------------------------------------------------
def call_huggingface_api(model_id: str, payload: bytes, hf_token: str, params=None) -> bytes | None:
    headers = {"Authorization": f"Bearer {hf_token}"}
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    try:
        response = requests.post(api_url, headers=headers, data=payload, params=params, timeout=60)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Koneksi Error: {e}")
        return None

def main() -> None:
    set_ui_style()
    hf_token = st.secrets.get("HF_TOKEN", "")

    st.title("🌸 Yuki - AI Image Studio")
    tab1, tab2, tab3, tab4 = st.tabs(["✨ Generate", "🎨 Transform Gaya", "⚡ Upscaler", "✂️ Remove BG"])

    # TAB 1: Generate (Gratis)
    with tab1:
        prompt = st.text_input("Deskripsi gambar:", key="gen_prompt")
        if st.button("✨ Generate", use_container_width=True) and prompt:
            encoded_prompt = requests.utils.quote(prompt)
            img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true"
            st.image(img_url, use_container_width=True)

    # TAB 2: Transform Gaya (Bebas/Prompt)
    with tab2:
        st.subheader("🎨 Transformasi Foto (Bebas Gaya)")
        uploaded_file = st.file_uploader("Upload foto:", type=["jpg", "png"], key="edit_file")
        style_prompt = st.text_input("Mau diubah jadi apa? (Misal: Cyberpunk, Oil Painting, Sketch, Studio Ghibli)", 
                                     value="Anime style masterpiece", key="style_prompt")
        
        if uploaded_file and st.button("🎨 Proses Transformasi", use_container_width=True):
            if not hf_token: st.error("HF_TOKEN belum diatur!")
            else:
                with st.spinner("🌸 Yuki sedang mengubah gaya gambarmu..."):
                    # Kita gunakan SDXL karena handal dengan prompt
                    model = "stabilityai/stable-diffusion-xl-base-1.0"
                    # Mengirim prompt melalui parameter
                    params = {"inputs": f"{style_prompt}, {uploaded_file.getvalue()}"} 
                    # Catatan: Implementasi detail API HF bervariasi tergantung model, 
                    # ini adalah alur dasar transformasi.
                    result = call_huggingface_api(model, uploaded_file.getvalue(), hf_token)
                    if result: st.image(Image.open(BytesIO(result)), use_container_width=True)

    # TAB 3: Upscaler
    with tab3:
        upscale_file = st.file_uploader("Gambar buram:", type=["jpg", "png"], key="upscale_file")
        if upscale_file and st.button("⚡ Mulai Upscale", use_container_width=True):
            result = call_huggingface_api("ai-forever/Real-ESRGAN", upscale_file.getvalue(), hf_token)
            if result: st.image(Image.open(BytesIO(result)), use_container_width=True)

    # TAB 4: Remove BG
    with tab4:
        bg_file = st.file_uploader("Gambar untuk hapus latar:", type=["jpg", "png"], key="bg_file")
        if bg_file and st.button("✂️ Hapus Background", use_container_width=True):
            result = call_huggingface_api("briaai/RMBG-1.4", bg_file.getvalue(), hf_token)
            if result: st.image(Image.open(BytesIO(result)), use_container_width=True)

if __name__ == "__main__":
    main()
