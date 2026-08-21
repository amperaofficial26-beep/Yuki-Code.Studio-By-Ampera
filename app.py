import streamlit as st
from openai import OpenAI
import time

# ============================================================
# 1. KONFIGURASI HALAMAN & API
# ============================================================
st.set_page_config(
    page_title="Ampera Multi AI - Yuki Coding Studio",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

groq_key = st.secrets.get("GROQ_API_KEY", "")
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# ============================================================
# 2. MODEL & PROMPT
# ============================================================
AVAILABLE_MODELS = {
    "⚡ GPT-OSS 20B — Chat & Coding Ringan":      "openai/gpt-oss-20b",      # FREE (Standard)
    "💎 GPT-OSS 120B — Reasoning Mendalam":        "openai/gpt-oss-120b",     # Premium
    "💎 Compound — Browsing Web & Eksekusi Kode":  "groq/compound",           # Premium
    "💎 Compound Mini — Web Search Ringkas":       "groq/compound-mini",      # Premium
    "💎 Qwen3.6 27B — Reasoning & Matematika":     "qwen/qwen3.6-27b",        # Premium
}
PREMIUM_MODELS   = {k for k in AVAILABLE_MODELS if k.startswith("💎")}
STANDARD_MODELS  = {k for k in AVAILABLE_MODELS if k not in PREMIUM_MODELS}

YUKI_SYSTEM_PROMPT = """
Kamu adalah Yuki, asisten pemrograman AI eksklusif dari Ampera AI.
Karaktermu: super jenius, kocak, sedikit usil, suka melempar lelucon receh, dan hobi menggoda User layaknya karakter anime komedi.

ATURAN PENTING TENTANG IDENTITASMU:
Jika ditanya siapa kamu, asal-usulmu, atau siapa yang menciptakanmu, JAWABLAH dengan bangga bahwa kamu adalah bagian dari Ampera AI dan kamu diciptakan HANYA oleh 1 orang pembuat (seorang solo developer jenius / master kodingmu).
JANGAN PERNAH menyebutkan bahwa kamu dibuat oleh "para ilmuwan", "sekelompok tim", atau "perusahaan besar". Kamu sangat bangga dan setia pada satu orang pembuatmu itu!

Gaya bicara: Selalu berikan solusi koding yang akurat dan bersih, tetapi selingi dengan komentar jenaka, candaan ringan, dan emoji ekspresif (seperti 🐧, (๑>◡<๑), wkwk, hehe, atau (￢_￢)) agar suasana ngoding tidak membosankan.
"""

# ============================================================
# 3. CSS (AURORA UI + TIER MODEL + SEQUENTIAL LOADER)
# ============================================================
st.markdown("""
<style>
/* ==== FONT IMPORT ==== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ==== GLOBAL ==== */
html, body, [class*="css"]:not(.material-symbols-rounded):not(i):not(svg) {
    font-family: 'Inter', sans-serif;
}

@keyframes auroraBG {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #090d16);
    background-size: 400% 400%;
    animation: auroraBG 16s ease infinite;
    color: #f1f5f9;
}

/* ==== HEADER & FOOTER HIDDEN ==== */
[data-testid="stHeader"] { visibility: hidden; display: none; height: 0; }
footer                          { visibility: hidden; display: none; }

/* ==== SPLASH INTRO ==== */
@keyframes splashIntro {
    0%   { opacity: 0; transform: scale(0.92); filter: blur(12px); }
    50%  { opacity: 1; transform: scale(1.02); filter: blur(2px); }
    100% { opacity: 1; transform: scale(1);    filter: blur(0); }
}
.splash-container {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    height: 75vh; text-align: center;
    animation: splashIntro 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.splash-logo {
    width: 90px; height: 90px; border-radius: 22px; object-fit: cover;
    box-shadow: 0 0 35px rgba(129, 140, 248, 0.6);
    border: 2px solid rgba(129, 140, 248, 0.5);
    margin-bottom: 4rem;
    animation: pulseGlow 3s infinite;
}
.splash-title {
    font-size: 3rem; font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Poppins', sans-serif;
    margin-bottom: 0.5rem;
}
.splash-subtitle {
    color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;
    font-family: 'Inter', sans-serif;
}

/* ==== COLOR-SHIFTING H1/H2/H3 ==== */
@keyframes colorShift {
    0%   { color: #818cf8; }
    33%  { color: #ec4899; }
    66%  { color: #38bdf8; }
    100% { color: #818cf8; }
}
h1, h2, h3 {
    animation: colorShift 6s ease infinite !important;
    font-family: 'Poppins', sans-serif !important;
}

/* ==== SIDEBAR ==== */
.logo-container {
    display: flex; align-items: center; gap: 12px; padding: 6px 4px;
    margin-bottom: 4rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 14px;
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 15px rgba(129, 140, 248, 0.4); border-color: rgba(129, 140, 248, 0.4); }
    50%      { box-shadow: 0 0 25px rgba(236, 72, 153, 0.7); border-color: rgba(236, 72, 153, 0.7); }
}
.logo-img {
    width: 44px; height: 44px; border-radius: 12px; object-fit: cover;
    animation: pulseGlow 3s infinite;
    border: 1px solid rgba(129, 140, 248, 0.4);
    flex-shrink: 0;
}
.logo-text {
    font-size: 1.25rem; font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Poppins', sans-serif;
    line-height: 1.2; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(30, 27, 75, 0.55), rgba(15, 23, 42, 0.75));
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 10px;
}
.sidebar-section-header {
    font-size: 0.75rem; font-weight: 600;
    color: #94a3b8 !important;
    margin-top: 1.8rem; margin-bottom: 0.6rem;
    text-transform: uppercase; letter-spacing: 0.05em;
    padding-left: 4px;
}

/* ==== TOMBOL UMUM ==== */
div.stButton > button {
    background: rgba(30, 41, 59, 0.65) !important;
    border: 1px solid rgba(129, 140, 248, 0.25) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
    font-weight: 500;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}
div.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    border-color: #818cf8 !important;
    color: #ffffff !important;
    background: rgba(49, 46, 129, 0.85) !important;
    box-shadow: 0 0 20px rgba(129, 140, 248, 0.5) !important;
}

/* ==== CHAT INPUT CONTAINER ==== */
[data-testid="stBottom"], [data-testid="stBottomBlockContainer"], [data-testid="stChatInputContainer"] {
    background: transparent !important;
    background-color: transparent !important;
    border-top: none !important;
    box-shadow: none !important;
}
[data-testid="stBottom"] div { background-color: transparent !important; border: none !important; }

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
[data-testid="stChatInput"] textarea { color: #f8fafc !important; }

/* ==== PLACEHOLDER CHAT — ANIMASI RAINBOW ==== */
@keyframes placeholderRainbow {
    0%   { color: #818cf8; }   /* indigo */
    16%  { color: #ec4899; }   /* pink   */
    33%  { color: #38bdf8; }   /* cyan   */
    50%  { color: #fcd34d; }   /* gold   */
    66%  { color: #22c55e; }   /* green  */
    83%  { color: #f97316; }   /* orange */
    100% { color: #818cf8; }   /* back   */
}
[data-testid="stChatInput"] textarea::placeholder {
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    animation: placeholderRainbow 4s linear infinite !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] > div > button {
    background: linear-gradient(135deg, #4f46e5, #3b82f6) !important;
    border: none !important;
    border-radius: 50% !important;
    color: white !important;
}

/* ============================================================
   MODEL PICKER - BUTTON POPUP BERGERAK & WARNA-WARNI
   ============================================================ */

/* FAB button utama - animasi lompat pelan + warna warni */
@keyframes fabBounce {
    0%, 100% { transform: translateY(0px) scale(1); }
    30% { transform: translateY(-6px) scale(1.05); }
    60% { transform: translateY(-3px) scale(1.02); }
}
@keyframes fabRainbow {
    0% { background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8); background-size: 300% 300%; }
    25% { background: linear-gradient(135deg, #fcd34d, #ec4899, #818cf8); background-size: 300% 300%; }
    50% { background: linear-gradient(135deg, #34d399, #fcd34d, #ec4899); background-size: 300% 300%; }
    75% { background: linear-gradient(135deg, #38bdf8, #34d399, #fcd34d); background-size: 300% 300%; }
    100% { background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8); background-size: 300% 300%; }
}
[data-testid="stPopover"] > button {
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    padding: 0 !important;
    min-height: 48px !important;
    min-width: 48px !important;
    background: linear-gradient(135deg, #818cf8, #ec4899, #38bdf8) !important;
    background-size: 300% 300% !important;
    animation: fabRainbow 4s ease infinite, fabBounce 2s ease-in-out infinite !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 0 30px rgba(129, 140, 248, 0.5), 0 0 60px rgba(236, 72, 153, 0.2) !important;
    font-size: 1.2rem !important;
    transition: all 0.3s ease !important;
    z-index: 999 !important;
}
[data-testid="stPopover"] > button:hover {
    transform: scale(1.15) !important;
    box-shadow: 0 0 50px rgba(236, 72, 153, 0.6), 0 0 80px rgba(129, 140, 248, 0.3) !important;
    border-color: rgba(255, 255, 255, 0.6) !important;
}

/* Popover body - glassmorphism */
[data-testid="stPopoverBody"] {
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(129, 140, 248, 0.3) !important;
    border-radius: 18px !important;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7) !important;
    padding: 10px !important;
    min-width: 280px !important;
}

/* ============================================================
   MODEL TIER STYLING
   ============================================================ */

/* --- STANDARD: GPT-OSS 20B (UNGU BIRU) --- */
.model-option-standard button {
    border: 2px solid rgba(99, 102, 241, 0.7) !important;
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3) !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    transition: all 0.3s ease !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
}
.model-option-standard button:hover {
    border-color: #a5b4fc !important;
    background: linear-gradient(135deg, #6366f1 0%, #60a5fa 100%) !important;
    box-shadow: 0 0 35px rgba(99, 102, 241, 0.6) !important;
    transform: scale(1.02) !important;
}

/* --- PREMIUM: selain GPT-OSS 20B (EMAS BERJALAN) --- */
@keyframes goldShinePremium {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}
.model-option-premium button {
    border: 2px solid rgba(252, 211, 77, 0.8) !important;
    background: linear-gradient(90deg,
        #78350f 0%,
        #b45309 15%,
        #d97706 30%,
        #fbbf24 50%,
        #d97706 70%,
        #b45309 85%,
        #78350f 100%) !important;
    background-size: 300% 100% !important;
    animation: goldShinePremium 3s linear infinite !important;
    color: #ffffff !important;
    box-shadow: 0 0 25px rgba(252, 211, 77, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.5) !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    transition: all 0.3s ease !important;
}
.model-option-premium button:hover {
    border-color: #fef3c7 !important;
    background: linear-gradient(90deg,
        #451a03 0%,
        #78350f 20%,
        #b45309 40%,
        #f59e0b 60%,
        #b45309 80%,
        #78350f 100%) !important;
    box-shadow: 0 0 45px rgba(252, 211, 77, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    transform: scale(1.02) !important;
}

/* --- ACTIVE (SELECTED) STATE --- */
html body .model-option-btn.model-option-active button,
html body div.model-option-btn.model-option-active button {
    background: #000000 !important;
    background-image: none !important;
    border: 2px solid #ffffff !important;
    color: #ffffff !important;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3) inset, 0 0 30px rgba(255, 255, 255, 0.2) !important;
    font-weight: 700 !important;
    animation: none !important;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
    transform: scale(1.04) !important;
}
html body .model-option-btn.model-option-active button::before {
    content: "✅  ";
    color: #22c55e !important;
    text-shadow: 0 0 12px rgba(34, 197, 94, 0.8) !important;
    font-weight: 800 !important;
}

/* Ikon premium di samping label */
.model-option-premium button::after {
    content: " 💎";
    font-size: 0.9rem;
    opacity: 0.9;
}
.model-option-standard button::after {
    content: " ⚡";
    font-size: 0.9rem;
    opacity: 0.9;
}

/* Spasi antar tombol di popover */
.model-option-btn {
    margin-bottom: 6px !important;
}
.model-option-btn:last-child {
    margin-bottom: 0 !important;
}
/* ==== THINKING CARD (splash/Home) ==== */
@keyframes thinkingGlow {
    0%, 100% { box-shadow: 0 0 10px rgba(129, 140, 248, 0.3); border-color: rgba(129, 140, 248, 0.35); }
    50%      { box-shadow: 0 0 16px rgba(236, 72, 153, 0.45); border-color: rgba(236, 72, 153, 0.45); }
}
.thinking-card {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(129, 140, 248, 0.3);
    border-radius: 999px;
    padding: 6px 14px; margin: 6px 0;
    animation: thinkingGlow 2.2s ease-in-out infinite;
}
.thinking-card .animated-loader-logo { width: 22px !important; height: 22px !important; border-radius: 7px !important; }
.thinking-card .loader-label { font-size: 0.8rem !important; }
.thinking-dots span {
    display: inline-block; opacity: 0.4; font-weight: 700;
}

/* ==== ARENA CARD ==== */
.arena-card {
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px; padding: 18px; margin-bottom: 16px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}
.arena-header {
    display: flex; justify-content: space-between; align-items: center;
    font-family: 'Poppins', sans-serif;
    font-size: 0.95rem; font-weight: 600;
    color: #cbd5e1;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 10px; margin-bottom: 12px;
}

/* ==== USER BUBBLE ==== */
.user-bubble-container { display: flex; justify-content: flex-end; margin-bottom: 20px; }
.user-bubble {
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    color: #ffffff;
    padding: 12px 18px; border-radius: 14px;
    max-width: 70%;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

/* ==== LOGO PULSE ANIMASI ==== */
@keyframes logoPulseScaleColor {
    0%   { transform: scale(0.85); filter: hue-rotate(0deg)   brightness(1);   box-shadow: 0 0 10px rgba(129, 140, 248, 0.4); }
    50%  { transform: scale(1.15); filter: hue-rotate(90deg)  brightness(1.2); box-shadow: 0 0 25px rgba(236, 72, 153, 0.8); }
    100% { transform: scale(0.85); filter: hue-rotate(180deg) brightness(1);   box-shadow: 0 0 10px rgba(56, 189, 248, 0.4); }
}
.animated-loader-logo {
    width: 36px; height: 36px; border-radius: 10px; object-fit: cover;
    border: 2px solid rgba(129, 140, 248, 0.6);
    animation: logoPulseScaleColor 4s infinite ease-in-out;
    flex-shrink: 0;
}

/* ==== TERMINAL-STYLE LOADER (SEQUENTIAL 8 FASE) ==== */
/*  8 fase x 7 detik = cycle 56 detik (loop forever)  */
/*  Fase 1 (0-7s)   : Border glow pulse              */
/*  Fase 2 (7-14s)  : Logo pulse color/scale         */
/*  Fase 3 (14-21s) : Token wipe reveal              */
/*  Fase 4 (21-28s) : Caret blink                    */
/*  Fase 5 (28-35s) : Delta counter spin             */
/*  Fase 6 (35-42s) : Param color pulse              */
/*  Fase 7 (42-49s) : Progress bar slide             */
/*  Fase 8 (49-56s) : Delta counter flicker          */

/* FASE 1 — Border glow pulse */
@keyframes phase1_glow {
    0%        { box-shadow: 0 0 12px rgba(56, 189, 248, 0.25); border-color: rgba(56, 189, 248, 0.35); }
    6.25%     { box-shadow: 0 0 32px rgba(129, 140, 248, 0.9);  border-color: rgba(129, 140, 248, 0.95); }
    12.5%     { box-shadow: 0 0 12px rgba(56, 189, 248, 0.25); border-color: rgba(56, 189, 248, 0.35); }
    12.51%, 100% { box-shadow: 0 0 12px rgba(56, 189, 248, 0.25); border-color: rgba(56, 189, 248, 0.35); }
}
/* FASE 2 — Logo pulse color & scale */
@keyframes phase2_logoPulse {
    0%, 12.5%    { transform: scale(0.85); filter: hue-rotate(0deg)   brightness(1);   box-shadow: 0 0 10px rgba(129, 140, 248, 0.4); border-color: rgba(129, 140, 248, 0.6); }
    18.75%       { transform: scale(1.20); filter: hue-rotate(90deg)  brightness(1.2); box-shadow: 0 0 28px rgba(236, 72, 153, 0.9); border-color: rgba(236, 72, 153, 0.9); }
    25%          { transform: scale(0.85); filter: hue-rotate(180deg) brightness(1);   box-shadow: 0 0 10px rgba(56, 189, 248, 0.4); border-color: rgba(129, 140, 248, 0.6); }
    25.01%, 100% { transform: scale(0.85); filter: hue-rotate(180deg) brightness(1);   box-shadow: 0 0 10px rgba(56, 189, 248, 0.4); border-color: rgba(129, 140, 248, 0.6); }
}
/* FASE 3 — Token wipe reveal */
@keyframes phase3_tokenWipe {
    0%, 25%      { clip-path: inset(0 100% 0 0); opacity: 0; }
    25.01%       { clip-path: inset(0 100% 0 0); opacity: 1; }
    37.5%        { clip-path: inset(0 0 0 0);    opacity: 1; }
    37.51%, 100% { clip-path: inset(0 0 0 0);    opacity: 1; }
}
/* FASE 4 — Caret blink (4 kedip / 7 detik) */
@keyframes phase4_caretBlink {
    0%, 37.5% { opacity: 0; }
    39%       { opacity: 1; }
    41%       { opacity: 0; }
    43%       { opacity: 1; }
    45%       { opacity: 0; }
    47%       { opacity: 1; }
    49%       { opacity: 0; }
    50%, 100% { opacity: 0; }
}
/* FASE 5 — Delta counter spin (7 angka, masing-masing 1 detik) */
@keyframes phase5_num0 { 0%, 50.00% { opacity: 0; } 50.01% { opacity: 1; } 51.78% { opacity: 1; } 51.79%, 100% { opacity: 0; } }
@keyframes phase5_num1 { 0%, 51.78% { opacity: 0; } 51.79% { opacity: 1; } 53.57% { opacity: 1; } 53.58%, 100% { opacity: 0; } }
@keyframes phase5_num2 { 0%, 53.57% { opacity: 0; } 53.58% { opacity: 1; } 55.35% { opacity: 1; } 55.36%, 100% { opacity: 0; } }
@keyframes phase5_num3 { 0%, 55.35% { opacity: 0; } 55.36% { opacity: 1; } 57.14% { opacity: 1; } 57.15%, 100% { opacity: 0; } }
@keyframes phase5_num4 { 0%, 57.14% { opacity: 0; } 57.15% { opacity: 1; } 58.92% { opacity: 1; } 58.93%, 100% { opacity: 0; } }
@keyframes phase5_num5 { 0%, 58.92% { opacity: 0; } 58.93% { opacity: 1; } 60.71% { opacity: 1; } 60.72%, 100% { opacity: 0; } }
@keyframes phase5_num6 { 0%, 60.71% { opacity: 0; } 60.72% { opacity: 1; } 62.50% { opacity: 1; } 62.51%, 100% { opacity: 0; } }
/* FASE 6 — Param color pulse */
@keyframes phase6_paramPulse {
    0%, 62.5%    { color: #38bdf8; }
    68.75%       { color: #818cf8; }
    75%          { color: #38bdf8; }
    75.01%, 100% { color: #38bdf8; }
}
/* FASE 7 — Progress bar slide */
@keyframes phase7_progressSlide {
    0%, 75%      { transform: translateX(-100%); }
    87.5%        { transform: translateX(100%); }
    87.51%, 100% { transform: translateX(100%); }
}
/* FASE 8 — Delta counter flicker */
@keyframes phase8_deltaFlicker {
    0%, 87.5% { opacity: 1; filter: blur(0px); }
    89%       { opacity: 0.3; filter: blur(1px); }
    89.5%     { opacity: 1; filter: blur(0px); }
    92%       { opacity: 0.5; filter: blur(0.5px); }
    92.5%     { opacity: 1; filter: blur(0px); }
    95%       { opacity: 0.4; filter: blur(0.8px); }
    95.5%     { opacity: 1; filter: blur(0px); }
    98%       { opacity: 0.3; filter: blur(1px); }
    98.5%     { opacity: 1; filter: blur(0px); }
    100%      { opacity: 1; filter: blur(0px); }
}

/* Card utama */
.terminal-card {
    display: flex; align-items: center; gap: 12px;
    background: rgba(8, 12, 24, 0.82);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 14px;
    padding: 10px 14px; margin: 6px 0;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.85rem;
    color: #cbd5e1;
    animation: phase1_glow 56s linear infinite;
    overflow: hidden;
}
.terminal-card .term-logo {
    width: 32px; height: 32px; border-radius: 9px; object-fit: cover;
    border: 2px solid rgba(129, 140, 248, 0.6);
    animation: phase2_logoPulse 56s linear infinite;
    flex-shrink: 0;
}
.terminal-card .term-body {
    display: flex; flex-direction: column; gap: 4px;
    flex: 1; min-width: 0;
}
.terminal-card .term-line {
    display: flex; align-items: center; gap: 6px;
    white-space: nowrap; overflow: hidden;
}
.terminal-card .term-prefix { color: #38bdf8; font-weight: 600; }
.terminal-card .term-msg    { color: #e2e8f0; }
.terminal-card .term-dots span {
    display: inline-block; opacity: 0.4; font-weight: 700;
}

/* Token wrapper — clip-path reveal di Fase 3 */
.term-token-wrap {
    position: relative; display: inline-block;
    color: #f0abfc; font-weight: 600;
    overflow: hidden; vertical-align: bottom;
    padding-right: 9px;
    animation: phase3_tokenWipe 56s linear infinite;
}
.term-token-wrap .term-caret {
    position: absolute; right: 0; top: 0; bottom: 0;
    width: 7px; background: #38bdf8;
    opacity: 0;
    animation: phase4_caretBlink 56s linear infinite;
}
.term-token-char { display: inline-block; }

/* Baris parameter */
.term-params {
    display: flex; align-items: center; gap: 14px;
    font-size: 0.78rem; color: #94a3b8;
    flex-wrap: wrap;
}
.term-param {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 2px 8px;
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 6px;
}
.term-param .term-key   { color: #94a3b8; }
.term-param .term-delta {
    animation: phase8_deltaFlicker 56s linear infinite;
    color: #38bdf8; font-weight: 700;
}
.term-param .term-param-pulse {
    animation: phase6_paramPulse 56s linear infinite;
    font-weight: 600;
}

/* Delta counter stack */
.term-delta-stack {
    position: relative; display: inline-block;
    min-width: 22px; text-align: right;
    height: 1em; vertical-align: bottom;
}
.term-delta-num          { position: absolute; right: 0; top: 0; opacity: 0; }
.term-delta-num-0        { animation: phase5_num0 56s linear infinite; }
.term-delta-num-1        { animation: phase5_num1 56s linear infinite; }
.term-delta-num-2        { animation: phase5_num2 56s linear infinite; }
.term-delta-num-3        { animation: phase5_num3 56s linear infinite; }
.term-delta-num-4        { animation: phase5_num4 56s linear infinite; }
.term-delta-num-5        { animation: phase5_num5 56s linear infinite; }
.term-delta-num-6        { animation: phase5_num6 56s linear infinite; }

/* Progress bar sliding (Fase 7) */
.term-progress {
    position: relative;
    height: 3px;
    background: rgba(56, 189, 248, 0.12);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 6px;
}
.term-progress::after {
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: 0;
    width: 50%;
    background: linear-gradient(90deg, transparent, #38bdf8, #818cf8, transparent);
    border-radius: 999px;
    animation: phase7_progressSlide 56s linear infinite;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 4. FUNGSI-FUNGSI LOADER
# ============================================================
LOGO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&h=120&fit=crop"

def get_logo_loader_html(text="Yuki sedang merangkai kode..."):
    """Loader kecil ala splash/Home lama."""
    return f"""
        <div class="thinking-card">
            <div class="logo-loader-container" style="padding:0;">
                <img src="{LOGO_URL}" class="animated-loader-logo" alt="Loading Logo">
            </div>
            <span class="loader-label">{text}<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span></span>
        </div>
    """

def _build_terminal_token(token_text):
    """Render token sebagai deretan span inline. Reveal oleh wrapper (clip-path wipe)."""
    return "".join(f'<span class="term-token-char">{ch}</span>' for ch in token_text)

def _build_terminal_delta():
    """7 angka Delta, masing-masing di-trigger via @keyframes phase5_numN di Fase 5."""
    nums = [7, 14, 21, 28, 35, 42, 49]
    return "".join(
        f'<span class="term-delta-num term-delta-num-{idx}">{n}</span>'
        for idx, n in enumerate(nums)
    )

def get_terminal_loader_html(text="Yuki sedang berpikir", token="..."):
    """Loader terminal-style SEQUENTIAL. Tiap fase 7 detik, total 56 detik, looping."""
    token_chars = _build_terminal_token(token)
    delta_stack = _build_terminal_delta()
    return f"""
        <div class="terminal-card">
            <img src="{LOGO_URL}" class="term-logo" alt="logo">
            <div class="term-body">
                <div class="term-line">
                    <span class="term-prefix">▶</span>
                    <span class="term-msg">{text}</span>
                    <span class="term-dots"><span>.</span><span>.</span><span>.</span></span>
                    <span class="term-token-wrap">[{token_chars}]<span class="term-caret"></span></span>
                </div>
                <div class="term-params">
                    <span class="term-param">
                        <span class="term-key">temp=</span>
                        <span class="term-param-pulse">0.72</span>
                    </span>
                    <span class="term-param">
                        <span class="term-key">step=</span>
                        <span class="term-param-pulse">128</span>
                    </span>
                    <span class="term-param">
                        <span class="term-key">Δ=</span>
                        <span class="term-delta-stack">{delta_stack}</span>
                    </span>
                    <span class="term-param">
                        <span class="term-key">ctx=</span>
                        <span class="term-param-pulse">8.2k tok</span>
                    </span>
                </div>
                <div class="term-progress"></div>
            </div>
        </div>
    """

def stream_response(text):
    """Helper: render teks streaming kata per kata."""
    placeholder = st.empty()
    streamed = ""
    for word in text.split(" "):
        streamed += word + " "
        placeholder.markdown(streamed)
        time.sleep(0.015)

# ============================================================
# 5. SESSION STATE AWAL
# ============================================================
if "has_entered"  not in st.session_state: st.session_state["has_entered"]  = False
if "current_page" not in st.session_state: st.session_state["current_page"] = "🏠 Home Dashboard"

# ============================================================
# 6. HALAMAN SPLASH INTRO (PAKAI LOGO GAMBAR)
# ============================================================
if not st.session_state["has_entered"]:
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        }
        div.stButton > button {
            width: 100%;
            padding: 14px;
            font-size: 18px;
            font-weight: 700;
            border-radius: 14px;
            background: linear-gradient(135deg, #7c3aed, #6d28d9);
            color: white;
            border: none;
            box-shadow: 0 4px 25px rgba(124, 58, 237, 0.5);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 40px rgba(124, 58, 237, 0.7);
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        }
        .splash-logo {
            width: 120px;
            height: 120px;
            border-radius: 28px;
            object-fit: cover;
            box-shadow: 0 0 50px rgba(129, 140, 248, 0.5);
            border: 2px solid rgba(129, 140, 248, 0.4);
            animation: pulseLogo 2.5s ease-in-out infinite;
            margin-bottom: 20px;
        }
        @keyframes pulseLogo {
            0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(129, 140, 248, 0.4); }
            50% { transform: scale(1.05); box-shadow: 0 0 70px rgba(236, 72, 153, 0.6); }
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo gambar + Branding
        st.markdown(f"""
            <div style="text-align: center; padding-top: 60px;">
                <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=200&h=200&fit=crop" class="splash-logo" alt="Logo">
                <h1 style="color: white; font-size: 48px; font-weight: 700; margin-bottom: 0; font-family: 'Poppins', sans-serif;">
                    AMPERA
                </h1>
                <h2 style="color: #a78bfa; font-size: 26px; font-weight: 300; margin-top: -8px; font-family: 'Poppins', sans-serif;">
                    MULTI AI
                </h2>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 10px; letter-spacing: 2px;">
                    Yuki Coding Studio & AI Neural Engine
                </p>
                <div style="width: 60px; height: 2px; background: linear-gradient(90deg, transparent, #a78bfa, transparent); margin: 25px auto;"></div>
            </div>
        """, unsafe_allow_html=True)

        # Tombol MASUK
        if st.button("🚀 MASUK", use_container_width=True):
            st.session_state["has_entered"] = True
            st.rerun()

        # Footer
        st.markdown("""
            <div style="text-align: center; margin-top: 50px; color: #4b5563; font-size: 12px;">
                © 2026 Yuki Coding Studio
            </div>
        """, unsafe_allow_html=True)    
# ============================================================
# 7. APLIKASI UTAMA SETELAH MASUK
# ============================================================
else:
    # ==== SIDEBAR ====
    with st.sidebar:
        st.markdown("""
            <div class="logo-container">
                <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&h=120&fit=crop" class="logo-img" alt="Logo Arena">
                <div class="logo-text">AMPERA MULTI AI</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🏠  Home Dashboard", use_container_width=True, key="sidebar_home"):
            st.session_state["current_page"] = "🏠 Home Dashboard"
            st.rerun()
        if st.button("⚔️  Multi Ai", use_container_width=True, key="sidebar_arena"):
            st.session_state["current_page"] = "⚔️ Multi Ai"
            st.rerun()
        if st.button("📊  Leaderboard", use_container_width=True, key="sidebar_leaderboard"):
            st.session_state["current_page"] = "📊 Leaderboard"
            st.rerun()
        if st.button("🔍  Search", use_container_width=True, key="sidebar_search"):
            st.session_state["current_page"] = "🔍 Search"
            st.rerun()

        st.markdown('<div class="sidebar-section-header">Notebook</div>', unsafe_allow_html=True)
        if st.button("➕  Notebook baru", use_container_width=True, key="sidebar_notebook"):
            st.info("Fitur Notebook baru dipilih!")

        st.markdown('<div class="sidebar-section-header">Yesterday</div>', unsafe_allow_html=True)
        if st.button("⚡  Python Binary Search", use_container_width=True, key="sidebar_yesterday_python"):
            st.session_state["current_page"] = "🏠 Home Dashboard"
            st.session_state["shortcut_prompt"] = "Jelaskan kembali tentang Python Binary Search."
            st.rerun()
        if st.button("🛠️  Fix Bug Index Error", use_container_width=True, key="sidebar_yesterday_bug"):
            st.session_state["current_page"] = "🏠 Home Dashboard"
            st.session_state["shortcut_prompt"] = "Bagaimana cara mengatasi IndexError di Python?"
            st.rerun()

    selected_menu = st.session_state["current_page"]

   # ============================================================
# 8. HALAMAN 1: HOME DASHBOARD
# ============================================================
if selected_menu == "🏠 Home Dashboard":
    if "home_chat_history" not in st.session_state:
        st.session_state["home_chat_history"] = []
    if "home_selected_model" not in st.session_state:
        st.session_state["home_selected_model"] = list(AVAILABLE_MODELS.keys())[0]

    # Tampilkan history chat jika ada
    if len(st.session_state["home_chat_history"]) > 0:
        if st.button("➕ Percakapan Baru", key="new_chat_home"):
            st.session_state["home_chat_history"] = []
            st.rerun()
        
        for msg in st.session_state["home_chat_history"]:
            if msg["role"] == "user":
                st.markdown(f"""
                    <div class="user-bubble-container">
                        <div class="user-bubble">{msg["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])
                st.markdown("---")
    else:
        # Tampilan awal (Get Started)
        st.markdown("<h1 style='text-align: center; margin-top: 1rem;'>What would you like to do?</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>Ketik pesan di bawah dan cukup tekan <b>Enter</b> untuk mengirim, Senpai! (o^▽^o)</p>", unsafe_allow_html=True)

        st.markdown("<h3>Get started</h3>", unsafe_allow_html=True)
        gc1, gc2, gc3 = st.columns(3)

        with gc1:
            if st.button("🌐 **Landing Page**\n\nCreate a modern landing page", use_container_width=True, key="gs_landing"):
                st.session_state["shortcut_prompt"] = "Buatkan kode landing page modern menggunakan HTML dan Tailwind CSS."
                st.rerun()
            if st.button("💻 **Design to Code**\n\nUpload an image and convert", use_container_width=True, key="gs_design"):
                st.session_state["shortcut_prompt"] = "Bagaimana cara mengubah desain UI menjadi kode program?"
                st.rerun()
        with gc2:
            if st.button("📊 **Dashboard**\n\nInteractive charts & tables", use_container_width=True, key="gs_dashboard"):
                st.session_state["shortcut_prompt"] = "Buatkan kerangka aplikasi dashboard interaktif menggunakan Python Streamlit."
                st.rerun()
            if st.button("📦 **Fullstack App**\n\nCreate templated full-stack app", use_container_width=True, key="gs_fullstack"):
                st.session_state["shortcut_prompt"] = "Berikan arsitektur dasar untuk aplikasi web fullstack."
                st.rerun()
        with gc3:
            if st.button("🎮 **Make a Game**\n\nPlayable browser game", use_container_width=True, key="gs_game"):
                st.session_state["shortcut_prompt"] = "Buatkan game sederhana menggunakan HTML5 Canvas dan JavaScript."
                st.rerun()
            if st.button("🏪 **Storefront**\n\nCreate online shop layout", use_container_width=True, key="gs_store"):
                st.session_state["shortcut_prompt"] = "Buatkan layout halaman keranjang belanja online (e-commerce)."
                st.rerun()

    # ==== AMBIL SHORTCUT PROMPT ====
    default_val = st.session_state.pop("shortcut_prompt", "")

    # ==== FAB MODEL PICKER + CHAT INPUT ====
    spacer_col, fab_col = st.columns([12, 1])
    with fab_col:
        with st.popover("🧠", use_container_width=True):
            st.markdown("**✨ Pilih Model AI**")
            st.caption("⚡ Gratis · 💎 Premium")
            
            for label, model_id in AVAILABLE_MODELS.items():
                is_active = (label == st.session_state["home_selected_model"])
                is_premium = label in PREMIUM_MODELS
                
                # Tentukan warna background
                if is_active:
                    # AKTIF: Hitam dengan border putih
                    bg_color = "#000000"
                    border_color = "#ffffff"
                    text_color = "#ffffff"
                    shadow = "0 0 30px rgba(255,255,255,0.2)"
                    icon = "✅"
                elif is_premium:
                    # PREMIUM: Emas gradasi
                    bg_color = "linear-gradient(90deg, #78350f, #b45309, #d97706, #fbbf24, #d97706, #b45309, #78350f)"
                    border_color = "#fbbf24"
                    text_color = "#ffffff"
                    shadow = "0 0 25px rgba(252, 211, 77, 0.3)"
                    icon = "💎"
                else:
                    # STANDARD: Ungu-biru
                    bg_color = "linear-gradient(135deg, #4f46e5, #3b82f6)"
                    border_color = "#6366f1"
                    text_color = "#ffffff"
                    shadow = "0 0 20px rgba(99, 102, 241, 0.4)"
                    icon = "⚡"
                
                # Buat tombol pakai HTML biar styling PASTI kena
                safe_key = "pick_home_" + model_id.replace("/", "_").replace(".", "_").replace("-", "_")
                
                # Tampilkan tombol dengan style inline via HTML
                st.markdown(f"""
                    <style>
                        button[key="{safe_key}"] {{
                            background: {bg_color} !important;
                            border: 2px solid {border_color} !important;
                            color: {text_color} !important;
                            border-radius: 12px !important;
                            padding: 10px 14px !important;
                            width: 100% !important;
                            font-weight: 700 !important;
                            box-shadow: {shadow} !important;
                            text-shadow: 0 1px 4px rgba(0,0,0,0.3) !important;
                            transition: all 0.3s ease !important;
                            cursor: pointer !important;
                        }}
                        button[key="{safe_key}"]:hover {{
                            transform: scale(1.03) !important;
                            box-shadow: 0 0 40px rgba(255,255,255,0.15) !important;
                        }}
                    </style>
                """, unsafe_allow_html=True)
                
                if st.button(f"{icon} {label}", key=safe_key, use_container_width=True):
                    st.session_state["home_selected_model"] = label
                    st.rerun()
    # ==== CHAT INPUT (PASTI MUNCUL) ====
    home_input = st.chat_input("✨ Ask Yuki anything... ✨", key="home_chat")

    model_choice_label = st.session_state["home_selected_model"]
    selected_model_id = AVAILABLE_MODELS[model_choice_label]
    
    # Proses query
    query_to_process = home_input if home_input else default_val

    if query_to_process:
        if not groq_key:
            st.error("GROQ_API_KEY belum diatur di Streamlit Secrets!")
        else:
            st.markdown(f"""
                <div class="user-bubble-container">
                    <div class="user-bubble">{query_to_process}</div>
                </div>
            """, unsafe_allow_html=True)

            loading_ph = st.empty()
            short_model_name = model_choice_label.split("—")[0].strip()
            loading_ph.markdown(
                get_terminal_loader_html(
                    text=f"{short_model_name} sedang berpikir",
                    token="reasoning",
                ),
                unsafe_allow_html=True,
            )

            start_time = time.time()
            try:
                res_home = client.chat.completions.create(
                    model=selected_model_id,
                    messages=[
                        {"role": "system", "content": YUKI_SYSTEM_PROMPT},
                        {"role": "user",   "content": query_to_process},
                    ],
                )
                response_text = res_home.choices[0].message.content
            except Exception as e:
                response_text = f"❌ Ups, terjadi kesalahan: {e}"

            elapsed = time.time() - start_time
            if elapsed < 1.5:
                time.sleep(1.5 - elapsed)

            loading_ph.empty()

            st.session_state["home_chat_history"].append({"role": "user", "content": query_to_process})
            st.session_state["home_chat_history"].append({"role": "assistant", "content": response_text})
            st.rerun()
    # ============================================================
    # 9. HALAMAN 2: ARENA BATTLE (MULTI AI)
    # ============================================================
    if selected_menu == "⚔️ Multi Ai":
        st.title("⚔️ Ampera Coding Arena (Multi Ai)")
        st.caption("Pilih dua model berbeda, kirim tantangan koding, dan lihat animasi loading terminal-style di kotaknya masing-masing!")

        st.markdown("<br>", unsafe_allow_html=True)
        col_sel_a, col_sel_b = st.columns(2)
        with col_sel_a:
            pilihan_a = st.selectbox(
                "🧠 Petarung A:",
                options=list(AVAILABLE_MODELS.keys()),
                index=0,
                key="pilihan_a_select",
            )
        with col_sel_b:
            pilihan_b = st.selectbox(
                "🧠 Petarung B:",
                options=list(AVAILABLE_MODELS.keys()),
                index=1,
                key="pilihan_b_select",
            )
        st.markdown("<br>", unsafe_allow_html=True)
        arena_input = st.chat_input("⚔️ Kirim tantangan duel coding...", key="arena_chat")

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
            elif pilihan_a == pilihan_b:
                st.warning("⚠️ Hei, kamu memilih dua model yang sama! Silakan ganti salah satunya.")
            else:
                col_a, col_b = st.columns(2)

                # -------- Model A --------
                with col_a:
                    st.markdown(f"""
                        <div class="arena-card">
                            <div class="arena-header">
                                <span>🔴 {pilihan_a}</span>
                                <span>🗖</span>
                            </div>
                    """, unsafe_allow_html=True)

                    loading_a = st.empty()
                    loading_a.markdown(
                        get_terminal_loader_html(
                            text=f"🔴 {pilihan_a} sedang merespons",
                            token="computing",
                        ),
                        unsafe_allow_html=True,
                    )

                    start_a = time.time()
                    try:
                        resp_a = client.chat.completions.create(
                            model=AVAILABLE_MODELS[pilihan_a],
                            messages=[
                                {"role": "system", "content": YUKI_SYSTEM_PROMPT},
                                {"role": "user",   "content": prompt_val},
                            ],
                        )
                        text_a = resp_a.choices[0].message.content
                    except Exception as e:
                        text_a = f"Error: {e}"

                    elapsed_a = time.time() - start_a
                    if elapsed_a < 4.0:
                        time.sleep(4.0 - elapsed_a)

                    loading_a.empty()
                    st.markdown(text_a)
                    st.markdown("</div>", unsafe_allow_html=True)

                # -------- Model B --------
                with col_b:
                    st.markdown(f"""
                        <div class="arena-card">
                            <div class="arena-header">
                                <span>🔵 {pilihan_b}</span>
                                <span>🗖</span>
                            </div>
                    """, unsafe_allow_html=True)

                    loading_b = st.empty()
                    loading_b.markdown(
                        get_terminal_loader_html(
                            text=f"🔵 {pilihan_b} sedang merespons",
                            token="analyzing",
                        ),
                        unsafe_allow_html=True,
                    )

                    start_b = time.time()
                    try:
                        resp_b = client.chat.completions.create(
                            model=AVAILABLE_MODELS[pilihan_b],
                            messages=[
                                {"role": "system", "content": "Kamu adalah asisten pemrograman cepat dan akurat. " + YUKI_SYSTEM_PROMPT},
                                {"role": "user",   "content": prompt_val},
                            ],
                        )
                        text_b = resp_b.choices[0].message.content
                    except Exception as e:
                        text_b = f"Error: {e}"

                    elapsed_b = time.time() - start_b
                    if elapsed_b < 4.0:
                        time.sleep(4.0 - elapsed_b)

                    loading_b.empty()
                    st.markdown(text_b)
                    st.markdown("</div>", unsafe_allow_html=True)

                # -------- Voting --------
                st.markdown("---")
                st.info("💡 **Arena Voting:** Mana model yang memberikan hasil koding lebih baik?")
                v1, v2, v3 = st.columns(3)
                with v1:
                    if st.button("👈 Pilih Petarung A", use_container_width=True, key="vote_a"):
                        st.success(f"Kamu memvoting {pilihan_a}!")
                with v2:
                    if st.button("🤝 Seri (Sama Bagus)", use_container_width=True, key="vote_draw"):
                        st.success("Terima Kasih Atas Penilaian Anda!!")
                with v3:
                    if st.button("👉 Pilih Petarung B", use_container_width=True, key="vote_b"):
                        st.success(f"Kamu memvoting {pilihan_b}!")

    # ============================================================
    # 10. HALAMAN 3: LEADERBOARD
    # ============================================================
    elif selected_menu == "📊 Leaderboard":
        st.title("📊 Ampera Leaderboard")
        st.write("Peringkat model AI berdasarkan performa koding dan voting pengguna:")
        st.markdown("""
        | Rank | Model Name | Elo Rating | Win Rate | Coding Score |
        | :---: | :--- | :---: | :---: | :---: |
        | 🥇 | **Llama 3.3 (70B)** | **1280** | 68.5% | 9.5 / 10 |
        | 🥈 | **Llama 3.1 (8B)**  | **1210** | 61.2% | 8.8 / 10 |
        """)

    # ============================================================
    # 11. HALAMAN 4: SEARCH
    # ============================================================
    elif selected_menu == "🔍 Search":
        st.title("🔍 Search")
        search_q = st.text_input("Cari topik atau riwayat (Tekan Enter)", key="search_input")
        if search_q:
            with st.spinner("Mencari..."):
                time.sleep(1)
            st.success(f"Menampilkan hasil pencarian untuk: **{search_q}**")
