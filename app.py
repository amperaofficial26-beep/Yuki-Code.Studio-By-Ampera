import streamlit as st
from openai import OpenAI
import time
import base64

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Ampera Multi AI", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Fungsi untuk load gambar ke HTML
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_base64 = get_base64_image("logo.png")

# 2. STYLE CSS (Fokus pada perbaikan tampilan & animasi)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Cinzel:wght@700&display=swap');

    /* Background Utama */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #161e35, #090d16);
        background-size: 400% 400%;
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* Hilangkan Header & Footer bawaan */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* MENGHILANGKAN AREA HITAM DI BAWAH */
    [data-testid="stBottom"] {{
        background-color: transparent !important;
        border: none !important;
    }}

    /* --- LOGIN UI --- */
    .login-box {{
        margin-top: 10vh;
        padding: 40px;
    }}
    
    .logo-container-login {{
        background: white;
        padding: 8px 15px;
        border-radius: 10px;
        display: inline-block;
        margin-bottom: 25px;
    }}

    /* Animasi Pelangi untuk Nama Aplikasi */
    @keyframes rainbow {{
        0% {{ color: #4ade80; }}
        33% {{ color: #38bdf8; }}
        66% {{ color: #c084fc; }}
        100% {{ color: #4ade80; }}
    }}

    .login-title {{
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        animation: rainbow 5s infinite linear;
        margin-bottom: 10px;
    }}

    .login-subtitle {{
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 50px;
    }}

    /* --- SIDEBAR UI --- */
    [data-testid="stSidebar"] {{
        background: rgba(15, 23, 42, 0.9) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(168, 85, 247, 0.2);
    }}

    /* Kartu Profil Sidebar sesuai Gambar 3 */
    .sidebar-profile-card {{
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 20px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }}

    .avatar-glow {{
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #c084fc, #38bdf8);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.6);
        flex-shrink: 0;
        overflow: hidden;
    }}
    
    .avatar-glow img {{
        width: 70%;
        height: 70%;
        object-fit: contain;
    }}

    .profile-name-sidebar {{
        font-size: 1.1rem;
        font-weight: 700;
        animation: rainbow 5s infinite linear;
    }}

    .badge-v2 {{
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8 !important;
        font-size: 0.7rem;
        padding: 2px 10px;
        border-radius: 20px;
        margin-top: 4px;
        display: inline-block;
        font-weight: 600;
    }}

    /* Tombol Masuk & Navigasi */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        transition: 0.3s;
        text-align: center;
    }}
    div.stButton > button:hover {{
        background: rgba(168, 85, 247, 0.2) !important;
        border-color: #c084fc !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
    }}

    /* Chat Input */
    [data-testid="stChatInput"] {{
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 20px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 3. LOGIKA HALAMAN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- HALAMAN MASUK (LOGIN) ---
if not st.session_state.logged_in:
    # Menggunakan columns agar tampilan berada di tengah secara aman
    col_l, col_main, col_r = st.columns([1, 4, 1])
    
    with col_main:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        # Logo Box (Putih)
        if logo_base64:
            st.markdown(f'<div class="logo-container-login"><img src="data:image/png;base64,{logo_base64}" width="40"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="logo-container-login" style="color:black; font-weight:bold;">LOGO</div>', unsafe_allow_html=True)
        
        # Title dengan Animasi Rainbow
        st.markdown('<div class="login-title">AMPERA MULTI AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Masuk untuk melanjutkan ke Generator Laporan Otomatis</div>', unsafe_allow_html=True)
        
        # Tombol Masuk
        if st.button("Masuk", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- HALAMAN UTAMA (DASHBOARD) ---
else:
    # SIDEBAR CUSTOM
    with st.sidebar:
        # Kartu Profil Sesuai Gambar
        logo_html = f'<img src="data:image/png;base64,{logo_base64}">' if logo_base64 else '<span style="color:white;font-weight:bold;">A</span>'
        
        st.markdown(f"""
            <div class="sidebar-profile-card">
                <div class="avatar-glow">
                    {logo_html}
                </div>
                <div class="profile-info">
                    <div class="profile-name-sidebar">Ampera Multi AI</div>
                    <div class="badge-v2">v2.0</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigasi
        st.button("🏠 Home Dashboard", use_container_width=True)
        st.button("⚔️ Arena Battle", use_container_width=True)
        
        st.markdown('<div style="margin-top:30px; color:#64748b; font-size:0.75rem; padding-left:10px; letter-spacing:1px;">HISTORY</div>', unsafe_allow_html=True)
        st.button("⚡ Python Binary Search", use_container_width=True)

    # KONTEN DASHBOARD
    st.markdown("<h1 style='text-align: center; margin-top: 2rem; font-family: Cinzel;'>What would you like to do?</h1>", unsafe_allow_html=True)
    
    # Grid Shortcut
    c1, c2, c3 = st.columns(3)
    with c1: st.button("🌐 Landing Page", use_container_width=True)
    with c2: st.button("📊 Dashboard", use_container_width=True)
    with c3: st.button("🎮 Make a Game", use_container_width=True)
    
    # Chat Input menyatu dengan background (Area Hitam Dihilangkan)
    st.chat_input("Ask anything... (Tekan Enter untuk mengirim)")
