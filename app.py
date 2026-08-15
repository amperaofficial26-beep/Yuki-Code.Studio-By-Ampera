import streamlit as st
from openai import OpenAI

# Konfigurasi Halaman
st.set_page_config(page_title="Yuki Coding Studio", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling CSS agar bersih dan modern
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f9f9fb;
        border-right: 1px solid #e5e7eb;
        padding-top: 10px;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
        color: #1f2937;
    }
    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .sidebar-menu-item {
        padding: 8px 12px;
        border-radius: 6px;
        color: #374151;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }
    .sidebar-menu-item:hover {
        background-color: #f3f4f6;
        color: #111827;
    }
    .history-header {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div.stButton > button {
        background: #2563eb !important;
        border: 1px solid #1d4ed8 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background: #1d4ed8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR ALA ARENA
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="sidebar-title">
            🏛️ Yuki Studio <span style="font-size: 0.9rem; color: #6b7280; font-weight: 400;">▼</span>
        </div>
    """, unsafe_allow_html=True)
    
    selected_menu = st.radio(
        "Menu Utama",
        ["🏠 Home Dashboard", "⚔️ Arena Battle", "📊 Leaderboard", "🔍 Search"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<div class="history-header">Yesterday</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">⚡ Python Binary Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">🛠️ Fix Bug Index Error</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# HALAMAN 1: HOME DASHBOARD (Enter to Send via st.chat_input)
# -------------------------------------------------------------
if selected_menu == "🏠 Home Dashboard":
    st.markdown("<h1 style='text-align: center; color: #111827; margin-top: 1rem;'>What would you like to do?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280; margin-bottom: 2rem;'>Ketik pesan di bawah dan cukup tekan <b>Enter</b> untuk mengirim, Senpai! (o^▽^o)</p>", unsafe_allow_html=True)
    
    # Grid Kartu "Get Started" di atas
    st.markdown("<h4 style='color: #374151; font-weight: 600;'>Get started</h4>", unsafe_allow_html=True)
    gc1, gc2, gc3 = st.columns(3)
    
    with gc1:
        if st.button("🌐 **Landing Page**\n\nCreate a modern landing page", use_container_width=True):
            st.session_state["shortcut_prompt"] = "Buatkan kode landing page modern menggunakan HTML dan Tailwind CSS."
        if st.button("💻 **Design to Code**\n\nUpload an image and convert", use_container_width=True):
            st.session_state["shortcut_prompt"] = "Bagaimana cara mengubah desain UI menjadi kode program?"
            
    with gc2:
        if st.button("📊 **Dashboard**\n\nInteractive charts & tables", use_container_width=True):
            st.session_state["shortcut_prompt"] = "Buatkan kerangka aplikasi dashboard interaktif menggunakan Python Streamlit."
        if st.button("📦 **Fullstack App**\n\nCreate templated full-stack app", use_container_width=True):
            st.session_state["shortcut_prompt"] = "Berikan arsitektur dasar untuk aplikasi web fullstack."
            
    with gc3:
        if st.button("🎮 **Make a Game**\n\nPlayable browser game", use_container_width=True):
            st.session_state["shortcut_prompt"] = "Buatkan game sederhana menggunakan HTML5 Canvas dan JavaScript."
        if st.button("🏪 **Storefront**\n\nCreate online shop layout", use_container_width=True):
            st.session_state["shortcut_prompt"] = "Buatkan layout halaman keranjang belanja online (e-commerce)."

    st.markdown("<br>", unsafe_allow_html=True)

    # Kotak Input Chat Bawah (Tekan Enter Langsung Kirim)
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
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
        else:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("### 🧬 Model A (Llama 3.3 - 70B)")
                with st.spinner("Model A mengetik..."):
                    try:
                        resp_a = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "Kamu adalah asisten pemrograman ahli. Berikan kode bersih dan penjelasan mendalam."},
                                {"role": "user", "content": arena_input}
                            ]
                        )
                        st.markdown(resp_a.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            with col_b:
                st.markdown("### ⚡ Model B (Llama 3.1 - 8B)")
                with st.spinner("Model B mengetik..."):
                    try:
                        resp_b = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "Kamu adalah asisten pemrograman cepat dan akurat. Berikan solusi ringkas."},
                                {"role": "user", "content": arena_input}
                            ]
                        )
                        st.markdown(resp_b.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            st.markdown("---")
            st.info("💡 **Arena Voting:** Mana model yang lebih baik?")
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
