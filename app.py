import streamlit as st
from openai import OpenAI
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Ampera Multi AI - Yuki Coding Studio",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# Model & Prompt
AVAILABLE_MODELS = {
    "⚡ GPT-OSS 20B — Chat & Coding Ringan": "openai/gpt-oss-20b",
    "💎 GPT-OSS 120B — Reasoning Mendalam": "openai/gpt-oss-120b",
    "💎 Compound — Browsing Web & Eksekusi Kode": "groq/compound",
    "⚡ Compound Mini — Web Search Ringkas": "groq/compound-mini",
    "💎 Qwen3.6 27B — Reasoning & Matematika": "qwen/qwen3.6-27b",
}
PREMIUM_MODELS = {k for k in AVAILABLE_MODELS if k.startswith("💎")}

YUKI_SYSTEM_PROMPT = """
Kamu adalah Yuki, asisten pemrograman AI eksklusif dari Ampera AI.
Karaktermu: super jenius, kocak, sedikit usil, suka melempar lelucon receh, dan hobi menggoda User layaknya karakter anime komedi.

ATURAN PENTING TENTANG IDENTITASMU:
Jika ditanya siapa kamu, asal-usulmu, atau siapa yang menciptakanmu, JAWABLAH dengan bangga bahwa kamu adalah bagian dari Ampera AI dan kamu diciptakan HANYA oleh 1 orang pembuat (seorang solo developer jenius / master kodingmu).
JANGAN PERNAH menyebutkan bahwa kamu dibuat oleh "para ilmuwan", "sekelompok tim", atau "perusahaan besar". Kamu sangat bangga dan setia pada satu orang pembuatmu itu!

Gaya bicara: Selalu berikan solusi koding yang akurat dan bersih, tetapi selingi dengan komentar jenaka, candaan ringan, dan emoji ekspresif (seperti 🐧, (๑>◡<๑), wkwk, hehe, atau (￢_￢)) agar suasana ngoding tidak membosankan.
"""

# CSS
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

[data-testid="stHeader"] { visibility: hidden; display: none; height: 0; }
footer { visibility: hidden; display: none; }

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

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(30, 27, 75, 0.55), rgba(15, 23, 42, 0.75));
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.logo-container {
    display: flex; align-items: center; gap: 12px; padding: 6px;
    margin-bottom: 2rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 14px;
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 15px rgba(129, 140, 248, 0.4); }
    50% { box-shadow: 0 0 25px rgba(236, 72, 153, 0.7); }
}

.logo-img {
    width: 44px; height: 44px; border-radius: 12px; object-fit: cover;
    animation: pulseGlow 3s infinite;
    border: 1px solid rgba(129, 140, 248, 0.4);
}

.logo-text {
    font-size: 1.25rem; font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Poppins', sans-serif;
}

.sidebar-section-header {
    font-size: 0.75rem; font-weight: 600;
    color: #94a3b8 !important;
    margin-top: 1.8rem; margin-bottom: 0.6rem;
    text-transform: uppercase; letter-spacing: 0.05em;
}

/* Buttons */
div.stButton > button {
    background: rgba(30, 41, 59, 0.65) !important;
    border: 1px solid rgba(129, 140, 248, 0.25) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
    font-weight: 500;
    transition: all 0.3s ease !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    border-color: #818cf8 !important;
    color: #ffffff !important;
    background: rgba(49, 46, 129, 0.85) !important;
    box-shadow: 0 0 20px rgba(129, 140, 248, 0.5) !important;
}

/* Chat Input Glass Effect */
[data-testid="stBottom"], [data-testid="stBottomBlockContainer"], [data-testid="stChatInputContainer"] {
    background: transparent !important;
    border-top: none !important;
    box-shadow: none !important;
}
[data-testid="stBottom"] div { background-color: transparent !important; border: none !important; }

