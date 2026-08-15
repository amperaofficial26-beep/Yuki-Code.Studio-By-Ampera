import streamlit as st
from openai import OpenAI

# Konfigurasi Halaman (Lebar agar mirip Arena)
st.set_page_config(page_title="Yuki Arena Coding Studio", page_icon="⚔️", layout="wide")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling Tema Chatbot Arena (Clean, Dark, Modern Tech)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    [data-testid="stMainBlockContainer"] { 
        background: #0e1117 !important; 
        max-width: 100% !important;
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #58a6ff !important;
        border-radius: 6px !important;
        font-weight: 600;
    }
    div.stButton > button {
        background: #238636 !important;
        border: 1px solid #2ea043 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background: #2ea043 !important;
    }
    .arena-box {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Header ala Arena
st.title("⚔️ Yuki Coding Arena (Model Battle)")
st.caption("Uji dan bandingkan performa dua model AI pemrograman secara head-to-head, ala Chatbot Arena! (o^▽^o)")

# Navigasi Tab Utama
tabs = st.tabs(["⚔️ Arena Battle (Side-by-Side)", "🛠️ Debugger & Optimizer Arena", "🚀 Quick Generator"])

# -------------------------------------------------------------
# TAB 1: Arena Battle (Side-by-Side Comparison)
# -------------------------------------------------------------
with tabs[0]:
    st.markdown("### 🤖 Blind / Head-to-Head Model Comparison")
    st.write("Kirimkan satu perintah koding, dan lihat bagaimana **Llama 3.3 (70B)** dan **Llama 3.1 (8B)** menyelesaikan masalah tersebut secara bersamaan.")
    
    prompt_arena = st.text_area("Masukkan prompt atau masalah koding Senpai di sini:", key="arena_prompt", placeholder="Contoh: Buatkan implementasi Linked List sederhana dalam bahasa Python.")
    
    if st.button("⚔️ Mulai Battle!", use_container_width=True) and prompt_arena:
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
        else:
            col_a, col_b = st.columns(2)
            
            # Kolom Model A (Llama 3.3 70B)
            with col_a:
                st.markdown("### 🧬 Model A (Llama 3.3 - 70B)")
                with st.spinner("Model A sedang meracik kode..."):
                    try:
                        resp_a = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "Kamu adalah asisten pemrograman ahli. Berikan kode yang bersih, efisien, dan penjelasan yang mendalam."},
                                {"role": "user", "content": prompt_arena}
                            ]
                        )
                        st.markdown(resp_a.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error Model A: {e}")
            
            # Kolom Model B (Llama 3.1 8B)
            with col_b:
                st.markdown("### ⚡ Model B (Llama 3.1 - 8B Instant)")
                with st.spinner("Model B sedang meracik kode..."):
                    try:
                        resp_b = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "Kamu adalah asisten pemrograman cepat dan akurat. Berikan solusi kode yang ringkas dan langsung pada sasaran."},
                                {"role": "user", "content": prompt_arena}
                            ]
                        )
                        st.markdown(resp_b.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error Model B: {e}")
            
            st.markdown("---")
            st.info("💡 **Arena Voting:** Menurut Senpai, model mana yang memberikan hasil koding lebih baik? (≧◡≦)")
            v_col1, v_col2, v_col3 = st.columns(3)
            with v_col1:
                if st.button("👈 Model A Unggul"):
                    st.success("Terima kasih! Suara untuk Model A dicatat.")
            with v_col2:
                if st.button("🤝 Seri / Keduanya Bagus"):
                    st.success("Terima kasih! Hasil seri dicatat.")
            with v_col3:
                if st.button("👉 Model B Unggul"):
                    st.success("Terima kasih! Suara untuk Model B dicatat.")

# -------------------------------------------------------------
# TAB 2: Debugger & Optimizer Arena
# -------------------------------------------------------------
with tabs[1]:
    st.markdown("### 🛠️ Code Debugger Arena")
    st.write("Masukkan kode yang error, biarkan kedua model bersaing memberikan perbaikan terbaik.")
    
    bug_code = st.text_area("Paste kode yang bermasalah:", height=150, key="arena_bug")
    bug_desc = st.text_input("Deskripsi error (opsional):", placeholder="Contoh: Infinite loop atau TypeError")
    
    if st.button("🔍 Bandingkan Solusi Debug", use_container_width=True) and bug_code:
        if not groq_key:
            st.error("API Key belum diatur!")
        else:
            query_bug = f"Perbaiki kode yang error ini:\n\n```\n{bug_code}\n```\nError: {bug_desc}"
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("### 🧬 Solusi Model A")
                with st.spinner("Menganalisis bug..."):
                    try:
                        fix_a = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "Kamu adalah expert debugger. Temukan akar masalah dan berikan kode yang sudah diperbaiki."},
                                {"role": "user", "content": query_bug}
                            ]
                        )
                        st.markdown(fix_a.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            with col_b:
                st.markdown("### ⚡ Solusi Model B")
                with st.spinner("Menganalisis bug..."):
                    try:
                        fix_b = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "Kamu adalah expert debugger cepat. Berikan solusi perbaikan kode yang efisien."},
                                {"role": "user", "content": query_bug}
                            ]
                        )
                        st.markdown(fix_b.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")

# -------------------------------------------------------------
# TAB 3: Quick Generator
# -------------------------------------------------------------
with tabs[2]:
    st.markdown("### 🚀 Quick Code Generator Arena")
    st.write("Buat kerangka kode instan dengan model pilihan terbaik.")
    
    gen_lang = st.selectbox("Bahasa Pemrograman:", ["Python", "JavaScript", "HTML/CSS", "C++", "SQL"])
    gen_desc = st.text_input("Fitur atau program apa yang ingin dibuat?", placeholder="Contoh: Form login sederhana dengan validasi")
    
    if st.button("✨ Generate Cepat", use_container_width=True) and gen_desc:
        if not groq_key:
            st.error("API Key belum diatur!")
        else:
            with st.spinner("🌸 Yuki sedang membuat kode..."):
                try:
                    res_gen = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": f"Buatkan kode {gen_lang} yang lengkap, bersih, dan langsung bisa dijalankan."},
                            {"role": "user", "content": gen_desc}
                        ]
                    )
                    st.success("Berhasil dibuat, Senpai! (o^▽^o)")
                    st.markdown(res_gen.choices[0].message.content)
                except Exception as e:
                    st.error(f"Gagal: {e}")
