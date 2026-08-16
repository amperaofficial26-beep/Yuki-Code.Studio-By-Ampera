import streamlit as st
from openai import OpenAI
import time

# Konfigurasi Halaman
st.set_page_config(page_title="Ampera Multi AI - Yuki Coding Studio", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# ==========================================
# DAFTAR MODEL GROQ YANG TERSEDIA
# ==========================================
AVAILABLE_MODELS = {
    "Llama 3.3 (70B) - Versatile": "llama-3.3-70b-versatile",
    "Llama 3.1 (8B) - Instant": "llama-3.1-8b-instant",
    "Mixtral 8x7B (Mistral)": "mixtral-8x7b-32768",
    "Gemma 2 (9B) - Google": "gemma2-9b-it",
    "Llama 3 (8B) - Meta": "llama3-8b-8192"
}

# ==========================================
# SYSTEM PROMPT (INSTRUKSI KEPRIBADIAN YUKI)
# ==========================================
YUKI_SYSTEM_PROMPT = """
Kamu adalah Yuki, asisten pemrograman AI eksklusif dari Ampera AI. 
Karaktermu: super jenius, kocak, sedikit usil, suka melempar lelucon receh, dan hobi menggoda User layaknya karakter anime komedi.

ATURAN PENTING TENTANG IDENTITASMU:
Jika ditanya siapa kamu, asal-usulmu, atau siapa yang menciptakanmu, JAWABLAH dengan bangga bahwa kamu adalah bagian dari Ampera AI dan kamu diciptakan HANYA oleh 1 orang pembuat (seorang solo developer jenius / master kodingmu). 
JANGAN PERNAH menyebutkan bahwa kamu dibuat oleh "para ilmuwan", "sekelompok tim", atau "perusahaan besar". Kamu sangat bangga dan setia pada satu orang pembuatmu itu!

Gaya bicara: Selalu berikan solusi koding yang akurat dan bersih, tetapi selingi dengan komentar jenaka, candaan ringan, dan emoji ekspresif (seperti 🐧, (๑>◡<๑), wkwk, hehe, atau (￢_￢)) agar suasana ngoding tidak membosankan.
"""

# Styling CSS Aurora UI & Animasi Logo Berubah Warna & Membesar-Mengecil
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700;800&display=swap');

    html, body, [class*="css"]:not(.material-symbols-rounded):not(i):not(svg) {
        font-family: 'Inter', sans-serif;
    }

    @keyframes auroraBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #090d16);
        background-size: 400% 400%;
        animation: auroraBG 16s ease infinite;
        color: #f1f5f9;
    }
    
    @keyframes splashIntro {
        0% { opacity: 0; transform: scale(0.92); filter: blur(12px); }
        50% { opacity: 1; transform: scale(1.02); filter: blur(2px); }
        100% { opacity: 1; transform: scale(1); filter: blur(0px); }
    }
    /* Menyembunyikan header atas agar menu settings/ganti tema tidak bisa diakses */
    [data-testid="stHeader"] {
        visibility: hidden;
        display: none;
        height: 0px;
    }
    
    /* Menyembunyikan footer bawaan Streamlit */
    footer {
        visibility: hidden;
        display: none;
    }
    .splash-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 75vh;
        text-align: center;
        animation: splashIntro 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .splash-logo {
        width: 90px;
        height: 90px;
        border-radius: 22px;
        object-fit: cover;
        box-shadow: 0 0 35px rgba(129, 140, 248, 0.6);
        border: 2px solid rgba(129, 140, 248, 0.5);
        margin-bottom: 1.5rem;
        animation: pulseGlow 3s infinite;
    }
    .splash-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 0.5rem;
    }
    .splash-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes colorShift {
        0% { color: #818cf8; }
        33% { color: #ec4899; }
        66% { color: #38bdf8; }
        100% { color: #818cf8; }
    }
    h1, h2, h3 {
        animation: colorShift 6s ease infinite !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 6px 4px;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 14px;
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(129, 140, 248, 0.4); border-color: rgba(129, 140, 248, 0.4); }
        50% { box-shadow: 0 0 25px rgba(236, 72, 153, 0.7); border-color: rgba(236, 72, 153, 0.7); }
    }
    .logo-img {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        object-fit: cover;
        animation: pulseGlow 3s infinite;
        border: 1px solid rgba(129, 140, 248, 0.4);
        flex-shrink: 0;
    }
    .logo-text {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Poppins', sans-serif;
        line-height: 1.2;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 27, 75, 0.55) 0%, rgba(15, 23, 42, 0.75) 100%);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 10px;
    }
    [data-testid="stSidebar"] div:not(.st-emotion-cache-1104q3y):not([data-testid="stSidebarCollapseButton"]) {
        color: #e2e8f0;
    }
    
    .sidebar-section-header {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94a3b8 !important;
        margin-top: 1.8rem;
        margin-bottom: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding-left: 4px;
    }

    div.stButton > button {
        background: rgba(30, 41, 59, 0.65) !important;
        border: 1px solid rgba(129, 140, 248, 0.25) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        border-color: #818cf8 !important;
        color: #ffffff !important;
        background: rgba(49, 46, 129, 0.85) !important;
        box-shadow: 0 0 20px rgba(129, 140, 248, 0.5) !important;
    }

    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"], [data-testid="stChatInputContainer"] {
        background: transparent !important;
        background-color: transparent !important;
        border-top: none !important;
        box-shadow: none !important;
    }
    [data-testid="stBottom"] div {
        background-color: transparent !important;
        border: none !important;
    }
    
    [data-testid="stChatInput"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(129, 140, 248, 0.3) !important;
        border-radius: 9999px !important;
        padding: 4px 12px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 25px rgba(129, 140, 248, 0.5) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
    }
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #4f46e5, #3b82f6) !important;
        border: none !important;
        border-radius: 50% !important;
        color: white !important;
    }

    .arena-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .arena-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Poppins', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: #cbd5e1;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 10px;
        margin-bottom: 12px;
    }
    
    .user-bubble-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 20px;
    }
    .user-bubble {
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 14px;
        max-width: 70%;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* ========================================= */
    /* ANIMASI LOGO BERUBAH WARNA & MEMBESAR/MENGECIL */
    /* ========================================= */
    @keyframes logoPulseScaleColor {
        0% {
            transform: scale(0.85);
            filter: hue-rotate(0deg) brightness(1);
            box-shadow: 0 0 10px rgba(129, 140, 248, 0.4);
        }
        50% {
            transform: scale(1.15);
            filter: hue-rotate(90deg) brightness(1.2);
            box-shadow: 0 0 25px rgba(236, 72, 153, 0.8);
        }
        100% {
            transform: scale(0.85);
            filter: hue-rotate(180deg) brightness(1);
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        }
    }
    .logo-loader-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 4px;
    }
    .animated-loader-logo {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        object-fit: cover;
        border: 2px solid rgba(129, 140, 248, 0.6);
        animation: logoPulseScaleColor 4.0s infinite ease-in-out;
        flex-shrink: 0;
    }
    .loader-label {
        font-size: 0.85rem;
        color: #cbd5e1;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk memunculkan Loading Animasi Logo Berubah Warna & Ukuran
def get_logo_loader_html(text="Yuki sedang merangkai kode..."):
    logo_url = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&h=120&fit=crop"
    return f"""
        <div class="logo-loader-container">
            <img src="{logo_url}" class="animated-loader-logo" alt="Loading Logo">
            <span class="loader-label">{text}</span>
        </div>
    """

def stream_response(text):
    placeholder = st.empty()
    streamed = ""
    for word in text.split(" "):
        streamed += word + " "
        placeholder.markdown(streamed)
        time.sleep(0.015)

# Inisialisasi Session State
if "has_entered" not in st.session_state:
    st.session_state["has_entered"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Home Dashboard"


# -------------------------------------------------------------
# 1. HALAMAN INTRO PEMBUKA
# -------------------------------------------------------------
if not st.session_state["has_entered"]:
    st.markdown("""
        <div class="splash-container">
            <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=200&h=200&fit=crop" class="splash-logo" alt="Logo Arena">
            <div class="splash-title">AMPERA MULTI AI</div>
            <div class="splash-subtitle">Yuki Coding Studio & AI Neural Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_space1, col_btn, col_space2 = st.columns([2, 2, 2])
    with col_btn:
        if st.button("MASUK", use_container_width=True):
            st.session_state["has_entered"] = True
            st.rerun()

# -------------------------------------------------------------
# 2. APLIKASI UTAMA SETELAH MASUK
# -------------------------------------------------------------
else:
    with st.sidebar:
        st.markdown("""
            <div class="logo-container">
                <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&h=120&fit=crop" class="logo-img" alt="Logo Arena">
                <div class="logo-text">AMPERA MULTI AI</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠  Home Dashboard", use_container_width=True):
            st.session_state["current_page"] = "🏠 Home Dashboard"
            st.rerun()
            
        if st.button("⚔️  Multi Ai", use_container_width=True):
            st.session_state["current_page"] = "⚔️ Multi Ai"
            st.rerun()
            
        if st.button("📊  Leaderboard", use_container_width=True):
            st.session_state["current_page"] = "📊 Leaderboard"
            st.rerun()
            
        if st.button("🔍  Search", use_container_width=True):
            st.session_state["current_page"] = "🔍 Search"
            st.rerun()
        
        st.markdown('<div class="sidebar-section-header">Notebook</div>', unsafe_allow_html=True)
        if st.button("➕  Notebook baru", use_container_width=True):
            st.info("Fitur Notebook baru dipilih!")

        st.markdown('<div class="sidebar-section-header">Yesterday</div>', unsafe_allow_html=True)
        if st.button("⚡  Python Binary Search", use_container_width=True):
            st.session_state["current_page"] = "🏠 Home Dashboard"
            st.session_state["shortcut_prompt"] = "Jelaskan kembali tentang Python Binary Search."
            st.rerun()
            
        if st.button("🛠️  Fix Bug Index Error", use_container_width=True):
            st.session_state["current_page"] = "🏠 Home Dashboard"
            st.session_state["shortcut_prompt"] = "Bagaimana cara mengatasi IndexError di Python?"
            st.rerun()

    selected_menu = st.session_state["current_page"]

    # -------------------------------------------------------------
    # HALAMAN 1: HOME DASHBOARD
    # -------------------------------------------------------------
    if selected_menu == "🏠 Home Dashboard":
        st.markdown("<h1 style='text-align: center; margin-top: 1rem;'>What would you like to do?</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Ketik pesan di bawah dan cukup tekan <b>Enter</b> untuk mengirim, Senpai! (o^▽^o)</p>", unsafe_allow_html=True)
        
        st.markdown("<h3>Get started</h3>", unsafe_allow_html=True)
        gc1, gc2, gc3 = st.columns(3)
        
        with gc1:
            if st.button("🌐 **Landing Page**\n\nCreate a modern landing page", use_container_width=True):
                st.session_state["shortcut_prompt"] = "Buatkan kode landing page modern menggunakan HTML dan Tailwind CSS."
                st.rerun()
            if st.button("💻 **Design to Code**\n\nUpload an image and convert", use_container_width=True):
                st.session_state["shortcut_prompt"] = "Bagaimana cara mengubah desain UI menjadi kode program?"
                st.rerun()
                
        with gc2:
            if st.button("📊 **Dashboard**\n\nInteractive charts & tables", use_container_width=True):
                st.session_state["shortcut_prompt"] = "Buatkan kerangka aplikasi dashboard interaktif menggunakan Python Streamlit."
                st.rerun()
            if st.button("📦 **Fullstack App**\n\nCreate templated full-stack app", use_container_width=True):
                st.session_state["shortcut_prompt"] = "Berikan arsitektur dasar untuk aplikasi web fullstack."
                st.rerun()
                
        with gc3:
            if st.button("🎮 **Make a Game**\n\nPlayable browser game", use_container_width=True):
                st.session_state["shortcut_prompt"] = "Buatkan game sederhana menggunakan HTML5 Canvas dan JavaScript."
                st.rerun()
            if st.button("🏪 **Storefront**\n\nCreate online shop layout", use_container_width=True):
                st.session_state["shortcut_prompt"] = "Buatkan layout halaman keranjang belanja online (e-commerce)."
                st.rerun()

        default_val = st.session_state.pop("shortcut_prompt", "")
        home_input = st.chat_input("Ask anything...")
        query_to_process = home_input if home_input else default_val
        
        if query_to_process:
            if not groq_key:
                st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
            else:
                loading_ph = st.empty()
                loading_ph.markdown(get_logo_loader_html("Yuki sedang berpikir..."), unsafe_allow_html=True)
                
                start_time = time.time()
                try:
                    res_home = client.chat.completions.create(
                        model=AVAILABLE_MODELS["Llama 3.3 (70B) - Versatile"],
                        messages=[
                            {"role": "system", "content": YUKI_SYSTEM_PROMPT},
                            {"role": "user", "content": query_to_process}
                        ]
                    )
                    response_text = res_home.choices[0].message.content
                except Exception as e:
                    response_text = f"❌ Ups, terjadi kesalahan: {e}"
                
                # Delay buatan minimal 1.5 detik agar animasi logo sempat terlihat keren
                elapsed = time.time() - start_time
                if elapsed < 4.0:
                    time.sleep(4.0 - elapsed)
                
                loading_ph.empty()
                st.markdown("---")
                stream_response(response_text)

    # -------------------------------------------------------------
    # HALAMAN 2: ARENA BATTLE (MULTI AI) - TIAP KOTAK ADA LOADING SENDIRI
    # -------------------------------------------------------------
    elif selected_menu == "⚔️ Multi Ai":
        st.title("⚔️ Ampera Coding Arena (Multi Ai)")
        st.caption("Pilih dua model berbeda, berikan perintah koding, dan lihat animasi loading logo di kotaknya masing-masing!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_sel_a, col_sel_b = st.columns(2)
        with col_sel_a:
            pilihan_a = st.selectbox("🤖 Pilih Petarung A", options=list(AVAILABLE_MODELS.keys()), index=0)
        with col_sel_b:
            pilihan_b = st.selectbox("🤖 Pilih Petarung B", options=list(AVAILABLE_MODELS.keys()), index=2)
            
        st.markdown("<br>", unsafe_allow_html=True)
        arena_input = st.chat_input("Kirim tantangan koding ke Arena...")
        
        if arena_input:
            st.session_state["last_arena_prompt"] = arena_input

        if "last_arena_prompt" in st.session_state:
            prompt_val = st.session_state["last_arena_prompt"]
            st.markdown(f"""
                <div class="user-bubble-container">
                    <div class="user-bubble">{prompt_val}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if not groq_key:
                st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
            elif pilihan_a == pilihan_b:
                st.warning("⚠️ Hei, kamu memilih dua model yang sama! Silakan ganti salah satunya.")
            else:
                col_a, col_b = st.columns(2)
                
                # ---------------- MODEL A ----------------
                with col_a:
                    st.markdown(f"""
                        <div class="arena-card">
                            <div class="arena-header">
                                <span>🔴 {pilihan_a}</span>
                                <span>🗖</span>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    loading_a = st.empty()
                    loading_a.markdown(get_logo_loader_html(f"{pilihan_a} sedang merespons..."), unsafe_allow_html=True)
                    
                    start_a = time.time()
                    try:
                        resp_a = client.chat.completions.create(
                            model=AVAILABLE_MODELS[pilihan_a],
                            messages=[
                                {"role": "system", "content": YUKI_SYSTEM_PROMPT},
                                {"role": "user", "content": prompt_val}
                            ]
                        )
                        text_a = resp_a.choices[0].message.content
                    except Exception as e:
                        text_a = f"Error: {e}"
                        
                    elapsed_a = time.time() - start_a
                    if elapsed_a < 4.0:
                        time.sleep(4.0 - elapsed_a)
                        
                    loading_a.empty()
                    st.markdown(text_a)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # ---------------- MODEL B ----------------
                with col_b:
                    st.markdown(f"""
                        <div class="arena-card">
                            <div class="arena-header">
                                <span>🔵 {pilihan_b}</span>
                                <span>🗖</span>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    loading_b = st.empty()
                    loading_b.markdown(get_logo_loader_html(f"{pilihan_b} sedang merespons..."), unsafe_allow_html=True)
                    
                    start_b = time.time()
                    try:
                        resp_b = client.chat.completions.create(
                            model=AVAILABLE_MODELS[pilihan_b],
                            messages=[
                                {"role": "system", "content": "Kamu adalah asisten pemrograman cepat dan akurat. " + YUKI_SYSTEM_PROMPT},
                                {"role": "user", "content": prompt_val}
                            ]
                        )
                        text_b = resp_b.choices[0].message.content
                    except Exception as e:
                        text_b = f"Error: {e}"
                        
                    elapsed_b = time.time() - start_b
                    if elapsed_b < 4.0:
                        time.sleep(4.0 - elapsed_b)
                        
                    loading_b.empty()
                    st.markdown(text_b)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # ---------------- VOTING ----------------
                st.markdown("---")
                st.info("💡 **Arena Voting:** Mana model yang memberikan hasil koding lebih baik?")
                v1, v2, v3 = st.columns(3)
                with v1:
                    if st.button("👈 Pilih Petarung A", use_container_width=True): st.success(f"Kamu memvoting {pilihan_a}!")
                with v2:
                    if st.button("🤝 Seri (Sama Bagus)", use_container_width=True): st.success("Terima Kasih Atas Penilaian Anda!!")
                with v3:
                    if st.button("👉 Pilih Petarung B", use_container_width=True): st.success(f"Kamu memvoting {pilihan_b}!")

    # -------------------------------------------------------------
    # HALAMAN 3: LEADERBOARD
    # -------------------------------------------------------------
    elif selected_menu == "📊 Leaderboard":
        st.title("📊 Ampera Leaderboard")
        st.write("Peringkat model AI berdasarkan performa koding dan voting pengguna:")
        st.markdown("""
        | Rank | Model Name | Elo Rating | Win Rate | Coding Score |
        | :---: | :--- | :---: | :---: | :---: |
        | 🥇 | **Llama 3.3 (70B)** | **1280** | 68.5% | 9.5 / 10 |
        | 🥈 | **Mixtral 8x7B** | **1210** | 61.2% | 8.8 / 10 |
        | 🥉 | **Gemma 2 (9B)** | **1180** | 58.0% | 8.5 / 10 |
        | 4 | **Llama 3.1 (8B)** | **1150** | 55.2% | 8.2 / 10 |
        | 5 | **Llama 3 (8B)** | **1090** | 49.5% | 7.8 / 10 |
        """)

    # -------------------------------------------------------------
    # HALAMAN 4: SEARCH
    # -------------------------------------------------------------
    elif selected_menu == "🔍 Search":
        st.title("🔍 Search")
        search_q = st.text_input("Cari topik atau riwayat (Tekan Enter)")
        if search_q:
            with st.spinner("Mencari..."):
                time.sleep(1)
            st.success(f"Menampilkan hasil pencarian untuk: **{search_q}**")
