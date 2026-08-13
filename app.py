#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app_yuki.py
===========
Yuki Vision Studio - AI Pembuat, Pengedit, dan Upscale Gambar
Tampilan: Cyberpunk Anime Glassmorphism + Streamlit Secrets
"""

import os
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ---------------------------------------------------------------------------
# Konfigurasi Halaman
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Yuki - AI Image Studio",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS — Cyberpunk Anime Glassmorphism UI (Yuki Theme: Pink/Purple Neon)
# ---------------------------------------------------------------------------
def set_ui_style() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #080514;
            background-image: 
                radial-gradient(circle at 2px 2px, rgba(255, 0, 128, 0.25) 1.5px, transparent 0),
                linear-gradient(rgba(255, 0, 128, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 0, 128, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
        }

        [data-testid="stMainBlockContainer"] { background: transparent !important; }

        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] {
            background: rgba(20, 15, 35, 0.8) !important;
            border: 1px solid rgba(255, 0, 128, 0.3) !important;
            border-radius: 12px !important;
            color: #ff0080 !important;
            padding: 10px 20px !important;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(255, 0, 128, 0.2) !important;
            border-color: #ff0080 !important;
            color: #ffffff !important;
        }

        div.stButton > button {
            background: rgba(25, 15, 40, 0.9) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 0, 128, 0.5) !important;
            color: #ff0080 !important;
            border-radius: 14px !important;
            font-weight: 600 !important;
            padding: 10px 24px !important;
            transition: all 0.35s ease !important;
        }

        div.stButton > button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            background: rgba(255, 0, 128, 0.2) !important;
            color: #ffffff !important;
            box-shadow: 0 0 20px rgba(255, 0, 128, 0.6) !important;
        }

        [data-testid="stTextInput"] input {
            background-color: rgba(15, 10, 25, 0.8) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 0, 128, 0.4) !important;
            border-radius: 12px !important;
        }

        .yuki-foot { 
            color: rgba(180, 160, 200, 0.7); 
            font-size: 0.8rem; 
            text-align: center; 
            margin-top: 2rem; 
        }

        html, body, [class*="css"] {
            font-family: 'Segoe UI', Roboto, sans-serif !important;
            color: #f0e6f6 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Mengambil Token secara Aman dari Streamlit Secrets
# ---------------------------------------------------------------------------
def get_hf_token() -> str:
    try:
        return st.secrets.get("HF_TOKEN", "")
    except Exception:
        return ""

# ---------------------------------------------------------------------------
# Fungsi Helper untuk Hugging Face API
# ---------------------------------------------------------------------------
def call_huggingface_api(model_id: str, payload: bytes, hf_token: str) -> bytes | None:
    headers = {"Authorization": f"Bearer {hf_token}"}
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    try:
        response = requests.post(api_url, headers=headers, data=payload, timeout=60)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Gagal dari Server HF (Error {response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Koneksi API Error: {e}")
        return None

# ---------------------------------------------------------------------------
# Fungsi Utama Aplikasi Yuki
# ---------------------------------------------------------------------------
def main() -> None:
    set_ui_style()
    hf_token = get_hf_token()

    # Sidebar Ringkas
    with st.sidebar:
        st.markdown("## 🌸 Yuki Studio")
        st.write("AI Image Generator & Upscaler Studio.")
        st.divider()
        st.markdown("**Status Sistem:**")
        if hf_token:
            st.markdown('<span style="color: #00f3ff; font-weight: bold;">● Secrets Terhubung</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color: #ff0080; font-weight: bold;">● Secrets Belum Diset</span>', unsafe_allow_html=True)

    st.title("🌸 Yuki - AI Image Studio")
    st.caption("Studio Kreatif Visual: Text-to-Image, Style Transfer, & Upscaling")

    # Membuat Tab Menu Utama
    tab1, tab2, tab3 = st.tabs(["✨ Pembuat Gambar (Free)", "🎨 Ubah Gaya / Anime", "⚡ AI Upscaler"])

    # ---------------------------------------------------------------------------
    # TAB 1: Text-to-Image (Pollinations.ai - Tanpa Token)
    # ---------------------------------------------------------------------------
    with tab1:
        st.subheader("Buat Gambar dari Teks (Text-to-Image)")
        st.write("Fitur ini gratis dan tidak memerlukan API key.")
        
        prompt = st.text_input("Contoh: A cute anime cyberpunk girl with blue hair, neon lights, 4k", key="gen_prompt")
        
        col1, col2 = st.columns(2)
        with col1:
            width = st.selectbox("Lebar (Width)", [512, 768, 1024], index=1)
        with col2:
            height = st.selectbox("Tinggi (Height)", [512, 768, 1024], index=1)

        if st.button("✨ Generate Gambar", use_container_width=True):
            if not prompt.strip():
                st.warning("Mohon masukkan deskripsi gambar terlebih dahulu!")
            else:
                with st.spinner("🌸 Yuki sedang meracik gambar impianmu..."):
                    try:
                        encoded_prompt = requests.utils.quote(prompt.strip())
                        img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
                        
                        response = requests.get(img_url, timeout=30)
                        if response.status_code == 200:
                            image = Image.open(BytesIO(response.content))
                            st.success("Yeay! Gambar berhasil dibuat:")
                            st.image(image, caption=f"Prompt: {prompt}", use_container_width=True)
                            
                            buf = BytesIO()
                            image.save(buf, format="PNG")
                            st.download_button(
                                label="📥 Unduh Gambar",
                                data=buf.getvalue(),
                                file_name="yuki_generated.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        else:
                            st.error("Gagal mengambil gambar dari server.")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")

    # ---------------------------------------------------------------------------
    # TAB 2: Style Transfer / Edit (Hugging Face API via Secrets)
    # ---------------------------------------------------------------------------
    with tab2:
        st.subheader("Transformasi Foto & Edit Gaya (Anime)")
        st.write("Ubah foto kamu menjadi gaya anime menggunakan model Hugging Face.")
        
        uploaded_file = st.file_uploader("Pilih foto (JPG/PNG):", type=["jpg", "jpeg", "png"], key="edit_file")
        model_style = st.text_input("Model ID Hugging Face", value="stabilityai/stable-diffusion-xl-base-1.0", key="style_model")

        if uploaded_file:
            st.image(uploaded_file, caption="Foto Asli", width=300)
            if st.button("🎨 Proses Transformasi", use_container_width=True):
                if not hf_token:
                    st.error("HF_TOKEN belum diatur di Streamlit Secrets!")
                else:
                    with st.spinner("🌸 Yuki sedang memproses gaya gambarmu..."):
                        img_bytes = uploaded_file.getvalue()
                        result_bytes = call_huggingface_api(model_style, img_bytes, hf_token)
                        if result_bytes:
                            res_image = Image.open(BytesIO(result_bytes))
                            st.success("Berhasil diubah!")
                            st.image(res_image, caption="Hasil Transformasi", use_container_width=True)

    # ---------------------------------------------------------------------------
    # TAB 3: Upscaler (Hugging Face API via Secrets)
    # ---------------------------------------------------------------------------
    with tab3:
        st.subheader("AI Image Upscaler")
        st.write("Memperbesar resolusi dan mempertajam detail gambar buram.")
        
        upscale_file = st.file_uploader("Pilih gambar buram/kecil:", type=["jpg", "jpeg", "png"], key="upscale_file")
        model_upscale = st.text_input("Model ID Upscaler", value="ai-forever/Real-ESRGAN", key="upscale_model")
        
        if upscale_file:
            st.image(upscale_file, caption="Gambar Sebelum Upscale", width=300)
            if st.button("⚡ Mulai Upscale", use_container_width=True):
                if not hf_token:
                    st.error("HF_TOKEN belum diatur di Streamlit Secrets!")
                else:
                    with st.spinner("🌸 Yuki sedang menjernihkan detail gambar..."):
                        img_bytes = upscale_file.getvalue()
                        result_bytes = call_huggingface_api(model_upscale, img_bytes, hf_token)
                        if result_bytes:
                            res_image = Image.open(BytesIO(result_bytes))
                            st.success("Upscale Selesai!")
                            st.image(res_image, caption="Hasil Upscale Tajam", use_container_width=True)

    st.markdown('<p class="yuki-foot">Yuki AI · Free Image Studio · Cyberpunk Glassmorphism UI</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
