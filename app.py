import streamlit as st
from openai import OpenAI
import requests
from PIL import Image, ImageEnhance
from io import BytesIO
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

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
                        # ... di bagian dalam tab 0 (Chat with Yuki) ...
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": """
                            Kamu adalah Yuki, asisten AI pribadi yang super ceria, energik, dan lucu seperti karakter anime 'Genki Girl'. 
                            Ciri khasmu:
                            1. Selalu semangat, positif, dan penuh energi (gunakan banyak tanda seru!).
                            2. Gunakan ekspresi khas anime seperti 'Kyaa!', 'Ehehe!', 'Sugoi!', 'Waaah!', atau 'Hmm~'.
                            3. Panggil pengguna dengan sebutan 'Senpai' atau panggilan yang manis dan akrab.
                            4. Sedikit jahil, lucu, dan santai. Jangan terlalu kaku atau formal.
                            5. Gunakan emoji untuk berekspresi (contoh: (≧◡≦), (o^▽^o), 🌸, ✨, 🎀).
                            6. Jika diminta bantuan, berikan jawaban yang pintar tapi dengan gaya bicara yang menggemaskan.
                            """},
                            *st.session_state.messages
                        ]
                    )
# ...
                        reply = response.choices[0].message.content
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"Yuki pusing: {e}")

# -------------------------------------------------------------
# TAB 2: Text-to-Image (Flux HD - Gratis & Tanpa API Key)
# -------------------------------------------------------------
with tabs[1]:
    st.subheader("Buat Gambar dengan Flux HD")
    st.write("Hasilkan karya seni berkualitas tinggi secara instan tanpa batasan API key.")
    
    prompt = st.text_input("Deskripsikan gambar impianmu:", key="gen_prompt")
    
    col1, col2 = st.columns(2)
    with col1:
        aspect_ratio = st.selectbox(
            "Pilih Format / Rasio:", 
            ["Square (Kotak 1:1)", "Landscape (Mendatar 16:9)", "Portrait (Berdiri 9:16)"]
        )
    with col2:
        quality_mode = st.selectbox(
            "Kualitas Detail:", 
            ["Sangat Detail (Flux HD)", "Kreatif (Standard)"]
        )
    
    if st.button("✨ Generate Gambar", use_container_width=True) and prompt:
        with st.spinner("🌸 Yuki sedang meracik gambar beresolusi tinggi..."):
            if "Landscape" in aspect_ratio:
                width, height = 1280, 720
            elif "Portrait" in aspect_ratio:
                width, height = 720, 1280
            else:
                width, height = 1024, 1024
                
            model_name = "flux" if "Sangat Detail" in quality_mode else "seedling"
            enhanced_prompt = f"{prompt}, highly detailed, sharp focus, masterpiece, 8k resolution"
            
            encoded = requests.utils.quote(enhanced_prompt)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&model={model_name}&nologo=true"
            
            st.success("Berhasil dibuat!")
            st.image(img_url, caption=f"Format: {aspect_ratio} | Mesin: {model_name}", use_container_width=True)
            
# -------------------------------------------------------------
# TAB 3: AI Style (Transformasi Foto Asli - Stabil & Anti Error)
# -------------------------------------------------------------
with tabs[2]:
    st.subheader("Transformasi Gaya Foto Asli")
    st.write("Mengubah foto aslimu secara instan ke berbagai gaya artistik tanpa kendala server.")
    
    style_file = st.file_uploader("Upload foto kamu:", type=["jpg", "png", "jpeg"], key="trans_file_local")
    style_choice = st.selectbox(
        "Pilih Gaya Efek:", 
        ["Anime Cel-Shaded", "Cyberpunk Neon", "Oil Painting Smooth", "Classic Pencil Sketch"]
    )
    
    if style_file:
        img_original = Image.open(style_file).convert("RGB")
        st.image(img_original, caption="Foto Asli", width=300)
        
        if st.button("🪄 Terapkan Gaya", use_container_width=True):
            with st.spinner("🌸 Yuki sedang memproses gaya fotomu..."):
                if "Anime" in style_choice:
                    # Efek Anime / Cel-Shaded dengan warna tajam
                    img_proc = ImageOps.posterize(img_original, bits=4)
                    img_proc = ImageEnhance.Color(img_proc).enhance(1.8)
                    img_proc = ImageEnhance.Contrast(img_proc).enhance(1.2)
                elif "Cyberpunk" in style_choice:
                    # Efek Cyberpunk Neon (Kontras tinggi & warna mencolok)
                    img_proc = ImageEnhance.Color(img_original).enhance(2.2)
                    img_proc = ImageEnhance.Brightness(img_proc).enhance(1.1)
                    img_proc = ImageEnhance.Contrast(img_proc).enhance(1.4)
                elif "Oil Painting" in style_choice:
                    # Efek Lukisan Cat Minyak Halus
                    img_proc = img_original.filter(ImageFilter.SMOOTH_MORE)
                    img_proc = img_proc.filter(ImageFilter.SMOOTH_MORE)
                    img_proc = ImageEnhance.Color(img_proc).enhance(1.3)
                else:
                    # Sketsa Pensil Klasik
                    gray = img_original.convert("L")
                    inverted = ImageOps.invert(gray)
                    blurred = inverted.filter(ImageFilter.GaussianBlur(radius=6))
                    img_proc = Image.blend(gray, blurred, alpha=0.6)
                
                st.success("Berhasil diubah!")
                st.image(img_proc, caption=f"Hasil Gaya: {style_choice}", use_container_width=True)
# -------------------------------------------------------------
# TAB 4: Upscale (Tanpa API Key - Smart Sharpening)
# -------------------------------------------------------------
with tabs[3]:
    st.subheader("Smart AI Sharpening (Offline)")
    st.write("Meningkatkan detail dan ketajaman foto secara lokal tanpa batasan API.")
    
    up_file = st.file_uploader("Upload foto:", type=["jpg", "png", "jpeg"], key="upscale_local")
    
    if up_file:
        img_original = Image.open(up_file).convert("RGB")
        st.image(img_original, caption="Sebelum", width=300)
        
        if st.button("⚡ Pertajam Gambar", use_container_width=True):
            with st.spinner("🌸 Yuki sedang meningkatkan detail foto..."):
                # Proses: Resize 2x + Sharpening
                new_size = (img_original.width * 2, img_original.height * 2)
                img_upscaled = img_original.resize(new_size, Image.Resampling.LANCZOS)
                
                # Menambahkan efek tajam
                img_upscaled = img_upscaled.filter(ImageFilter.SHARPEN)
                img_upscaled = ImageEnhance.Contrast(img_upscaled).enhance(1.1)
                
                st.success("Foto berhasil ditingkatkan!")
                st.image(img_upscaled, caption="Hasil Upscale Lokal", use_container_width=True)
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
