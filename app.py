import streamlit as st
from openai import OpenAI
import time

# Konfigurasi Halaman
st.set_page_config(page_title="Yuki Coding Studio - Aurora Arena", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling CSS Aurora UI, Efek Ganti Warna, & Animasi Intro Pembuka
st.markdown("""
    <style>
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
    
    /* ANIMASI INTRO PEMBUKA (SPLASH SCREEN) */
    @keyframes splashIntro {
        0% {
            opacity: 0;
            transform: scale(0.92);
            filter: blur(12px);
        }
        50% {
            opacity: 1;
            transform: scale(1.02);
            filter: blur(2px);
        }
        100% {
            opacity: 1;
            transform: scale(1);
            filter: blur(0px);
        }
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
        font-weight: 900;
        background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.15em;
        font-family: monospace;
        margin-bottom: 0.5rem;
    }
    .splash-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* ANIMASI JUDUL BERGANTI WARNA OTOMATIS */
    @keyframes colorShift {
        0% { color: #818cf8; }
        33% { color: #ec4899; }
        66% { color: #38bdf8; }
        100% { color: #818cf8; }
    }
    h1, h2, h3 {
        animation: colorShift 6s ease infinite !important;
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
    }
    .logo-text {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.08em;
        font-family: monospace;
    }
    
    /* Sidebar Lembut & Tidak Kaku (Aurora Glassmorphism) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 27, 75, 0.55) 0%, rgba(15, 23, 42, 0.75) 100%);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 10px;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    .sidebar-section-header {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94a3b8;
        margin-top: 1.8rem;
        margin-bottom: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding-left: 4px;
    }

    /* Tombol Timbul & Bersinar (Aurora Glow Button) */
    div.stButton > button {
        background: rgba(30, 41, 59, 0.65) !important;
        border: 1px solid rgba(129, 140, 248, 0.25) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        border-color: #818cf8 !important;
        color: #ffffff !important;
        background: rgba(49, 46, 129, 0.85) !important;
        box-shadow: 0 0 20px rgba(129, 140, 248, 0.5), 0 0 35px rgba(99, 102, 241, 0.3) !important;
    }

    /* MEMAKSA SEMUA PEMBUNGKUS BAWAH MENJADI TRANSPARAN TOTAL */
    [data-testid="stBottom"], 
    [data-testid="stBottomBlockContainer"], 
    [data-testid="stChatInputContainer"] {
        background: transparent !important;
        background-color: transparent !important;
        border-top: none !important;
        box-shadow: none !important;
    }
    [data-testid="stBottom"] div {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* KOTAK INPUT CHAT LONJONG ESTETIK */
    [data-testid="stChatInput"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(129, 140, 248, 0.3) !important;
        border-radius: 9999px !important;
        padding: 4px 12px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 25px rgba(129, 140, 248, 0.5), inset 0 0 10px rgba(129, 140, 248, 0.2) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
    }
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #4f46e5, #3b82f6) !important;
        border: none !important;
        border-radius: 50% !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4) !important;
    }
    [data-testid="stChatInput"] button:hover {
        transform: scale(1.08);
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.8) !important;
    }

    /* Styling Kartu Arena */
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
        font-family: monospace;
        font-size: 0.95rem;
        font-weight: 600;
        color: #cbd5e1;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 10px;
        margin-bottom: 12px;
    }
    
    /* Gelembung User di Kanan */
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
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk efek teks muncul perlahan (Typewriter Effect)
def stream_response(text):
    placeholder = st.empty()
    streamed = ""
    for word in text.split(" "):
        streamed += word + " "
        placeholder.markdown(streamed)
        time.sleep(0.015)

# Inisialisasi Session State untuk Intro & Navigasi
if "has_entered" not in st.session_state:
    st.session_state["has_entered"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Home Dashboard"

# -------------------------------------------------------------
# 1. HALAMAN INTRO PEMBUKA (SPLASH SCREEN DENGAN ANIMASI MASUK)
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
            st.rerun()  # Diperbaiki dari st.reruns() = st.rerun()
            
# -------------------------------------------------------------
# 2. APLIKASI UTAMA SETELAH MASUK
# -------------------------------------------------------------
else:
    # -------------------------------------------------------------
    # SIDEBAR
    # -------------------------------------------------------------
    with st.sidebar:
        st.markdown("""
            <div class="logo-container">
                <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&h=120&fit=crop" class="logo-img" alt="Logo Arena">
                <div class="logo-text">ARENA</div>
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
                with st.status("🧠 Yuki lagi nyari contekan dulu buat Kamu...", expanded=True) as status:
                    st.write("🔍 Menganalisis niat dan struktur koding Kamu...")
                    time.sleep(1.8)
                    st.write("⚙️ Memproses logika algoritma melalui Llama 3.3 (70B)...")
                    time.sleep(2.0)
                    st.write("💡 Aha! Ketemu celahnya (atau malah nambah bug baru, hehe)...")
                    time.sleep(2.0)
                    st.write("✨ Persiapan akhir selesai.")
                    time.sleep(1.2)
                    
                    try:
                        res_home = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {
                                    "role": "system", 
                                    "content": (
                                        "Kamu adalah Yuki, asisten pemrograman AI yang super jenius tapi juga kocak, "
                                        "sedikit usil, suka melempar lelucon receh, dan hobi menggoda User layaknya "
                                        "karakter anime komedi. Tetap berikan solusi koding yang akurat dan bersih, "
                                        "tetapi selingi dengan komentar jenaka, candaan ringan, dan emoji ekspresif "
                                        "(seperti 🐧, (๑>◡<๑), wkwk, atau (￢_￢)) agar suasana ngoding tidak membosankan!"
                                    )
                                },
                                {"role": "user", "content": query_to_process}
                            ]
                        )
                        status.update(label="✨ Proses berpikir selesai!", state="complete", expanded=False)
                        response_text = res_home.choices[0].message.content
                    except Exception as e:
                        status.update(label="❌ Terjadi kesalahan saat memproses.", state="error", expanded=True)
                        response_text = f"Error: {e}"
                
                st.markdown("---")
                stream_response(response_text)

    # -------------------------------------------------------------
    # HALAMAN 2: ARENA BATTLE
    # -------------------------------------------------------------
    elif selected_menu == "⚔️ Multi Ai":
        st.title("⚔️ Yuki Coding Arena (Multi Ai)")
        st.caption("Ketik perintah koding di bawah dan tekan **Enter**....")
        
        arena_input = st.chat_input("Kirim pesan ke Multi Ai...")
        
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
            else:
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("""
                        <div class="arena-card">
                            <div class="arena-header">
                                <span>⚫ llama-3.3-70b-versatile</span>
                                <span>🗖</span>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    with st.status("🧠 Model A Thinking...", expanded=True) as status_a:
                        st.write("Analisis mendalam model A...")
                        time.sleep(3.0)
                        try:
                            resp_a = client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=[
                                    {"role": "system", "content": "Kamu adalah asisten pemrograman ahli. Berikan kode bersih dan penjelasan mendalam."},
                                    {"role": "user", "content": prompt_val}
                                ]
                            )
                            status_a.update(label="Model A Ready", state="complete", expanded=False)
                            text_a = resp_a.choices[0].message.content
                        except Exception as e:
                            status_a.update(label="Error", state="error", expanded=True)
                            text_a = f"Error: {e}"
                    
                    st.markdown("---")
                    st.markdown(text_a)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col_b:
                    st.markdown("""
                        <div class="arena-card">
                            <div class="arena-header">
                                <span>⚫ llama-3.1-8b-instant</span>
                                <span>🗖</span>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    with st.status("⚡ Model B Thinking...", expanded=True) as status_b:
                        st.write("Analisis kilat model B...")
                        time.sleep(2.0)
                        try:
                            resp_b = client.chat.completions.create(
                                model="llama-3.1-8b-instant",
                                messages=[
                                    {"role": "system", "content": "Kamu adalah asisten pemrograman cepat dan akurat. Berikan solusi Yang detail."},
                                    {"role": "user", "content": prompt_val}
                                ]
                            )
                            status_b.update(label="Model B Ready", state="complete", expanded=False)
                            text_b = resp_b.choices[0].message.content
                        except Exception as e:
                            status_b.update(label="Error", state="error", expanded=True)
                            text_b = f"Error: {e}"
                    
                    st.markdown("---")
                    st.markdown(text_b)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.info("💡 **Arena Voting:** Mana model yang memberikan hasil koding lebih baik?")
                v1, v2, v3 = st.columns(3)
                with v1:
                    if st.button("👈 Model A"): st.success("Terima Kasih Atas Penilaian Anda!")
                with v2:
                    if st.button("🤝 Seri"): st.success("Terima Kasih Atas Penilaian Anda!!")
                with v3:
                    if st.button("👉 Model"): st.success("Terima Kasih Atas Penilaian Anda!")

    # -------------------------------------------------------------
    # HALAMAN 3: LEADERBOARD
    # -------------------------------------------------------------
    elif selected_menu == "📊 Leaderboard":
        st.title("📊 Ampera Leaderboard")
        st.write("Peringkat model AI berdasarkan performa koding dan voting pengguna:")
        st.markdown("""
        | Rank | Model Name | Elo Rating | Win Rate | Coding Score |
        | :---: | :--- | :---: | :---: | :---: |
        | 🥇 | **llama-3.3-70b-versatile** | **1280** | 68.5% | 9.5 / 10 |
        | 🥈 | **llama-3.1-8b-instant** | **1150** | 55.2% | 8.2 / 10 |
        """)

    # -------------------------------------------------------------
    # HALAMAN 4: SEARCH
    # -------------------------------------------------------------
    elif selected_menu == "🔍 Search":
        st.title("🔍 Search Chat History")
        search_query = st.text_input("Cari riwayat percakapan atau kode sebelumnya...")
        if search_query:
            st.info(f"Hasil pencarian untuk: **{search_query}**")
            st.markdown("- ⚡ *Python Binary Search* (Ditemukan di riwayat Yesterday)")
