import streamlit as st
from openai import OpenAI

# Konfigurasi Halaman
st.set_page_config(page_title="Yuki Dual-AI Coding Studio", page_icon="💻", layout="wide")

# Inisialisasi Groq API (Chat)
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling Tema Cyberpunk Coding Glassmorphism
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #080514;
        background-image: radial-gradient(circle at 2px 2px, rgba(0, 255, 204, 0.15) 1.5px, transparent 0);
        background-size: 40px 40px;
    }
    [data-testid="stMainBlockContainer"] { background: transparent !important; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(20, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 255, 204, 0.3) !important;
        color: #00ffcc !important;
        border-radius: 10px !important;
    }
    div.stButton > button {
        background: rgba(15, 30, 40, 0.9) !important;
        border: 1px solid rgba(0, 255, 204, 0.5) !important;
        color: #00ffcc !important;
        border-radius: 12px !important;
    }
    .ai-card {
        background: rgba(20, 25, 45, 0.7);
        border: 1px solid rgba(0, 255, 204, 0.2);
        padding: 20px;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💻 Yuki Dual-AI Coding Studio")
st.write("Asisten pemrograman super pintar dengan tenaga 2 AI sekaligus (Llama 3.3 & Mixtral) untuk Senpai! (≧◡≦) ✨")

# Navigasi Tab
tabs = st.tabs(["⚡ Dual AI Code Chat", "🛠️ Dual AI Code Debugger & Fixer", "🚀 Quick Code Generator"])

# -------------------------------------------------------------
# TAB 1: Dual AI Code Chat (Dua AI menjawab bersamaan)
# -------------------------------------------------------------
with tabs[0]:
    st.subheader("⚡ Tanya Coding ke 2 AI Sekaligus")
    st.write("Ketik pertanyaan pemrogramanmu, dan lihat bagaimana dua AI menganalisisnya dari sudut pandang berbeda!")
    
    code_prompt = st.text_area("Tuliskan pertanyaan, algoritma, atau masalah codingmu di sini:", key="dual_chat_input", placeholder="Contoh: Bagaimana cara membuat fungsi binary search di Python?")
    
    if st.button("🚀 Kirim ke Kedua AI", use_container_width=True) and code_prompt:
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur di Streamlit Secrets, Senpai!")
        else:
            col1, col2 = st.columns(2)
            
            # AI 1: Llama 3.3 (Senior Architect)
            with col1:
                st.markdown("### 🌸 AI 1: Yuki-Llama (Senior Architect)")
                with st.spinner("Yuki-Llama sedang menulis kode..."):
                    try:
                        res1 = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "Kamu adalah Yuki, asisten AI pemrograman yang cerdas, ramah, dan bernuansa anime. Berikan solusi kode yang bersih, efisien, dan penjelasan yang mudah dipahami."},
                                {"role": "user", "content": code_prompt}
                            ]
                        )
                        st.markdown(res1.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error AI 1: {e}")
            
            # AI 2: Mixtral (Code Reviewer & Optimizer)
            with col2:
                st.markdown("### ⚡ AI 2: Yuki-Mixtral (Code Optimizer)")
                with st.spinner("Yuki-Mixtral sedang mereview kode..."):
                    try:
                        res2 = client.chat.completions.create(
                            model="mixtral-8x7b-32768",
                            messages=[
                                {"role": "system", "content": "Kamu adalah Yuki versi Optimizer, asisten AI pemrograman kedua. Berikan sudut pandang alternatif, tips performa, atau cara optimasi dari kode yang ditanyakan."},
                                {"role": "user", "content": code_prompt}
                            ]
                        )
                        st.markdown(res2.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error AI 2: {e}")

# -------------------------------------------------------------
# TAB 2: Dual AI Code Debugger & Fixer
# -------------------------------------------------------------
with tabs[1]:
    st.subheader("🛠️ Debugging Kode dengan 2 AI")
    st.write("Punya kode yang error atau bug? Masukkan kodenya di bawah, biarkan kedua AI mencari solusinya!")
    
    buggy_code = st.text_area("Paste kode yang error di sini:", key="buggy_code_input", height=150)
    error_desc = st.text_input("Pesan error (opsional):", key="error_desc_input", placeholder="Contoh: IndexError: list index out of range")
    
    if st.button("🔍 Cari dan Perbaiki Bug", use_container_width=True) and buggy_code:
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur!")
        else:
            full_query = f"Tolong perbaiki kode yang error ini:\n\n```\n{buggy_code}\n```\nPesan Error: {error_desc}"
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🌸 Solusi dari Yuki-Llama")
                with st.spinner("Menganalisis bug..."):
                    try:
                        fix1 = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "Kamu adalah expert debugger. Temukan letak error pada kode user, berikan kode yang sudah diperbaiki, dan jelaskan kenapa itu error."},
                                {"role": "user", "content": full_query}
                            ]
                        )
                        st.markdown(fix1.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            with col2:
                st.markdown("### ⚡ Solusi dari Yuki-Mixtral")
                with st.spinner("Mencari alternatif perbaikan..."):
                    try:
                        fix2 = client.chat.completions.create(
                            model="mixtral-8x7b-32768",
                            messages=[
                                {"role": "system", "content": "Kamu adalah expert code reviewer. Berikan analisis tambahan dan cara mencegah error serupa di masa depan."},
                                {"role": "user", "content": full_query}
                            ]
                        )
                        st.markdown(fix2.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")

# -------------------------------------------------------------
# TAB 3: Quick Code Generator
# -------------------------------------------------------------
with tabs[2]:
    st.subheader("🚀 Generator Struktur / Boilerplate Code")
    st.write("Buat kerangka proyek atau script dasar secara instan.")
    
    lang = st.selectbox("Pilih Bahasa / Framework:", ["Python", "JavaScript / Node.js", "HTML / CSS / JS", "C++", "SQL"])
    project_desc = st.text_input("Apa yang ingin kamu buat?", placeholder="Contoh: Script web scraper sederhana menggunakan BeautifulSoup")
    
    if st.button("✨ Generate Kode", use_container_width=True) and project_desc:
        if not groq_key:
            st.error("API Key belum diatur!")
        else:
            with st.spinner("🌸 Yuki sedang meracik kodenya untuk Senpai..."):
                try:
                    res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": f"Kamu adalah AI pembuat kode handal. Buatkan kode lengkap dengan bahasa {lang} berdasarkan permintaan user beserta komentar penjelasannya."},
                            {"role": "user", "content": project_desc}
                        ]
                    )
                    st.success("Berhasil dibuat, Senpai! (o^▽^o)")
                    st.markdown(res.choices[0].message.content)
                except Exception as e:
                    st.error(f"Gagal: {e}")
