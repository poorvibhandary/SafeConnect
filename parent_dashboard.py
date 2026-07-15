import streamlit as st
import json
import os
from ai_detector import detect_toxicity

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Parent Dashboard",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

[data-testid="stSidebarNav"]{
display:none;
}

.metric-card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}

.alert-card{
background:#ffe5e5;
padding:15px;
border-radius:15px;
margin-bottom:15px;
border-left:6px solid red;
}

.topbar{
background:#075E54;
padding:20px;
border-radius:15px;
color:white;
margin-bottom:20px;
}

small{
color:gray;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN CHECK
# =========================

if "username" not in st.session_state:
    st.error("Please login first")
    st.switch_page("app.py")
    st.stop()

parent_username = st.session_state.username

# =========================
# LOAD USERS
# =========================

with open("users.json", "r") as file:
    users = json.load(file)

child_name = ""

for user in users:
    if (
        user["username"] == parent_username
        and user["role"] == "parent"
    ):
        child_name = user["child"]

# =========================
# LOAD MESSAGES
# =========================

all_messages = {}

if os.path.exists("messages.json"):

    try:
        with open("messages.json", "r") as file:
            all_messages = json.load(file)

        if not isinstance(all_messages, dict):
            all_messages = {}

    except:
        all_messages = {}

messages = all_messages.get(child_name, [])

# =========================
# HEADER
# =========================

st.markdown(f"""
<div class="topbar">
<h2>🛡 Parent Security Center</h2>
<p>Monitoring Child : <b>{child_name}</b></p>
</div>
""", unsafe_allow_html=True)

# =========================
# THREAT DETECTION
# =========================

threats = 0
suspicious_users = set()

cyberbullying = 0
grooming = 0
toxic_language = 0

for chat in messages:

    if not isinstance(chat, dict):
        continue

    message = chat.get("message", "")
    sender = chat.get("user", "")

    label, score, category = detect_toxicity(message)

    if label.lower() == "toxic":

        threats += 1
        suspicious_users.add(sender)

        if "Cyberbullying" in category:
            cyberbullying += 1

        elif "Grooming" in category:
            grooming += 1

        elif "Toxic" in category:
            toxic_language += 1

# =========================
# RISK LEVEL
# =========================

if threats == 0:
    risk = "🟢 LOW"

elif threats <= 2:
    risk = "🟡 MEDIUM"

else:
    risk = "🔴 HIGH"

# =========================
# METRICS
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Threats Detected",
        threats
    )

with col2:
    st.metric(
        "Suspicious Users",
        len(suspicious_users)
    )

with col3:
    st.metric(
        "Risk Level",
        risk
    )

# =========================
# THREAT SUMMARY
# =========================

st.divider()

st.subheader("📊 Threat Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🚫 Cyberbullying", cyberbullying)

with c2:
    st.metric("👤 Online Grooming", grooming)

with c3:
    st.metric("⚠ Toxic Language", toxic_language)

# =========================
# =========================
# ALERTS
# =========================

st.divider()

st.subheader("🚨 AI Detected Alerts")

alert_found = False

for chat in messages:

    if not isinstance(chat, dict):
        continue

    message = chat.get("message", "")
    sender = chat.get("user", "")
    time = chat.get("time", "Unknown")

    label, score, category = detect_toxicity(message)

    if label.lower() == "toxic":

        alert_found = True

               # =========================
        # Severity
        # =========================

        if score >= 0.90:
            severity = "🔴 Critical"
        elif score >= 0.70:
            severity = "🟠 High"
        else:
            severity = "🟡 Medium"

        # =========================
        # Recommendation
        # =========================

        if "Cyberbullying" in category:

            recommendation = [
                "Talk calmly with your child.",
                "Block or report the abusive user.",
                "Save screenshots as evidence.",
                "Inform the school if bullying continues."
            ]

        elif "Online Grooming" in category:

            recommendation = [
                "Do not reply to the sender.",
                "Block the suspicious account immediately.",
                "Never share personal information or photos.",
                "Inform parents or the cybercrime authorities."
            ]

        elif "Toxic Language" in category:

            recommendation = [
                "Monitor future conversations.",
                "Discuss respectful communication.",
                "Encourage positive online behaviour."
            ]

        else:

            recommendation = [
                "Review the conversation carefully."
            ]

        # =========================
        # Alert Card
        # =========================

        with st.container(border=True):

            st.markdown(f"### 🚨 {category}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**👤 User:** {sender}")

            with col2:
                st.markdown(f"**🕒 Time:** {time}")

            st.markdown(f"**🔥 Severity:** {severity}")

            st.progress(score)

            st.markdown(f"**🤖 AI Confidence:** {round(score*100,2)}%")

            st.markdown("**💬 Suspicious Message**")

            st.error(message)

            st.markdown("**✅ Recommended Action**")

            for tip in recommendation:
                st.markdown(f"- {tip}")
if not alert_found:
    st.success("✅ No suspicious messages detected.")

# =========================
# PRIVACY
# =========================

st.divider()

st.info(
    "🔒 Only AI-flagged suspicious messages are visible to parents. Normal conversations remain private."
)

# =========================
# REFRESH
# =========================

if st.button("🔄 Refresh"):
    st.rerun()

# =========================
# LOGOUT
# =========================

st.write("")

if st.button("Logout"):
    st.switch_page("app.py")