import streamlit as st
from openai import OpenAI

# Konfigurasi Halaman
st.set_page_config(page_title="Yuki Coding Studio - Aurora Arena", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling CSS Aurora UI & Pembersihan Total Background Bawah
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
    
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 8px;
        padding-left: 4px;
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
    
    /* Menghilangkan background dari seluruh div pembungkus di area stBottom */
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

# Inisialisasi Session State untuk navigasi
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Home Dashboard"

# -------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="sidebar-title">
            🏛️ Yuki Studio <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 400;">▼</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠  Home Dashboard", use_container_width=True):
        st.session_state["current_page"] = "🏠 Home Dashboard"
        st.rerun()
        
    if st.button("⚔️  Arena Battle", use_container_width=True):
        st.session_state["current_page"] = "⚔️ Arena Battle"
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
    st.markdown("<h1 style='text-align: center; color: #f8fafc; margin-top: 1rem;'>What would you like to do?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Ketik pesan di bawah dan cukup tekan <b>Enter</b> untuk mengirim, Senpai! (o^▽^o)</p>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='color: #e2e8f0; font-weight: 600;'>Get started</h4>", unsafe_allow_html=True)
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
    home_input = st.chat_input("Ask anything... (Tekan Enter untuk mengirim)")
    query_to_process = home_input if home_input else default_val
    
    if query_to_process:
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
        else:
            with st.spinner("🌸 Yuki sedang merespons perintah Senpai..."):
                try:
                    res_home = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Kamu adalah asisten pemrograman ahli yang ramah dan ceria ala anime."},
                            {"role": "user", "content": query_to_process}
                        ]
                    )
                    st.success("Berhasil! (≧◡≦) ✨")
                    st.markdown(res_home.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

# -------------------------------------------------------------
# HALAMAN 2: ARENA BATTLE
# -------------------------------------------------------------
elif selected_menu == "⚔️ Arena Battle":
    st.title("⚔️ Yuki Coding Arena (Model Battle)")
    st.caption("Ketik perintah koding di bawah dan tekan **Enter** untuk menguji Llama 3.3 (70B) vs Llama 3.1 (8B) secara head-to-head!")
    
    arena_input = st.chat_input("Kirim pesan ke Arena Battle...")
    
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
                
                with st.spinner("Generating..."):
                    try:
                        resp_a = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "Kamu adalah asisten pemrograman ahli. Berikan kode bersih dan penjelasan mendalam."},
                                {"role": "user", "content": prompt_val}
                            ]
                        )
                        st.markdown(resp_a.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col_b:
                st.markdown("""
                    <div class="arena-card">
                        <div class="arena-header">
                            <span>⚫ llama-3.1-8b-instant</span>
                            <span>🗖</span>
                        </div>
                """, unsafe_allow_html=True)
                
                with st.spinner("Generating..."):
                    try:
                        resp_b = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "Kamu adalah asisten pemrograman cepat dan akurat. Berikan solusi ringkas."},
                                {"role": "user", "content": prompt_val}
                            ]
                        )
                        st.markdown(resp_b.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("💡 **Arena Voting:** Mana model yang memberikan hasil koding lebih baik?")
            v1, v2, v3 = st.columns(3)
            with v1:
                if st.button("👈 Model A Unggul"): st.success("Suara tercatat untuk Model A!")
            with v2:
                if st.button("🤝 Seri"): st.success("Hasil seri dicatat!")
            with v3:
                if st.button("👉 Model B Unggul"): st.success("Suara tercatat untuk Model B!")

# -------------------------------------------------------------
# HALAMAN 3: LEADERBOARD
# -------------------------------------------------------------
elif selected_menu == "📊 Leaderboard":
    st.title("📊 Arena Leaderboard")
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
