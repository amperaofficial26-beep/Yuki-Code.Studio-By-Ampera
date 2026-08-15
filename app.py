import streamlit as st
from openai import OpenAI

# Konfigurasi Halaman
st.set_page_config(page_title="Yuki Coding Studio", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling CSS agar mirip Dashboard Modern (Clean & Minimalist)
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
# HALAMAN 1: HOME DASHBOARD (Seperti di Gambar Referensi)
# -------------------------------------------------------------
if selected_menu == "🏠 Home Dashboard":
    st.markdown("<h1 style='text-align: center; color: #111827; margin-top: 2rem;'>What would you like to do?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280; margin-bottom: 2rem;'>Pilih jalur cepat di bawah atau tulis perintah kodingmu, Senpai! (o^▽^o)</p>", unsafe_allow_html=True)
    
    # Input Utama ala Dashboard
    home_prompt = st.text_area("Ask anything...", placeholder="Ketik ide aplikasi atau pertanyaan koding di sini...", height=120, label_visibility="collapsed")
    
    # Baris Tombol Fitur di Bawah Input
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1.5, 1, 1, 1, 1])
    with col_f1:
        st.button("📎 Add files", use_container_width=True)
    with col_f2:
        st.button("⚡ Mode", use_container_width=True)
    with col_f3:
        st.button("💻 Code", use_container_width=True)
    with col_f4:
        st.button("🌐 Web", use_container_width=True)
    with col_f5:
        if st.button("🚀 Kirim", use_container_width=True) and home_prompt:
            st.success(f"Perintah diterima: {home_prompt}")

    st.markdown("<br><h4 style='color: #374151; font-weight: 600;'>Get started</h4>", unsafe_allow_html=True)
    
    # Grid Kartu "Get Started" (6 Pilihan)
    gc1, gc2, gc3 = st.columns(3)
    
    with gc1:
        if st.button("🌐 **Create a landing page**\n\nCreate a sleek, modern landing page", use_container_width=True):
            st.info("Fitur Landing Page Builder dipilih!")
        if st.button("💻 **Design to Code**\n\nUpload an image and have AI build it", use_container_width=True):
            st.info("Fitur Design to Code dipilih!")
            
    with gc2:
        if st.button("📊 **Build a dashboard**\n\nTurn data into interactive charts", use_container_width=True):
            st.info("Fitur Dashboard Builder dipilih!")
        if st.button("📦 **Build a fullstack app**\n\nCreate a templated full-stack app", use_container_width=True):
            st.info("Fitur Fullstack App dipilih!")
            
    with gc3:
        if st.button("🎮 **Make a game**\n\nBuild a playable browser game", use_container_width=True):
            st.info("Fitur Game Maker dipilih!")
        if st.button("🏪 **Launch a storefront**\n\nCreate a beautiful online shop", use_container_width=True):
            st.info("Fitur Storefront dipilih!")

# -------------------------------------------------------------
# HALAMAN 2: ARENA BATTLE (Side-by-Side 2 AI)
# -------------------------------------------------------------
elif selected_menu == "⚔️ Arena Battle":
    st.title("⚔️ Yuki Coding Arena (Model Battle)")
    st.caption("Uji dan bandingkan performa Llama 3.3 (70B) vs Llama 3.1 (8B) secara head-to-head!")
    
    prompt_arena = st.text_area("Kirim pesan ke Arena Battle:", key="arena_prompt", placeholder="Contoh: Buatkan fungsi QuickSort di Python...")
    
    if st.button("⚔️ Mulai Battle", use_container_width=True) and prompt_arena:
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
                                {"role": "user", "content": prompt_arena}
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
                                {"role": "user", "content": prompt_arena}
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
