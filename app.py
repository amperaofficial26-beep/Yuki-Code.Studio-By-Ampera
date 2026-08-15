import streamlit as st
from openai import OpenAI
import time
import base64

# Konfigurasi Halaman
st.set_page_config(page_title="Ampera Multi AI", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Fungsi untuk membaca image ke base64 agar bisa muncul di dalam HTML sidebar
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_base64 = get_base64_image("logo.png")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling CSS Utama
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Cinzel:wght@700&display=swap');

    /* BACKGROUND UTAMA */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #1e1b4b, #090d16);
        background-size: 400% 400%;
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    /* MENGHILANGKAN BAR HITAM BAWAH & FOOTER */
    [data-testid="stBottom"] {{
        background-color: transparent !important;
        border-top: none !important;
    }}
    footer {{display: none !important;}}
    header {{display: none !important;}}

    /* --- LOGIN SCREEN --- */
    .login-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
        text-align: left;
        max-width: 600px;
        margin: auto;
    }}
    
    .login-logo-box {{
        background: white;
        padding: 10px 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        align-self: flex-start;
    }}

    .login-title {{
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4ade80, #38bdf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.1em;
        margin-bottom: 20px;
        text-transform: uppercase;
    }}
    
    .login-sub-text {{
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 40px;
        align-self: flex-start;
    }}

    /* --- SIDEBAR CUSTOM --- */
    [data-testid="stSidebar"] {{
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(168, 85, 247, 0.2);
    }}

    /* KARTU PROFIL SIDEBAR */
    .sidebar-card {{
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 24px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}

    .avatar-circle {{
        width: 65px;
        height: 65px;
        background: linear-gradient(135deg, #c084fc, #6366f1, #38bdf8);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.1);
    }}

    .avatar-circle img {{
        width: 80%;
        height: 80%;
        object-fit: contain;
    }}

    .profile-info {{
        display: flex;
        flex-direction: column;
    }}

    /* EFEK WARNA BERGANTI-GANTI PADA NAMA */
    @keyframes rainbowText {{
        0% {{ color: #4ade80; }}
        33% {{ color: #38bdf8; }}
        66% {{ color: #c084fc; }}
        100% {{ color: #4ade80; }}
    }}

    .profile-name {{
        font-size: 1.2rem;
        font-weight: 800;
        animation: rainbowText 4s infinite linear;
        margin-bottom: 5px;
        white-space: nowrap;
    }}

    .version-tag {{
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8 !important;
        font-size: 0.75rem;
        padding: 2px 12px;
        border-radius: 20px;
        width: fit-content;
        font-weight: 600;
    }}

    /* INPUT CHAT STYLE */
    [data-testid="stChatInput"] {{
        border-radius: 30px !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        background: rgba(15, 23, 42, 0.8) !important;
        margin-bottom: 20px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. HALAMAN LOGIN
# -------------------------------------------------------------
if not st.session_state.get("has_entered", False):
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Logo Box
    st.markdown(f'''
        <div class="login-logo-box">
            <img src="data:image/png;base64,{logo_base64}" width="50">
        </div>
    ''', unsafe_allow_html=True)

    # Title & Subtitle
    st.markdown('''
        <div class="login-title">AMPERA MULTI AI</div>
        <div class="login-sub-text">Masuk untuk melanjutkan ke Generator Laporan Otomatis</div>
    ''', unsafe_allow_html=True)
    
    # Button (Kita gunakan CSS untuk merapikan posisi tombol Streamlit)
    if st.button("Masuk", use_container_width=True):
        st.session_state["has_entered"] = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. APLIKASI UTAMA
# -------------------------------------------------------------
else:
    with st.sidebar:
        # KARTU PROFIL CUSTOM (Sesuai Gambar 3)
        st.markdown(f"""
            <div class="sidebar-card">
                <div class="avatar-circle">
                    <img src="data:image/png;base64,{logo_base64}">
                </div>
                <div class="profile-info">
                    <div class="profile-name">Ampera Multi AI</div>
                    <div class="version-tag">v2.0</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Menu Navigasi
        if st.button("🏠 Home Dashboard", use_container_width=True):
            st.session_state["current_page"] = "🏠 Home Dashboard"
        
        if st.button("⚔️ Arena Battle", use_container_width=True):
            st.session_state["current_page"] = "⚔️ Arena Battle"

        st.markdown('<div style="margin-top:20px; color:#64748b; font-size:0.8rem; padding-left:10px;">HISTORY</div>', unsafe_allow_html=True)
        st.button("⚡ Python Binary Search", use_container_width=True)

    # Isi Konten Dashboard
    if st.session_state.get("current_page", "🏠 Home Dashboard") == "🏠 Home Dashboard":
        st.markdown("<h1 style='text-align:center; font-family:Cinzel;'>What would you like to do?</h1>", unsafe_allow_html=True)
        
        # Tombol-tombol shortcut
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("🌐 Landing Page", use_container_width=True)
        with col2:
            st.button("📊 Dashboard", use_container_width=True)
        with col3:
            st.button("🎮 Make a Game", use_container_width=True)

        # Input Chat yang menyatu dengan background
        st.chat_input("Ask anything... (Tekan Enter untuk mengirim)")
