import streamlit as st
import json
import os
from datetime import datetime

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Child Dashboard",
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

.child-msg{
background:#DCF8C6;
padding:12px;
border-radius:15px;
margin:10px;
text-align:right;
max-width:70%;
margin-left:auto;
}

.user-msg{
background:#F1F0F0;
padding:12px;
border-radius:15px;
margin:10px;
max-width:70%;
}

.topbar{
background:#075E54;
padding:15px;
border-radius:10px;
color:white;
margin-bottom:15px;
}

small{
color:gray;
font-size:11px;
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

child_username = st.session_state.username

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

else:

    all_messages = {}

st.session_state.messages = all_messages.get(
    child_username,
    []
)

# =========================
# HEADER
# =========================

st.markdown(f"""
<div class="topbar">
<h2>👦 Child Dashboard</h2>
<p>Logged in as: <b>{child_username}</b></p>
</div>
""", unsafe_allow_html=True)

# =========================
# CHAT DISPLAY
# =========================

for chat in st.session_state.messages:

    if not isinstance(chat, dict):
        continue

    if "user" not in chat or "message" not in chat:
        continue

    time = chat.get("time", "Just now")

    if chat["user"] == "Child":

        st.markdown(
            f"""
            <div class="child-msg">
            {chat['message']}<br>
            <small>{time}</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="user-msg">
            <b>{chat['user']}</b><br>
            {chat['message']}<br>
            <small>{time}</small>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# INPUT SECTION
# =========================

st.divider()

message_type = st.selectbox(
    "Message Type",
    [
        "Child Sending Message",
        "Incoming Message"
    ]
)

if message_type == "Incoming Message":

    sender = st.text_input("Sender Username")

else:

    sender = "Child"

message = st.text_input("Enter Message")

# =========================
# SEND BUTTON
# =========================

if st.button("Send"):

    if message.strip() != "":

        if os.path.exists("messages.json"):

            try:

                with open("messages.json", "r") as file:
                    all_messages = json.load(file)

                if not isinstance(all_messages, dict):
                    all_messages = {}

            except:
                all_messages = {}

        else:

            all_messages = {}

        if child_username not in all_messages:
            all_messages[child_username] = []

        current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        all_messages[child_username].append(
            {
                "user": sender,
                "message": message,
                "time": current_time
            }
        )

        with open("messages.json", "w") as file:
            json.dump(
                all_messages,
                file,
                indent=4
            )

        st.session_state.messages = all_messages[child_username]

        st.rerun()

# =========================
# LOGOUT
# =========================

st.write("")

if st.button("Logout"):
    st.switch_page("app.py")