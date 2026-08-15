import streamlit as st
from openai import OpenAI

# Konfigurasi Halaman (Sidebar default terbuka)
st.set_page_config(page_title="Yuki Arena Coding Studio", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Styling CSS untuk Sidebar & Tema Arena Clean
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
        text-decoration: none;
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
# SIDEBAR ALA CHATBOT ARENA
# -------------------------------------------------------------
with st.sidebar:
    # Header Logo & Nama Arena
    st.markdown("""
        <div class="sidebar-title">
            🏛️ Arena <span style="font-size: 0.9rem; color: #6b7280; font-weight: 400;">▼</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu Navigasi Samping
    selected_menu = st.radio(
        "Menu Utama",
        ["💬 New Chat", "📊 Leaderboard", "🔍 Search"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Bagian Riwayat Chat (History)
    st.markdown('<div class="history-header">Yesterday</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">⚡ Python Binary Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">🛠️ Fix Bug Index Error</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="history-header">Previous 7 Days</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">🚀 Flask Rest API Boilerplate</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-menu-item">💡 Sorting Algorithm Battle</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# KONTEN UTAMA SESUAI MENU SIDEBAR
# -------------------------------------------------------------
if selected_menu == "💬 New Chat":
    col_top1, col_top2 = st.columns([4, 1])
    with col_top1:
        st.title("⚔️ Yuki Coding Arena (Model Battle)")
    with col_top2:
        battle_mode = st.selectbox("Mode", ["⚔️ Battle Mode", "🤖 Single Model"], label_visibility="collapsed")
    
    st.caption("Uji dan bandingkan performa dua model AI pemrograman secara head-to-head (Llama 3.3 70B vs Llama 3.1 8B). (o^▽^o)")
    
    prompt_arena = st.text_area("Kirim pesan ke Arena:", key="arena_prompt", placeholder="Contoh: Buatkan fungsi QuickSort di Python...")
    
    if st.button("🚀 Kirim", use_container_width=True) and prompt_arena:
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
                                {"role": "system", "content": "Kamu adalah asisten pemrograman ahli. Berikan kode yang bersih dan penjelasan mendalam."},
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

elif selected_menu == "📊 Leaderboard":
    st.title("📊 Arena Leaderboard")
    st.write("Peringkat model AI berdasarkan performa koding dan voting terbanyak dari pengguna:")
    
    # Tabel Leaderboard Sederhana
    st.markdown("""
    | Rank | Model Name | Elo Rating | Win Rate | Coding Score |
    | :---: | :--- | :---: | :---: | :---: |
    | 🥇 | **llama-3.3-70b-versatile** | **1280** | 68.5% | 9.5 / 10 |
    | 🥈 | **llama-3.1-8b-instant** | **1150** | 55.2% | 8.2 / 10 |
    | 🥉 | **mixtral-8x7b-32768** | **1110** | 51.0% | 8.0 / 10 |
    """)

elif selected_menu == "🔍 Search":
    st.title("🔍 Search Chat History")
    search_query = st.text_input("Cari riwayat percakapan atau kode sebelumnya:", placeholder="Ketik kata kunci...")
    if search_query:
        st.info(f"Menampilkan hasil pencarian untuk: **{search_query}**")
        st.markdown("- ⚡ *Python Binary Search* (Ditemukan di riwayat Yesterday)")
        st.markdown("- 🛠️ *Fix Bug Index Error* (Ditemukan di riwayat Yesterday)")
