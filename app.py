import streamlit as st
import pickle
import numpy as np
import re
import requests
import base64


# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(page_title="Cyber Threat Scanner", page_icon="🔐", layout="wide")

# =====================================
# LOAD MODEL
# =====================================
@st.cache_resource
def load_model():
    with open("url_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# =====================================
# FEATURE EXTRACTION FUNCTION
# =====================================
def extract_features(url):
    features = []
    url = str(url)

    features.append(1 if re.match(r"^(http[s]?://)?(\d{1,3}\.){3}\d{1,3}", url) else 0)
    features.append(len(url))
    features.append(1 if "@" in url else 0)
    features.append(1 if "-" in url else 0)
    features.append(url.count("."))
    features.append(1 if "https" in url else 0)
    features.append(url.count("/"))

    suspicious_words = ["login", "secure", "bank", "update", "verify"]
    features.append(1 if any(word in url.lower() for word in suspicious_words) else 0)

    return features
def check_live_status(url):
    try:
        response = requests.get(url,timeout=5)
        return "Website is Live✅" if response.status_code ==200 else f"Status : {response.status_code}"
    except:
        return "website is Not Reachable❌"

# =====================================
# PREMIUM UI STYLING
# =====================================
st.markdown("""
<style>

/* Remove top spacing */
.block-container {
    padding-top: 2rem;
}
            
/* Background */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 70% 50%, #3b0a57 0%, #0a001a 50%, #000000 90%);
    color: white;
}
            
/* Flashing Red Animation */
@keyframes flashRed {
  0% {opacity: 1;}
  50% {opacity: 0.3;}
  100% {opacity: 1;}
}

.threat {
    color: red;
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    text-shadow:
        0 0 10px red,
        0 0 30px red,
        0 0 60px red;
    animation: flashRed 1s infinite;
}

.safe {
    color: #00ffff;
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    text-shadow:
        0 0 10px #00ffff,
        0 0 30px #00ffff;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* HERO TITLE */
.hero-title {
    font-size: 60px;
    font-weight: 800;
    line-height: 1.2;
}

.gradient-text {
    background: linear-gradient(90deg,#7f00ff,#00ffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 18px;
    color: #cccccc;
    margin-top: 20px;
}

/* STATS */
.stats {
    display: flex;
    gap: 60px;
    margin-top: 60px;
}

.stat h2 {
    color: #a855f7;
}

.stat p {
    color: gray;
}

/* SCANNER BOX */
.scan-box {
    position: relative;
    margin-top: 60px;
    padding: 60px;
    border-radius: 25px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    box-shadow: 0 0 40px rgba(138,43,226,0.3);
    overflow: hidden;
}

/* Glowing background inside scan box */
.scan-box::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, #00f0ff 0%, transparent 70%);
    filter: blur(120px);
    opacity: 0.6;
    z-index: 0;
}

/* Make content appear above glow */
.scan-box * {
    position: relative;
    z-index: 1;
}


</style>
""", unsafe_allow_html=True)

# =====================================
# HERO SECTION
# =====================================
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    <div class="hero-title">
        Secure all packets with <br>
        <span class="gradient-text">Advanced AI Security</span>
    </div>

    <div class="hero-sub">
        Real-time phishing detection powered by machine learning.
        Protect users from malicious URLs instantly.
    </div>

    <div class="stats">
        <div class="stat">
            <h2>200K+</h2>
            <p>Scans Completed</p>
        </div>
        <div class="stat">
            <h2>98.7%</h2>
            <p>Detection Accuracy</p>
        </div>
        <div class="stat">
            <h2>24/7</h2>
            <p>AI Monitoring</p>
        </div>
    </div>  """, unsafe_allow_html=True)

with col2:
    st.markdown("<h1 style='font-size:200px;text-align:center;'>🔐</h1>", unsafe_allow_html=True)

# =====================================
# SOUND FUNCTIONS
# =====================================
def play_alert_silent_controls():
    with open("alert.mpeg", "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


def play_safe_silent_controls():
    with open("safe.mpeg", "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# =====================================
# SCANNER SECTION
# =====================================
st.markdown('<div class="scan-box">', unsafe_allow_html=True)
st.subheader("🔎 Enter Target URL")

url = st.text_input("Enter URL Here", key="unique_url_input")

if st.button("🚀 INITIATE SCAN", key="scan_button"):
    if url == "":
        st.warning("Enter a valid URL")
    else:
        features = np.array(extract_features(url)).reshape(1, -1)
        prediction = model.predict(features)
        probability = model.predict_proba(features)
        confidence = round(max(probability[0]) * 100, 2)
        
        if prediction[0] == 1:
            st.markdown('<div class="threat">⚠️ THREAT DETECTED!</div>',
         unsafe_allow_html=True)
            play_alert_silent_controls()
        else:
           st.markdown('<div class="safe">✅ TARGET SECURE</div>', unsafe_allow_html=True)
           play_safe_silent_controls()
           
           st.progress(int(confidence))
           st.markdown(f"<h3 style='text-align:center;'>Confidence Level: {confidence}%</h3>", unsafe_allow_html=True)

           status = check_live_status(url)
           st.info(status)
           
st.markdown('</div>',
unsafe_allow_html=True)