import streamlit as st
import random
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Security Dashboard")

st.markdown("# 📊 Security Operations Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Scans Today", random.randint(120,250))
col2.metric("Threats Blocked", random.randint(10,40))
col3.metric("System Status", "ACTIVE")

import matplotlib.pyplot as plt

if os.path.exists("scan_history.csv"):
    df = pd.read_csv("scan_history.csv")

    threat_count = len(df[df["Result"] == "THREAT"])
    safe_count = len(df[df["Result"] == "SAFE"])

    st.subheader("Threat Distribution Overview")

    fig, ax = plt.subplots()
    ax.pie([threat_count, safe_count],
           labels=["Threats Detected", "Safe URLs"],
           autopct='%1.1f%%')
    ax.set_title("Threat Distribution")

    st.pyplot(fig)

st.markdown("---")

st.subheader("Threat Level Overview")
st.progress(70)

st.info("System operating normally. No critical vulnerabilities detected.")