import streamlit as st
from openai import OpenAI
import time

# Konfigurasi Halaman
st.set_page_config(page_title="Ampera Multi AI - Yuki Coding Studio", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Groq API (Pastikan GROQ_API_KEY ada di Streamlit Secrets)
try:
    groq_key = st.secrets["GROQ_API_KEY"]
    client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
except:
    groq_key = None
    client = None

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

# Styling CSS Global
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700;800;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #090d16);
        background-size: 400% 400%;
        animation: auroraBG 16s ease infinite;
        color: #f1f5f9;
    }
    @keyframes auroraBG { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    
    h1, h2, h3 { font-family: 'Poppins', sans-serif !important; }
    
    .logo-container { display: flex; align-items: center; gap: 12px; padding: 6px 4px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
    .logo-img { width: 44px; height: 44px; border-radius: 12px; object-fit: cover; border: 1px solid #818cf8; }
    .logo-text { font-size: 1.25rem; font-weight: 700; background: linear-gradient(135deg, #818cf8, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    [data-testid="stChatInput"] { border-radius: 9999px !important; border: 1px solid #818cf8 !important; }
    
    .user-bubble { background: linear-gradient(135deg, #3b82f6, #6366f1); color: white; padding: 12px 18px; border-radius: 14px; margin-bottom: 10px; }
    
    .arena-card { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 18px; }
    </style>
""", unsafe_allow_html=True)

# Fungsi Pendukung
def stream_response(text):
    placeholder = st.empty()
    streamed = ""
    for word in text.split(" "):
        streamed += word + " "
        placeholder.markdown(streamed)
        time.sleep(0.01)

# Session State
if "has_entered" not in st.session_state: st.session_state["has_entered"] = False
if "current_page" not in st.session_state: st.session_state["current_page"] = "🏠 Home Dashboard"

# 1. HALAMAN INTRO
if not st.session_state["has_entered"]:
    st.markdown("""
        <div style="display:flex; justify-content:center; align-items:center; min-height:80vh;">
          <div style="background: rgba(255,255,255,0.05); padding: 40px; border-radius: 24px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
            <h1>AMPERA MULTI AI</h1>
            <p>YUKI CODING STUDIO & AI NEURAL ENGINE</p>
          </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 MULAI SEKARANG"):
        st.session_state["has_entered"] = True
        st.rerun()

# 2. APLIKASI UTAMA
else:
    with st.sidebar:
        st.markdown('<div class="logo-container"><div class="logo-text">AMPERA MULTI AI</div></div>', unsafe_allow_html=True)
        if st.button("🏠 Home"): st.session_state["current_page"] = "🏠 Home Dashboard"
        if st.button("⚔️ Multi Ai"): st.session_state["current_page"] = "⚔️ Multi Ai"
        if st.button("📊 Leaderboard"): st.session_state["current_page"] = "📊 Leaderboard"

    selected_menu = st.session_state["current_page"]

    if selected_menu == "🏠 Home Dashboard":
        st.title("What would you like to do?")
        query = st.chat_input("Ask Yuki anything...")
        if query:
            if not client: st.error("API Key belum diset!")
            else:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": YUKI_SYSTEM_PROMPT}, {"role": "user", "content": query}]
                )
                stream_response(res.choices[0].message.content)

    elif selected_menu == "⚔️ Multi Ai":
        st.title("⚔️ Coding Arena")
        arena_input = st.chat_input("Tantang Model AI...")
        if arena_input:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Model A")
                st.write("Menjawab...")
            with col2:
                st.subheader("Model B")
                st.write("Menjawab...")

    elif selected_menu == "📊 Leaderboard":
        st.title("📊 Leaderboard")
        st.table({"Model": ["Llama-3.3-70b", "Llama-3.1-8b"], "Score": [9.5, 8.2]})
