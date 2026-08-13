import streamlit as st
from openai import OpenAI
import requests
from PIL import Image, ImageEnhance
from io import BytesIO
from rembg import remove

# Konfigurasi Halaman
st.set_page_config(page_title="Yuki AI Studio", page_icon="🌸", layout="centered")

# Inisialisasi Groq API (Chat)
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling Tema Cyberpunk Anime Glassmorphism
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

st.title("🌸 Yuki AI Studio & Photo Suite")
st.write("Asisten chat cerdas dan studio editor foto lengkap dalam satu tempat!")

# Navigasi Tab Lengkap
tabs = st.tabs(["💬 Chat with Yuki", "✨ Text-to-Image", "🪄 AI Style", "⚡ HD Upscale", "✂️ Remove BG"])

# -------------------------------------------------------------
# TAB 1: Chat with Yuki (Groq Llama 3.3)
# -------------------------------------------------------------
with tabs[0]:
    st.subheader("💬 Ngobrol dengan Yuki")
    st.write("Tanya apa saja atau minta bantuan seputar ide kreatif!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if chat_input := st.chat_input("Ketik pesan ke Yuki..."):
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
        else:
            st.session_state.messages.append({"role": "user", "content": chat_input})
            with st.chat_message("user"):
                st.markdown(chat_input)
            
            with st.chat_message("assistant"):
                with st.spinner("Yuki sedang mengetik..."):
                    try:
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "Kamu adalah Yuki, asisten AI pribadi yang ramah, hangat, sedikit bergaya anime/cyberpunk, dan siap membantu pengguna."},
                                *st.session_state.messages
                            ]
                        )
                        reply = response.choices[0].message.content
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"Yuki pusing: {e}")

# -------------------------------------------------------------
# TAB 2: Text-to-Image (Dengan Pilihan Ukuran & Model Flux HD)
# -------------------------------------------------------------
with tabs[1]:
    st.subheader("Buat Gambar dari Teks (HD & Custom Ratio)")
    
    prompt = st.text_input("Deskripsikan gambar impianmu:", key="gen_prompt")
    
    col1, col2 = st.columns(2)
    with col1:
        aspect_ratio = st.selectbox(
            "Pilih Format / Rasio:", 
            ["Square (Kotak 1:1)", "Landscape (Mendatar 16:9)", "Portrait (Berdiri 9:16)"]
        )
    with col2:
        ai_model = st.selectbox(
            "Pilih Mesin AI:", 
            ["flux (Sangat Detail & Jernih)", "seedling (Standar / Kreatif)"]
        )
    
    if st.button("✨ Generate Gambar", use_container_width=True) and prompt:
        with st.spinner("🌸 Yuki sedang meracik gambar beresolusi tinggi..."):
            if "Landscape" in aspect_ratio:
                width, height = 1280, 720
            elif "Portrait" in aspect_ratio:
                width, height = 720, 1280
            else:
                width, height = 1024, 1024
                
            model_name = "flux" if "flux" in ai_model else "seedling"
            enhanced_prompt = f"{prompt}, highly detailed, sharp focus, masterpiece, 8k resolution"
            
            encoded = requests.utils.quote(enhanced_prompt)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&model={model_name}&nologo=true"
            
            st.success("Berhasil dibuat!")
            st.image(img_url, caption=f"Format: {aspect_ratio} | Model: {model_name}", use_container_width=True)

from huggingface_hub import InferenceClient

# Inisialisasi Hugging Face Client dengan token gratis
hf_key = st.secrets.get("HF_TOKEN", "")
hf_client = InferenceClient(token=hf_key) if hf_key else None

# -------------------------------------------------------------
# TAB 3: AI Style (True Image-to-Image via Hugging Face)
# -------------------------------------------------------------
with tabs[2]:
    st.subheader("Transformasi Gaya Foto (Hugging Face AI)")
    st.write("Mengubah foto asli secara akurat menggunakan model AI open-source gratis.")
    
    style_file = st.file_uploader("Upload foto kamu:", type=["jpg", "png", "jpeg"], key="hf_trans")
    style_prompt = st.text_input("Gaya yang diinginkan (contoh: anime style, studio ghibli, oil painting):", key="hf_style")
    
    if style_file:
        img_original = Image.open(style_file).convert("RGB")
        st.image(img_original, caption="Foto Asli", width=300)
        
        if st.button("🪄 Ubah Gaya dengan AI", use_container_width=True) and style_prompt:
            if not hf_key:
                st.error("HF_TOKEN belum diatur di Streamlit Secrets!")
            else:
                with st.spinner("🌸 Yuki sedang mengirim foto ke server AI Hugging Face..."):
                    try:
                        # Menggunakan model Stable Diffusion Image-to-Image gratis
                        # Model: stabilityai/stable-diffusion-xl-base-1.0 atau yang khusus img2img
                        image_bytes = style_file.getvalue()
                        
                        # Memanggil API Hugging Face untuk Image-to-Image
                        # Menggunakan model open-source populer yang mendukung img2img
                        output_image = hf_client.image_to_image(
                            image=image_bytes,
                            prompt=f"{style_prompt}, masterpiece, highly detailed",
                            model="stabilityai/stable-diffusion-xl-base-1.0"
                        )
                        
                        st.success("Berhasil diubah oleh AI!")
                        st.image(output_image, caption=f"Hasil: {style_prompt}", use_container_width=True)
                    except Exception as e:
                        st.error(f"Gagal memproses AI: {e}")
# -------------------------------------------------------------
# TAB 4: HD Upscale & Enhancer
# -------------------------------------------------------------
with tabs[3]:
    st.subheader("AI HD Upscale & Enhancer")
    st.write("Memperbesar resolusi dan mempertajam detail foto secara instan.")
    up_file = st.file_uploader("Upload foto buram/pecah:", type=["jpg", "png", "jpeg"], key="up_file")
    
    if up_file:
        st.image(up_file, caption="Foto Sebelum", width=300)
        if st.button("⚡ Mulai Upscale", use_container_width=True):
            with st.spinner("🌸 Yuki sedang menjernihkan detail foto..."):
                img = Image.open(up_file).convert("RGB")
                w, h = img.size
                img_resized = img.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
                
                enhancer = ImageEnhance.Sharpness(img_resized)
                img_sharp = enhancer.enhance(2.2)
                color_enhancer = ImageEnhance.Color(img_sharp)
                img_final = color_enhancer.enhance(1.1)
                
                st.success("Upscale & Enhance Berhasil!")
                st.image(img_final, caption="Hasil Lebih Tajam & HD (2x)", use_container_width=True)

# -------------------------------------------------------------
# TAB 5: Remove Background
# -------------------------------------------------------------
with tabs[4]:
    st.subheader("Hapus Latar Belakang (Remove BG)")
    st.write("Menghapus background foto secara otomatis dan menghasilkan gambar transparan.")
    bg_file = st.file_uploader("Upload foto untuk hapus background:", type=["jpg", "png", "jpeg"], key="bg_file")
    
    if bg_file:
        st.image(bg_file, caption="Foto Asli", width=300)
        if st.button("✂️ Hapus Background", use_container_width=True):
            with st.spinner("🌸 Yuki sedang memotong background dengan presisi..."):
                input_bytes = bg_file.getvalue()
                output_bytes = remove(input_bytes)
                res_img = Image.open(BytesIO(output_bytes))
                
                st.success("Background Berhasil Dihapus!")
                st.image(res_img, caption="Hasil Transparan (PNG)", use_container_width=True)
