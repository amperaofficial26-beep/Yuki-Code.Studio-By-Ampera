#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app_yuki.py
===========
Yuki Vision Studio - AI Pembuat, Pengedit, dan Upscale Gambar
Tampilan: Cyberpunk Anime Glassmorphism
"""

from __name__ == "__main__"  # Safety check
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
        /* Background Circuit Board (PCB) */
        [data-testid="stAppViewContainer"] {
            background-color: #080514;
            background-image: 
                radial-gradient(circle at 2px 2px, rgba(255, 0, 128, 0.25) 1.5px, transparent 0),
                linear-gradient(rgba(255, 0, 128, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 0, 128, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
        }

        [data-testid="stMainBlockContainer"] { background: transparent !important; }

        /* Kotak / Container Glassmorphism */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
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

        /* Tombol Neon */
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

        /* Kotak Input Teks */
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
# Fungsi Utama Aplikasi Yuki
# ---------------------------------------------------------------------------
def main() -> None:
    set_ui_style()

    st.title("🌸 Yuki - AI Image Studio")
    st.caption("Studio Kreatif Visual: Text-to-Image, Style Transfer, & Upscaling")

    # Membuat Tab Menu Utama
    tab1, tab2, tab3 = st.tabs(["✨ Pembuat Gambar (Free)", "🎨 Ubah Gaya / Anime", "⚡ AI Upscaler"])

    # ---------------------------------------------------------------------------
    # TAB 1: Text-to-Image (Menggunakan Pollinations.ai - Gratis & Tanpa API Key)
    # ---------------------------------------------------------------------------
    with tab1:
        st.subheader("Buat Gambar dari Teks (Text-to-Image)")
        st.write("Tuliskan deskripsi gambar yang kamu inginkan secara detail dalam bahasa Inggris untuk hasil terbaik.")
        
        prompt = st.text_input("Contoh: A cute anime cyberpunk girl with blue hair, neon lights, 4k resolution", key="gen_prompt")
        
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
                        # Menggunakan layanan publik gratis berbasis URL
                        encoded_prompt = requests.utils.quote(prompt.strip())
                        img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
                        
                        # Ambil gambar dari URL
                        response = requests.get(img_url, timeout=30)
                        if response.status_code == 200:
                            image = Image.open(BytesIO(response.content))
                            st.success("Yeay! Gambar berhasil dibuat:")
                            st.image(image, caption=f"Prompt: {prompt}", use_container_width=True)
                            
                            # Tombol Unduh
                            buf = BytesIO()
                            image.save(buf, format="PNG")
                            byte_im = buf.getvalue()
                            st.download_button(
                                label="📥 Unduh Gambar",
                                data=byte_im,
                                file_name="yuki_generated.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        else:
                            st.error("Gagal mengambil gambar dari server. Coba beberapa saat lagi.")
                    except Exception as e:
                        st.error(fTerjadi kesalahan: {e}")

    # ---------------------------------------------------------------------------
    # TAB 2: Style Transfer / Edit (Modifikasi Foto)
    # ---------------------------------------------------------------------------
    with tab2:
        st.subheader("Transformasi Foto & Edit Gaya")
        st.write("Unggah foto kamu untuk diubah ke gaya anime atau dimodifikasi.")
        
        uploaded_file = st.file_uploader("Pilih foto (JPG/PNG):", type=["jpg", "jpeg", "png"], key="edit_file")
        edit_prompt = st.text_input("Instruksi ubah (Misal: Turn into anime studio Ghibli style)", key="edit_prompt")

        if uploaded_file:
            st.image(uploaded_file, caption="Foto Asli", width=300)
            if st.button("🎨 Proses Transformasi", use_container_width=True):
                with st.spinner("🌸 Yuki sedang memproses gaya gambarmu..."):
                    # Placeholder logika integrasi API Edit/HuggingFace kamu selanjutnya
                    st.info("Fitur ini siap dihubungkan ke API Editor pilihanmu (seperti HuggingFace / Replicate).")

    # ---------------------------------------------------------------------------
    # TAB 3: Upscaler (Memperbesar & Menjernihkan Resolusi)
    # ---------------------------------------------------------------------------
    with tab3:
        st.subheader("AI Image Upscaler")
        st.write("Perbesar resolusi gambar buram atau kecil menjadi tajam tanpa kehilangan detail.")
        
        upscale_file = st.file_uploader("Pilih gambar buram/kecil:", type=["jpg", "jpeg", "png"], key="upscale_file")
        
        if upscale_file:
            st.image(upscale_file, caption="Gambar Sebelum Upscale", width=300)
            if st.button("⚡ Mulai Upscale (2x/4x)", use_container_width=True):
                with st.spinner("🌸 Yuki sedang menjernihkan detail gambar..."):
                    # Placeholder logika integrasi API Upscaler (Real-ESRGAN / Replicate)
                    st.info("Fitur ini siap dihubungkan ke API Upscaler pilihanmu.")

    st.markdown('<p class="yuki-foot">Yuki AI · Free Image Studio · Cyberpunk Glassmorphism UI</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()