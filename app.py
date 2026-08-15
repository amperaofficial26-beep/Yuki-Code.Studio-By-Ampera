import streamlit as st
from openai import OpenAI
import time

# Konfigurasi Halaman
st.set_page_config(page_title="Ampera Multi AI", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling CSS Aurora UI & Perbaikan Tampilan Sesuai Gambar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Cinzel:wght@700&display=swap');

    /* BACKGROUND ANIMASI */
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
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* MENGHILANGKAN BAR HITAM DI BAWAH (Chat Input menyatu dengan BG) */
    [data-testid="stBottom"] {
        background-color: transparent !important;
        border-top: none !important;
    }
    footer {display: none !important;}

    /* LAYOUT UTAMA LOGIN DI TENGAH */
    .stMainBlockContainer {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 85vh;
    }
    
    /* KARTU LOGIN (Glow Ungu sesuai gambar) */
    .login-card-box {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(25px);
        border: 2px solid rgba(168, 85, 247, 0.4);
        border-radius: 30px;
        padding: 50px 40px;
        text-align: center;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.3), inset 0 0 20px rgba(168, 85, 247, 0.1);
        max-width: 500px;
        width: 100%;
        margin: auto;
        animation: cardAppear 0.8s ease-out;
    }
    @keyframes cardAppear {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .login-title-text {
        font-family: 'Cinzel', serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4ade80 0%, #38bdf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .login-sub-text {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 2.5rem;
    }

    /* STYLING SIDEBAR (Glassmorphism & Profile) */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .sidebar-profile-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 20px;
        padding: 16px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-avatar-circle {
        width: 55px;
        height: 55px;
        background: linear-gradient(135deg, #c084fc 0%, #6366f1 50%, #38bdf8 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 800;
        font-size: 1.5rem;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.5);
        flex-shrink: 0;
    }
    
    .sidebar-profile-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: -2px;
    }
    
    .sidebar-profile-sub {
        font-size: 0.85rem;
        color: #94a3b8 !important;
    }
    
    .sidebar-version-badge {
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8 !important;
        font-size: 0.75rem;
        padding: 2px 10px;
        border-radius: 20px;
        margin-top: 5px;
        display: inline-block;
    }

    /* TOMBOL STYLING */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: rgba(168, 85, 247, 0.2) !important;
        border-color: #c084fc !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
    }

    /* INPUT CHAT STYLING */
    [data-testid="stChatInput"] {
        border-radius: 15px !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        background: rgba(15, 23, 42, 0.8) !important;
    }
    </style>
""", unsafe_allow_html=True)

def stream_response(text):
    placeholder = st.empty()
    streamed = ""
    for word in text.split(" "):
        streamed += word + " "
        placeholder.markdown(streamed)
        time.sleep(0.015)

if "has_entered" not in st.session_state:
    st.session_state["has_entered"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Home Dashboard"

# -------------------------------------------------------------
# 1. HALAMAN LOGIN
# -------------------------------------------------------------
if not st.session_state["has_entered"]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card-box">', unsafe_allow_html=True)
        
        # Logo Ampera
        try:
            st.image("logo.png", width=70) # Pastikan file logo.png ada
        except:
            st.markdown("<h1 style='font-size: 3rem;'>🏛️</h1>", unsafe_allow_html=True)

        st.markdown("""
            <div class="login-title-text">Ampera Multi AI</div>
            <div class="login-sub-text">Masuk untuk melanjutkan ke Generator Laporan Otomatis</div>
        """, unsafe_allow_html=True)
        
        # Tombol Masuk
        if st.button("Masuk", use_container_width=True):
            st.session_state["has_entered"] = True
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
            
# -------------------------------------------------------------
# 2. APLIKASI UTAMA (Setelah Login)
# -------------------------------------------------------------
else:
    with st.sidebar:
        # User Profile Card (Sesuai Gambar 3)
        st.markdown(f"""
            <div class="sidebar-profile-card">
                <div class="sidebar-avatar-circle">A</div>
                <div class="sidebar-profile-info">
                    <div class="sidebar-profile-name">admin</div>
                    <div class="sidebar-profile-sub">Anggota Ampera Multi AI</div>
                    <div class="sidebar-version-badge">v2.0</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        if st.button("🏠 Home Dashboard", use_container_width=True):
            st.session_state["current_page"] = "🏠 Home Dashboard"
            st.rerun()
        if st.button("⚔️ Arena Battle", use_container_width=True):
            st.session_state["current_page"] = "⚔️ Arena Battle"
            st.rerun()
        if st.button("📊 Leaderboard", use_container_width=True):
            st.session_state["current_page"] = "📊 Leaderboard"
            st.rerun()
        if st.button("🔍 Search", use_container_width=True):
            st.session_state["current_page"] = "🔍 Search"
            st.rerun()
        
        st.markdown('<div style="color:#94a3b8; font-size:0.75rem; margin-top:2rem; padding-left:5px;">HISTORY</div>', unsafe_allow_html=True)
        st.button("⚡ Python Binary Search", use_container_width=True)
        st.button("🛠️ Fix Bug Index Error", use_container_width=True)

    # PAGE CONTENT
    selected_menu = st.session_state["current_page"]

    if selected_menu == "🏠 Home Dashboard":
        st.markdown("<h1 style='text-align: center; margin-top: 1rem; font-family: \"Cinzel\", serif;'>What would you like to do?</h1>", unsafe_allow_html=True)
        
        # Shortcuts Grid
        gc1, gc2, gc3 = st.columns(3)
        with gc1:
            st.button("🌐 **Landing Page**\n\nCreate a modern landing page", use_container_width=True)
            st.button("💻 **Design to Code**\n\nUpload an image and convert", use_container_width=True)
        with gc2:
            st.button("📊 **Dashboard**\n\nInteractive charts & tables", use_container_width=True)
            st.button("📦 **Fullstack App**\n\nCreate templated full-stack app", use_container_width=True)
        with gc3:
            st.button("🎮 **Make a Game**\n\nPlayable browser game", use_container_width=True)
            st.button("🏪 **Storefront**\n\nCreate online shop layout", use_container_width=True)

        # Chat Input (Sekarang menyatu dengan background)
        home_input = st.chat_input("Ask anything... (Tekan Enter untuk mengirim)")
        
        if home_input:
            with st.status("🧠 Memproses permintaan...", expanded=True) as status:
                time.sleep(1.5)
                if groq_key:
                    res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": home_input}]
                    )
                    response_text = res.choices[0].message.content
                else:
                    response_text = "API Key tidak ditemukan. Mohon atur di Secrets."
                status.update(label="Selesai!", state="complete", expanded=False)
            
            st.markdown("---")
            stream_response(response_text)

    # Tambahkan Logika untuk halaman lainnya di sini (Arena, Leaderboard, dll) sesuai kebutuhan Anda
