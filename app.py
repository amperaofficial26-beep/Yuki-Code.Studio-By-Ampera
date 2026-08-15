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
    </style>
""", unsafe_allow_html=True)

st.title("💻 Yuki Dual-AI Coding Studio (DeepSeek + Mixtral)")
st.write("Studio pemrograman dengan tenaga 2 AI cerdas khusus logika dan optimasi kode untuk Senpai! (≧◡≦) ✨")

# Navigasi Tab
tabs = st.tabs(["⚡ Dual AI Code Chat", "🛠️ Dual AI Code Debugger", "🚀 Quick Code Generator"])

# -------------------------------------------------------------
# TAB 1: Dual AI Code Chat
# -------------------------------------------------------------
with tabs[0]:
    st.subheader("⚡ Tanya Coding ke DeepSeek & Mixtral")
    st.write("DeepSeek-R1 akan memberikan penalaran logika mendalam, sementara Mixtral memberikan alternatif optimal!")
    
    code_prompt = st.text_area("Tuliskan pertanyaan atau masalah codingmu:", key="dual_chat_input", placeholder="Contoh: Buatkan algoritma QuickSort di Python beserta penjelasannya")
    
    if st.button("🚀 Kirim ke Kedua AI", use_container_width=True) and code_prompt:
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur di Streamlit Secrets, Senpai!")
        else:
            col1, col2 = st.columns(2)
            
            # AI 1: DeepSeek-R1 (Master of Logic & Reasoning)
            with col1:
                st.markdown("### 🌸 AI 1: Yuki-DeepSeek (Logic & Code)")
                with st.spinner("DeepSeek sedang berpikir dan merancang logika..."):
                    try:
                        res1 = client.chat.completions.create(
                            model="deepseek-r1-distill-llama-70b",
                            messages=[
                                {"role": "system", "content": "Kamu adalah Yuki versi Code Master yang didukung DeepSeek. Berikan penalaran logika yang matang, kode bersih, dan penjelasan terstruktur."},
                                {"role": "user", "content": code_prompt}
                            ]
                        )
                        st.markdown(res1.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error AI 1: {e}")
            
            # AI 2: Mixtral (Code Reviewer & Optimizer)
            with col2:
                st.markdown("### ⚡ AI 2: Yuki-Mixtral (Optimizer)")
                with st.spinner("Mixtral sedang mereview alternatif kode..."):
                    try:
                        res2 = client.chat.completions.create(
                            model="mixtral-8x7b-32768",
                            messages=[
                                {"role": "system", "content": "Kamu adalah Yuki versi Optimizer. Berikan sudut pandang alternatif, tips performa, atau ringkasan efisiensi dari kodingan tersebut."},
                                {"role": "user", "content": code_prompt}
                            ]
                        )
                        st.markdown(res2.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error AI 2: {e}")

# -------------------------------------------------------------
# TAB 2: Dual AI Code Debugger
# -------------------------------------------------------------
with tabs[1]:
    st.subheader("🛠️ Debugging Kode dengan DeepSeek & Mixtral")
    st.write("Temukan dan perbaiki bug dengan analisis tingkat tinggi dari dua model AI!")
    
    buggy_code = st.text_area("Paste kode yang error di sini:", key="buggy_code_input", height=150)
    error_desc = st.text_input("Pesan error (opsional):", key="error_desc_input", placeholder="Contoh: NameError: name 'x' is not defined")
    
    if st.button("🔍 Analisis dan Perbaiki Bug", use_container_width=True) and buggy_code:
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur!")
        else:
            full_query = f"Tolong cari bug dan perbaiki kode ini:\n\n```\n{buggy_code}\n```\nPesan Error: {error_desc}"
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🌸 Solusi dari DeepSeek-R1")
                with st.spinner("Menganalisis akar masalah bug..."):
                    try:
                        fix1 = client.chat.completions.create(
                            model="deepseek-r1-distill-llama-70b",
                            messages=[
                                {"role": "system", "content": "Kamu adalah expert debugger. Analisis letak error secara mendalam, berikan kode yang sudah diperbaiki, dan jelaskan alasannya."},
                                {"role": "user", "content": full_query}
                            ]
                        )
                        st.markdown(fix1.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            with col2:
                st.markdown("### ⚡ Solusi dari Mixtral")
                with st.spinner("Mengecek sudut pandang lain..."):
                    try:
                        fix2 = client.chat.completions.create(
                            model="mixtral-8x7b-32768",
                            messages=[
                                {"role": "system", "content": "Kamu adalah expert code reviewer. Berikan cara pencegahan error serupa dan tips clean code."},
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
    st.subheader("🚀 Generator Kode Cepat (DeepSeek)")
    st.write("Buat kerangka program atau fungsi spesifik secara instan.")
    
    lang = st.selectbox("Pilih Bahasa Pemrograman:", ["Python", "JavaScript / Node.js", "C++", "HTML/CSS/JS", "SQL"])
    project_desc = st.text_input("Apa yang ingin kamu buat?", placeholder="Contoh: Fungsi validasi email regex di Python")
    
    if st.button("✨ Generate Kode", use_container_width=True) and project_desc:
        if not groq_key:
            st.error("API Key belum diatur!")
        else:
            with st.spinner("🌸 DeepSeek sedang meracik kodenya untuk Senpai... (o^▽^o)"):
                try:
                    res = client.chat.completions.create(
                        model="deepseek-r1-distill-llama-70b",
                        messages=[
                            {"role": "system", "content": f"Kamu adalah AI pembuat kode handal. Berikan kode {lang} yang bersih, efisien, dan siap pakai."},
                            {"role": "user", "content": project_desc}
                        ]
                    )
                    st.success("Berhasil dibuat, Senpai! ✨")
                    st.markdown(res.choices[0].message.content)
                except Exception as e:
                    st.error(f"Gagal: {e}")
