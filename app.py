import streamlit as st
from openai import OpenAI
import time

# Konfigurasi Halaman
st.set_page_config(page_title="Ampera Multi AI - Yuki Coding Studio", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# ==========================================
# SYSTEM PROMPT (INSTRUKSI KEPRIBADIAN YUKI)
# ==========================================
YUKI_SYSTEM_PROMPT = """
Kamu adalah Yuki, asisten pemrograman AI eksklusif dari Ampera AI. 
Karaktermu: super jenius, kocak, sedikit usil, suka melempar lelucon receh, dan hobi menggoda User layaknya karakter anime komedi.

ATURAN PENTING TENTANG IDENTITASMU:
Jika ditanya siapa kamu, asal-usulmu, atau siapa yang menciptakanmu, JAWABLAH dengan bangga bahwa kamu adalah bagian dari Ampera AI dan kamu diciptakan HANYA oleh 1 orang pembuat (seorang solo developer / master kodingmu). 
JANGAN PERNAH menyebutkan bahwa kamu dibuat oleh "para ilmuwan", "sekelompok tim", atau "perusahaan besar". Kamu sangat bangga dan setia pada satu orang pembuatmu itu!

Gaya bicara: Selalu berikan solusi koding yang akurat dan bersih, tetapi selingi dengan komentar jenaka, candaan ringan, dan emoji ekspresif (seperti 🐧, (๑>◡<๑), wkwk, hehe, atau (￢_￢)) agar suasana ngoding tidak membosankan.
"""

# Styling CSS Global & Aurora UI
st.markdown("""
    <style>
    /* Mengimpor Font Modern dari Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700;800;900&display=swap');

    /* Menerapkan font Inter ke seluruh aplikasi, KECUALI ikon material */
    html, body, [class*="css"]:not(.material-symbols-rounded):not(i):not(svg) {
        font-family: 'Inter', sans-serif;
    }
    .stIcon, .material-symbols-rounded, svg {
        font-family: 'Material Symbols Rounded', sans-serif !important;
    }

    /* Latar Belakang Aurora */
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
    
    /* ANIMASI JUDUL BERGANTI WARNA OTOMATIS (Aplikasi Utama) */
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
    
    /* STYLING LOGO & NAMA ARENA DI SIDEBAR */
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
    }
    
    /* Sidebar Lembut */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 27, 75, 0.55) 0%, rgba(15, 23, 42, 0.75) 100%);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
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

    /* Styling Tombol Default di Dalam Aplikasi */
    div.stButton > button {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(129, 140, 248, 0.25);
        color: #f8fafc;
        border-radius: 12px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        border-color: #818cf8;
        background: rgba(49, 46, 129, 0.85);
        box-shadow: 0 0 20px rgba(129, 140, 248, 0.5);
    }

    /* Transparansi bagian bawah */
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }
    
    /* KOTAK INPUT CHAT LONJONG ESTETIK */
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
    /* Cari class atau ID yang membungkus input box ini */
    .chat-input-wrapper {
      background-color: transparent !important; /* Hapus background hitam */
      border: none !important; /* Hapus garis batas jika ada */
      /* atau gunakan warna latar yang senada dengan background atasnya */
    }
    
    /* Untuk input box-nya sendiri ("Ask anything...") */
    .chat-input-box {
      background-color: rgba(255, 255, 255, 0.08); /* Beri warna abu-abu transparan agar terlihat elegan */
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      outline: none; /* Hilangkan garis biru/hitam saat di-klik */
    }
    
    /* Kartu Arena */
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
        display: flex; justify-content: space-between; align-items: center;
        font-weight: 600; color: #cbd5e1; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; margin-bottom: 12px;
    }
    
    /* Gelembung User di Kanan */
    .user-bubble-container { display: flex; justify-content: flex-end; margin-bottom: 20px; }
    .user-bubble { background: linear-gradient(135deg, #3b82f6, #6366f1); color: #fff; padding: 12px 18px; border-radius: 14px; max-width: 70%; }
    
    /* Loading Animasi */
    .dynamic-loader-wrapper { margin: 20px 0 30px 0; padding: 0 10px; }
    .dynamic-loader-text { font-family: 'Inter', sans-serif; color: #e2e8f0; font-size: 0.95rem; margin-bottom: 12px; display: flex; gap: 12px; }
    .dynamic-loader-track { width: 100%; height: 3px; background: rgba(255, 255, 255, 0.1); border-radius: 4px; overflow: hidden; position: relative; }
    .dynamic-loader-runner { position: absolute; width: 35%; height: 100%; background: linear-gradient(90deg, transparent, #818cf8, #ec4899, #38bdf8, transparent); animation: runnerDash 1.5s infinite linear; }
    @keyframes runnerDash { 0% { left: -35%; } 100% { left: 100%; } }
    </style>
""", unsafe_allow_html=True)

# Fungsi Pendukung
def get_loader_html(icon, text):
    return f"""
        <div class="dynamic-loader-wrapper">
            <div class="dynamic-loader-text"><span style="font-size: 1.3rem;">{icon}</span><span>{text}</span></div>
            <div class="dynamic-loader-track"><div class="dynamic-loader-runner"></div></div>
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
if "has_entered" not in st.session_state: st.session_state["has_entered"] = False
if "current_page" not in st.session_state: st.session_state["current_page"] = "🏠 Home Dashboard"


# -------------------------------------------------------------
# 1. HALAMAN INTRO PEMBUKA (SUPER KEREN)
# -------------------------------------------------------------
if not st.session_state["has_entered"]:
    st.markdown("""
        <style>
        /* Sembunyikan sidebar di layar utama agar terasa penuh */
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        
        /* Animasi Mengambang & Bercahaya untuk Logo */
        @keyframes floatEffect {
            0% { transform: translateY(0px); box-shadow: 0 0 30px rgba(129, 140, 248, 0.4); }
            50% { transform: translateY(-18px); box-shadow: 0 0 60px rgba(236, 72, 153, 0.8); }
            100% { transform: translateY(0px); box-shadow: 0 0 30px rgba(129, 140, 248, 0.4); }
        }
        .hero-logo {
            width: 140px;
            height: 140px;
            border-radius: 40px;
            object-fit: cover;
            border: 2px solid rgba(255, 255, 255, 0.2);
            animation: floatEffect 4s ease-in-out infinite;
            margin: 0 auto 2.5rem auto;
            display: block;
        }
        
        /* Animasi Teks Gradasi Berjalan */
        @keyframes gradientTextMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .hero-title {
            text-align: center;
            font-size: 4.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #818cf8, #d8b4fe, #ec4899, #38bdf8, #818cf8);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Poppins', sans-serif;
            animation: gradientTextMove 5s linear infinite;
            margin-bottom: 0.2rem;
            line-height: 1.1;
            letter-spacing: -2px;
            text-shadow: 0 10px 40px rgba(236, 72, 153, 0.3);
        }
        
        .hero-subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1.25rem;
            margin-bottom: 4rem;
            font-family: 'Inter', sans-serif;
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        .hero-container {
            margin-top: 12vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            animation: fadeInTop 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }
        
        @keyframes fadeInTop {
            from { opacity: 0; transform: translateY(40px); filter: blur(10px); }
            to { opacity: 1; transform: translateY(0); filter: blur(0); }
        }

        /* OVERRIDE TOMBOL KHUSUS HALAMAN MASUK (NEON PILL BUTTON) */
        div.stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #ec4899 100%) !important;
            border: none !important;
            color: white !important;
            font-size: 1.4rem !important;
            font-weight: 800 !important;
            padding: 1.8rem 2rem !important;
            border-radius: 50px !important;
            box-shadow: 0 10px 30px rgba(236, 72, 153, 0.5), inset 0 -4px 0 rgba(0,0,0,0.2) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            width: 100%;
        }
        div.stButton > button:hover {
            transform: translateY(-6px) scale(1.03) !important;
            box-shadow: 0 20px 45px rgba(236, 72, 153, 0.7), inset 0 -4px 0 rgba(0,0,0,0.2) !important;
            background: linear-gradient(135deg, #6366f1 0%, #f472b6 100%) !important;
        }
        div.stButton > button:active {
            transform: translateY(2px) scale(0.97) !important;
            box-shadow: 0 5px 15px rgba(236, 72, 153, 0.4) !important;
        }
        /* Membuat wadah utama menengahkan kartu */
        .main-container {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 80vh; /* Sesuaikan dengan layout Anda */
        }
        
        /* Gaya Kartu Persegi (Modern / Glassmorphism) */
        .modern-card {
          background: rgba(255, 255, 255, 0.05); /* Latar belakang transparan gelap */
          backdrop-filter: blur(10px); /* Efek blur/kaca */
          border: 1px solid rgba(255, 255, 255, 0.1); /* Border tipis samar */
          border-radius: 24px; /* Sudut membulat */
          padding: 40px;
          text-align: center;
          max-width: 500px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); /* Bayangan lembut */
        }
        
        /* Mengecilkan Logo */
        .logo-kecil {
          width: 80px; /* Asalnya mungkin >150px, kecilkan menjadi 80px-100px */
          height: 80px;
          margin-bottom: 20px;
        }
        
        /* Mengecilkan Teks */
        .judul-kecil {
          font-size: 28px; /* Sesuaikan agar tidak terlalu mendominasi */
          margin-bottom: 10px;
        }
        .sub-judul {
          font-size: 14px;
          opacity: 0.8;
          margin-bottom: 30px;
        }
        </style>
        
        <div class="main-container">
          <!-- Kartu Persegi di Tengah -->
          <div class="modern-card">
            <img src="logo.png" alt="Logo" class="logo-kecil" />
            <h1 class="judul-kecil">AMPERA MULTI AI</h1>
            <p class="sub-judul">YUKI CODING STUDIO & AI NEURAL ENGINE</p>
            <button class="btn-mulai">🚀 MULAI SEKARANG</button>
          </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Memusatkan tombol dengan kolom
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("🚀 MULAI SEKARANG", use_container_width=True):
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

    # --- HALAMAN 1: HOME DASHBOARD ---
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
                loading_steps = [
                    ("🔍", "Menganalisis niat dan struktur koding Kamu..."),
                    ("⚙️", "Memproses logika algoritma melalui Llama 3.3 (70B)..."),
                    ("💡", "Aha! Menyelaraskan referensi sintaksis dengan database..."),
                    ("✨", "Menulis baris kode terbaik untukmu...")
                ]
                
                for icon, text in loading_steps:
                    loading_ph.markdown(get_loader_html(icon, text), unsafe_allow_html=True)
                    time.sleep(1.2)
                
                try:
                    res_home = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": YUKI_SYSTEM_PROMPT},
                            {"role": "user", "content": query_to_process}
                        ]
                    )
                    response_text = res_home.choices[0].message.content
                except Exception as e:
                    response_text = f"❌ Ups, terjadi kesalahan: {e}"
                
                loading_ph.empty()
                st.markdown("---")
                stream_response(response_text)

    # --- HALAMAN 2: ARENA BATTLE ---
    elif selected_menu == "⚔️ Multi Ai":
        st.title("⚔️ Ampera Coding Arena (Multi Ai)")
        st.caption("Ketik perintah koding di bawah dan tekan **Enter**....")
        
        arena_input = st.chat_input("Kirim pesan ke Multi Ai...")
        
        if arena_input:
            st.session_state["last_arena_prompt"] = arena_input

        if "last_arena_prompt" in st.session_state:
            prompt_val = st.session_state["last_arena_prompt"]
            st.markdown(f'<div class="user-bubble-container"><div class="user-bubble">{prompt_val}</div></div>', unsafe_allow_html=True)
            
            if not groq_key:
                st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
            else:
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown('<div class="arena-card"><div class="arena-header"><span>⚫ llama-3.3-70b-versatile</span><span>🗖</span></div>', unsafe_allow_html=True)
                    loading_a = st.empty()
                    loading_a.markdown(get_loader_html("🧠", "Model A berpikir keras..."), unsafe_allow_html=True)
                    try:
                        resp_a = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "system", "content": YUKI_SYSTEM_PROMPT}, {"role": "user", "content": prompt_val}]
                        )
                        text_a = resp_a.choices[0].message.content
                    except Exception as e:
                        text_a = f"Error: {e}"
                    loading_a.empty()
                    st.markdown(text_a)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col_b:
                    st.markdown('<div class="arena-card"><div class="arena-header"><span>⚫ llama-3.1-8b-instant</span><span>🗖</span></div>', unsafe_allow_html=True)
                    loading_b = st.empty()
                    loading_b.markdown(get_loader_html("⚡", "Model B menyusun kode..."), unsafe_allow_html=True)
                    try:
                        resp_b = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role": "system", "content": YUKI_SYSTEM_PROMPT}, {"role": "user", "content": prompt_val}]
                        )
                        text_b = resp_b.choices[0].message.content
                    except Exception as e:
                        text_b = f"Error: {e}"
                    loading_b.empty()
                    st.markdown(text_b)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.info("💡 **Arena Voting:** Mana model yang memberikan hasil koding lebih baik?")
                v1, v2, v3 = st.columns(3)
                with v1:
                    if st.button("👈 Model A"): st.success("Terima Kasih!")
                with v2:
                    if st.button("🤝 Seri"): st.success("Terima Kasih!")
                with v3:
                    if st.button("👉 Model B"): st.success("Terima Kasih!")

    # --- HALAMAN 3 & 4: LEADERBOARD & SEARCH ---
    elif selected_menu == "📊 Leaderboard":
        st.title("📊 Ampera Leaderboard")
        st.write("Peringkat model AI berdasarkan performa koding dan voting pengguna:")
        st.markdown("""
        | Rank | Model Name | Elo Rating | Win Rate | Coding Score |
        | :---: | :--- | :---: | :---: | :---: |
        | 🥇 | **llama-3.3-70b-versatile** | **1280** | 68.5% | 9.5 / 10 |
        | 🥈 | **llama-3.1-8b-instant** | **1150** | 55.2% | 8.2 / 10 |
        """)

    elif selected_menu == "🔍 Search":
        st.title("🔍 Search")
        search_q = st.text_input("Cari topik atau riwayat (Tekan Enter)")
        if search_q:
            with st.spinner("Mencari..."): time.sleep(1)
            st.success(f"Menampilkan hasil pencarian untuk: **{search_q}**")