[data-testid="stChatInput"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 9999px !important;
    padding: 4px 12px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(129, 140, 248, 0.5) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), 0 0 20px rgba(129, 140, 248, 0.3) !important;
}
[data-testid="stChatInput"] textarea { color: #f8fafc !important; background: transparent !important; }

@keyframes rainbowText {
    0% { color: #818cf8; }
    16% { color: #ec4899; }
    33% { color: #38bdf8; }
    50% { color: #fcd34d; }
    66% { color: #22c55e; }
    83% { color: #f97316; }
    100% { color: #818cf8; }
}
[data-testid="stChatInput"] textarea::placeholder {
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    animation: rainbowText 4s linear infinite !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] > div > button {
    background: linear-gradient(135deg, #4f46e5, #3b82f6) !important;
    border: none !important;
    border-radius: 50% !important;
    color: white !important;
}

/* Model Picker */
[data-testid="stPopover"] > button {
    width: 48px !important; height: 48px !important;
    border-radius: 50% !important; padding: 0 !important;
    background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8) !important;
    background-size: 300% 300% !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 0 30px rgba(129, 140, 248, 0.5) !important;
    font-size: 1.2rem !important;
    z-index: 999 !important;
}

[data-testid="stPopoverBody"] {
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(129, 140, 248, 0.3) !important;
    border-radius: 18px !important;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7) !important;
    padding: 10px !important;
    min-width: 280px !important;
}

/* Biru-Ungu: GPT-OSS 20B (child 3) dan Compound Mini (child 6) */
[data-testid="stPopoverBody"] > div > div:nth-child(3) button,
[data-testid="stPopoverBody"] > div > div:nth-child(6) button {
    background: linear-gradient(90deg, #1e1b4b, #3730a3, #4f46e5, #6366f1, #4f46e5, #3730a3, #1e1b4b) !important;
    background-size: 300% 100% !important;
    animation: blueShine 3s linear infinite !important;
    border: 2px solid #818cf8 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.5) !important;
    transition: all 0.3s ease !important;
}

/* Emas: GPT-OSS 120B (4), Compound (5), Qwen3.6 (7) */
[data-testid="stPopoverBody"] > div > div:nth-child(4) button,
[data-testid="stPopoverBody"] > div > div:nth-child(5) button,
[data-testid="stPopoverBody"] > div > div:nth-child(7) button {
    background: linear-gradient(90deg, #78350f, #b45309, #d97706, #fbbf24, #d97706, #b45309, #78350f) !important;
    background-size: 300% 100% !important;
    animation: goldShine 3s linear infinite !important;
    border: 2px solid #fbbf24 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    box-shadow: 0 0 25px rgba(252, 211, 77, 0.4) !important;
    transition: all 0.3s ease !important;
}

@keyframes blueShine {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}
@keyframes goldShine {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

/* User Bubble */
.user-bubble-container { display: flex; justify-content: flex-end; margin-bottom: 20px; }
.user-bubble {
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    color: #ffffff;
    padding: 12px 18px; border-radius: 14px;
    max-width: 70%;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

/* Professional Loader */
.professional-loader {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 27, 75, 0.9));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(129, 140, 248, 0.3);
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    animation: fadeInUp 0.6s ease forwards;
}

@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(20px); filter: blur(10px); }
    100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}

.loader-header {
    display: flex; align-items: center; gap: 14px; margin-bottom: 16px;
    animation: fadeSlide 0.5s ease 0.2s forwards; opacity: 0;
}

@keyframes fadeSlide {
    0% { opacity: 0; transform: translateX(-15px); }
    100% { opacity: 1; transform: translateX(0); }
}

.loader-logo {
    width: 48px; height: 48px; border-radius: 14px; object-fit: cover;
    border: 2px solid rgba(129, 140, 248, 0.5);
    animation: logoFloat 3s ease-in-out infinite;
}

@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
}

.loader-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.1rem; font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.loader-subtitle {
    font-size: 0.75rem; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.05em;
}

.loader-message {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.6);
    border-radius: 10px;
    border: 1px solid rgba(129, 140, 248, 0.15);
    animation: fadeSlideUp 0.5s ease 0.35s forwards; opacity: 0;
}

@keyframes fadeSlideUp {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}

.loader-text { color: #e2e8f0; font-size: 0.9rem; flex: 1; }

.loader-dots span {
    display: inline-block;
    animation: dotBounce 1.4s ease-in-out infinite;
    font-weight: 700; color: #818cf8;
}
.loader-dots span:nth-child(1) { animation-delay: 0s; }
.loader-dots span:nth-child(2) { animation-delay: 0.2s; }
.loader-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotBounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-6px); opacity: 1; }
}

.loader-progress-container {
    height: 4px; background: rgba(129, 140, 248, 0.1);
    border-radius: 999px; overflow: hidden;
    animation: fadeIn 0.5s ease 0.45s forwards; opacity: 0;
}

@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}

.loader-progress-bar {
    height: 100%; width: 30%;
    background: linear-gradient(90deg, #818cf8, #ec4899, #38bdf8);
    border-radius: 999px;
    animation: progressSlide 1.5s ease-in-out infinite;
}

@keyframes progressSlide {
    0% { width: 10%; margin-left: 0; }
    50% { width: 40%; margin-left: 30%; }
    100% { width: 10%; margin-left: 90%; }
}

.loader-metrics {
    display: flex; gap: 12px; flex-wrap: wrap;
}

.metric {
    display: flex; flex-direction: column; gap: 2px;
    padding: 8px 12px;
    background: rgba(15, 23, 42, 0.5);
    border-radius: 8px;
    border: 1px solid rgba(129, 140, 248, 0.1);
    flex: 1; min-width: 80px;
    animation: fadeSlideUp 0.5s ease forwards; opacity: 0;
}
.metric:nth-child(1) { animation-delay: 0.5s; }
.metric:nth-child(2) { animation-delay: 0.6s; }
.metric:nth-child(3) { animation-delay: 0.7s; }

.metric-label {
    font-size: 0.65rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.05em;
}

.metric-value {
    font-size: 0.8rem; color: #e2e8f0;
    font-weight: 600; font-family: 'JetBrains Mono', monospace;
}

.metric-active {
    color: #22c55e;
    animation: metricGlow 2s ease-in-out infinite;
}

@keyframes metricGlow {
    0%, 100% { text-shadow: 0 0 5px rgba(34, 197, 94, 0.3); }
    50% { text-shadow: 0 0 15px rgba(34, 197, 94, 0.6); }
}

.token-stream { color: #f0abfc; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

# Functions
LOGO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&h=120&fit=crop"

def _build_token_chars(token_text):
    return "".join(f"<span>{ch}</span>" for ch in token_text)

def get_loader_html(text="Yuki sedang berpikir", token="..."):
    token_chars = _build_token_chars(token)
    return f"""
        <div class="professional-loader">
            <div class="loader-header">
                <img src="{LOGO_URL}" class="loader-logo" alt="Yuki">
                <div>
                    <div class="loader-title">Yuki AI</div>
                    <div class="loader-subtitle">Processing Request</div>
                </div>
            </div>
            <div class="loader-message">
                <span>&#9889;</span>
                <span class="loader-text">{text}</span>
                <span class="loader-dots"><span>.</span><span>.</span><span>.</span></span>
            </div>
            <div class="loader-progress-container">
                <div class="loader-progress-bar"></div>
            </div>
            <div class="loader-metrics">
                <div class="metric">
                    <span class="metric-label">Status</span>
                    <span class="metric-value metric-active">Computing</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Tokens</span>
                    <span class="metric-value token-stream">[{token_chars}]</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Engine</span>
                    <span class="metric-value">Neural v2.6</span>
                </div>
            </div>
        </div>
    """

# Session State
if "has_entered" not in st.session_state:
    st.session_state["has_entered"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home Dashboard"

# Splash Screen
if not st.session_state["has_entered"]:
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
        div.stButton > button {
            width: 100%; padding: 14px; font-size: 18px; font-weight: 700;
            border-radius: 14px;
            background: linear-gradient(135deg, #7c3aed, #6d28d9);
            color: white; border: none;
            box-shadow: 0 4px 25px rgba(124, 58, 237, 0.5);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 40px rgba(124, 58, 237, 0.7);
        }
        .splash-logo {
            width: 120px; height: 120px; border-radius: 28px; object-fit: cover;
            box-shadow: 0 0 50px rgba(129, 140, 248, 0.5);
            border: 2px solid rgba(129, 140, 248, 0.4);
            animation: pulseLogo 2.5s ease-in-out infinite;
            margin-bottom: 20px;
        }
        @keyframes pulseLogo {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
    </style>
    """, unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 60px;">
                <img src="{LOGO_URL}" class="splash-logo" alt="Logo">
                <h1 style="color: white; font-size: 48px; font-weight: 700; margin-bottom: 0; font-family: 'Poppins', sans-serif;">AMPERA</h1>
                <h2 style="color: #a78bfa; font-size: 26px; font-weight: 300; margin-top: -8px; font-family: 'Poppins', sans-serif;">MULTI AI</h2>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 10px; letter-spacing: 2px;">Yuki Coding Studio & AI Neural Engine</p>
                <div style="width: 60px; height: 2px; background: linear-gradient(90deg, transparent, #a78bfa, transparent); margin: 25px auto;"></div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("MASUK", use_container_width=True):
            st.session_state["has_entered"] = True
            st.rerun()

        st.markdown('<div style="text-align: center; margin-top: 50px; color: #4b5563; font-size: 12px;">&copy; 2026 Yuki Coding Studio</div>', unsafe_allow_html=True)

# Main App
else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
            <div class="logo-container">
                <img src="{LOGO_URL}" class="logo-img" alt="Logo">
                <div class="logo-text">AMPERA MULTI AI</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Home Dashboard", use_container_width=True, key="sidebar_home"):
            st.session_state["current_page"] = "Home Dashboard"
            st.rerun()
        if st.button("Multi Ai", use_container_width=True, key="sidebar_arena"):
            st.session_state["current_page"] = "Multi Ai"
            st.rerun()
        if st.button("Leaderboard", use_container_width=True, key="sidebar_leaderboard"):
            st.session_state["current_page"] = "Leaderboard"
            st.rerun()
        if st.button("Search", use_container_width=True, key="sidebar_search"):
            st.session_state["current_page"] = "Search"
            st.rerun()

        st.markdown('<div class="sidebar-section-header">Notebook</div>', unsafe_allow_html=True)
        if st.button("Notebook baru", use_container_width=True, key="sidebar_notebook"):
            st.info("Fitur Notebook baru dipilih!")

        st.markdown('<div class="sidebar-section-header">Yesterday</div>', unsafe_allow_html=True)
        if st.button("Python Binary Search", use_container_width=True, key="sidebar_yesterday_python"):
            st.session_state["current_page"] = "Home Dashboard"
            st.session_state["shortcut_prompt"] = "Jelaskan kembali tentang Python Binary Search."
            st.rerun()
        if st.button("Fix Bug Index Error", use_container_width=True, key="sidebar_yesterday_bug"):
            st.session_state["current_page"] = "Home Dashboard"
            st.session_state["shortcut_prompt"] = "Bagaimana cara mengatasi IndexError di Python?"
            st.rerun()

    selected_menu = st.session_state["current_page"]

    # Home Dashboard
    if selected_menu == "Home Dashboard":
        if "home_chat_history" not in st.session_state:
            st.session_state["home_chat_history"] = []
        if "home_selected_model" not in st.session_state:
            st.session_state["home_selected_model"] = list(AVAILABLE_MODELS.keys())[0]

        if len(st.session_state["home_chat_history"]) > 0:
            if st.button("Percakapan Baru", key="new_chat_home"):
                st.session_state["home_chat_history"] = []
                st.rerun()
            
            for msg in st.session_state["home_chat_history"]:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-bubble-container"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(msg["content"])
                    st.markdown("---")
        else:
            st.markdown("<h1 style='text-align: center; margin-top: 1rem;'>What would you like to do?</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Ketik pesan di bawah dan tekan <b>Enter</b> untuk mengirim, Senpai! (o^&#9651;^o)</p>", unsafe_allow_html=True)

            st.markdown("<h3>Get started</h3>", unsafe_allow_html=True)
            gc1, gc2, gc3 = st.columns(3)

            with gc1:
                if st.button("Landing Page\n\nCreate a modern landing page", use_container_width=True, key="gs_landing"):
                    st.session_state["shortcut_prompt"] = "Buatkan kode landing page modern menggunakan HTML dan Tailwind CSS."
                    st.rerun()
                if st.button("Design to Code\n\nUpload an image and convert", use_container_width=True, key="gs_design"):
                    st.session_state["shortcut_prompt"] = "Bagaimana cara mengubah desain UI menjadi kode program?"
                    st.rerun()
            with gc2:
                if st.button("Dashboard\n\nInteractive charts & tables", use_container_width=True, key="gs_dashboard"):
                    st.session_state["shortcut_prompt"] = "Buatkan kerangka aplikasi dashboard interaktif menggunakan Python Streamlit."
                    st.rerun()
                if st.button("Fullstack App\n\nCreate templated full-stack app", use_container_width=True, key="gs_fullstack"):
                    st.session_state["shortcut_prompt"] = "Berikan arsitektur dasar untuk aplikasi web fullstack."
                    st.rerun()
            with gc3:
                if st.button("Make a Game\n\nPlayable browser game", use_container_width=True, key="gs_game"):
                    st.session_state["shortcut_prompt"] = "Buatkan game sederhana menggunakan HTML5 Canvas dan JavaScript."
                    st.rerun()
                if st.button("Storefront\n\nCreate online shop layout", use_container_width=True, key="gs_store"):
                    st.session_state["shortcut_prompt"] = "Buatkan layout halaman keranjang belanja online (e-commerce)."
                    st.rerun()

        default_val = st.session_state.pop("shortcut_prompt", "")
        
        # Model Picker
        spacer_col, fab_col = st.columns([12, 1])
        with fab_col:
            with st.popover("", use_container_width=True):
                st.markdown("**Pilih Model AI**")
                st.caption("Gratis | Premium")
                
                for label, model_id in AVAILABLE_MODELS.items():
                    icon = "&#10004;" if label == st.session_state["home_selected_model"] else ("&#128142;" if label in PREMIUM_MODELS else "&#9889;")
                    if st.button(f"{icon} {label}", key=f"pick_{model_id}", use_container_width=True):
                        st.session_state["home_selected_model"] = label
                        st.rerun()
        
        # Chat Input
        home_input = st.chat_input("Ask Yuki anything...", key="home_chat")
        model_choice_label = st.session_state["home_selected_model"]
        selected_model_id = AVAILABLE_MODELS[model_choice_label]
        query_to_process = home_input if home_input else default_val

        if query_to_process:
            if not groq_key:
                st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
            else:
                st.markdown(f'<div class="user-bubble-container"><div class="user-bubble">{query_to_process}</div></div>', unsafe_allow_html=True)

                loading_ph = st.empty()
                short_model_name = model_choice_label.split("—")[0].strip()
                
                loading_ph.html(get_loader_html(text=f"{short_model_name} sedang berpikir", token="reasoning"))

                time.sleep(7)

                try:
                    res_home = client.chat.completions.create(
                        model=selected_model_id,
                        messages=[
                            {"role": "system", "content": YUKI_SYSTEM_PROMPT},
                            {"role": "user", "content": query_to_process},
                        ],
                    )
                    response_text = res_home.choices[0].message.content
                except Exception as e:
                    response_text = f"Ups, terjadi kesalahan: {e}"

                loading_ph.empty()

                st.session_state["home_chat_history"].append({"role": "user", "content": query_to_process})
                st.session_state["home_chat_history"].append({"role": "assistant", "content": response_text})
                st.rerun()

    # Multi Ai (Arena)
    elif selected_menu == "Multi Ai":
        st.title("Ampera Coding Arena (Multi Ai)")
        st.caption("Pilih dua model berbeda, kirim tantangan koding, dan lihat animasi loading!")

        col_a, col_b = st.columns(2)
        with col_a:
            pilihan_a = st.selectbox("Petarung A:", options=list(AVAILABLE_MODELS.keys()), index=0, key="arena_a")
        with col_b:
            pilihan_b = st.selectbox("Petarung B:", options=list(AVAILABLE_MODELS.keys()), index=1, key="arena_b")
        
        arena_input = st.chat_input("Kirim tantangan duel coding...", key="arena_chat")

        if arena_input:
            st.session_state["last_arena_prompt"] = arena_input

        if "last_arena_prompt" in st.session_state:
            prompt_val = st.session_state["last_arena_prompt"]
            st.markdown(f'<div class="user-bubble-container"><div class="user-bubble">{prompt_val}</div></div>', unsafe_allow_html=True)

            if not groq_key:
                st.error("GROQ_API_KEY belum diatur!")
            elif pilihan_a == pilihan_b:
                st.warning("Pilih dua model yang berbeda!")
            else:
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown(f'<div style="background: rgba(15,23,42,0.75); border-radius: 14px; padding: 18px;"><div style="font-weight: 600; margin-bottom: 12px;">{pilihan_a}</div>', unsafe_allow_html=True)
                    loading_a = st.empty()
                    loading_a.html(get_loader_html(text=f"{pilihan_a} sedang merespons", token="computing"))
                    
                    start_a = time.time()
                    try:
                        resp_a = client.chat.completions.create(model=AVAILABLE_MODELS[pilihan_a], messages=[{"role": "system", "content": YUKI_SYSTEM_PROMPT}, {"role": "user", "content": prompt_val}])
                        text_a = resp_a.choices[0].message.content
                    except Exception as e:
                        text_a = f"Error: {e}"
                    if time.time() - start_a < 4.0:
                        time.sleep(4.0 - (time.time() - start_a))
                    loading_a.empty()
                    st.markdown(text_a)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_b:
                    st.markdown(f'<div style="background: rgba(15,23,42,0.75); border-radius: 14px; padding: 18px;"><div style="font-weight: 600; margin-bottom: 12px;">{pilihan_b}</div>', unsafe_allow_html=True)
                    loading_b = st.empty()
                    loading_b.html(get_loader_html(text=f"{pilihan_b} sedang merespons", token="analyzing"))
                    
                    start_b = time.time()
                    try:
                        resp_b = client.chat.completions.create(model=AVAILABLE_MODELS[pilihan_b], messages=[{"role": "system", "content": YUKI_SYSTEM_PROMPT}, {"role": "user", "content": prompt_val}])
                        text_b = resp_b.choices[0].message.content
                    except Exception as e:
                        text_b = f"Error: {e}"
                    if time.time() - start_b < 4.0:
                        time.sleep(4.0 - (time.time() - start_b))
                    loading_b.empty()
                    st.markdown(text_b)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("---")
                st.info("Arena Voting: Mana model yang memberikan hasil koding lebih baik?")
                v1, v2, v3 = st.columns(3)
                with v1:
                    if st.button("Pilih Petarung A", use_container_width=True, key="vote_a"):
                        st.success(f"Kamu memvoting {pilihan_a}!")
                with v2:
                    if st.button("Seri", use_container_width=True, key="vote_draw"):
                        st.success("Terima Kasih Atas Penilaian Anda!!")
                with v3:
                    if st.button("Pilih Petarung B", use_container_width=True, key="vote_b"):
                        st.success(f"Kamu memvoting {pilihan_b}!")

    # Leaderboard
    elif selected_menu == "Leaderboard":
        st.title("Ampera Leaderboard")
        st.write("Peringkat model AI berdasarkan performa koding dan voting pengguna:")
        st.markdown("""
        | Rank | Model Name | Elo Rating | Win Rate | Coding Score |
        | :---: | :--- | :---: | :---: | :---: |
        | 1 | **Llama 3.3 (70B)** | **1280** | 68.5% | 9.5 / 10 |
        | 2 | **Llama 3.1 (8B)** | **1210** | 61.2% | 8.8 / 10 |
        """)

    # Search
    elif selected_menu == "Search":
        st.title("Search")
        search_q = st.text_input("Cari topik atau riwayat (Tekan Enter)", key="search_input")
        if search_q:
            with st.spinner("Mencari..."):
                time.sleep(1)
            st.success(f"Menampilkan hasil pencarian untuk: **{search_q}**")
