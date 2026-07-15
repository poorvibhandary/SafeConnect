import streamlit as st
import json

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="SafeConnect",
    page_icon="🛡",
    layout="wide"
)

# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

[data-testid="stSidebarNav"]{
    display:none;
}

/* Background */

.stApp{
    background: linear-gradient(
    135deg,
    #0F172A,
    #1E293B,
    #334155
    );
}

/* Hero Section */

.hero{
    background: linear-gradient(
    135deg,
    #06B6D4,
    #3B82F6
    );

    padding:60px;
    border-radius:30px;
    text-align:center;
    color:white;
    margin-bottom:30px;
    box-shadow:0px 10px 25px rgba(0,0,0,0.3);
}

/* Cards */

.card{
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(10px);
    padding:35px;
    border-radius:25px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.2);
    color:white;
    min-height:220px;
}

/* Features */

.feature{
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(10px);
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    border:1px solid rgba(255,255,255,0.15);
}

/* Buttons */

.stButton > button{
    width:100%;
    height:55px;
    border:none;
    border-radius:15px;
    font-size:18px;
    font-weight:bold;
    background:linear-gradient(
    135deg,
    #06B6D4,
    #3B82F6
    );
    color:white;
}

/* Input Boxes */

.stTextInput input{
    border-radius:15px;
    padding:10px;
    background:white;
}

/* Login Container */

.login-box{
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(10px);
    padding:35px;
    border-radius:25px;
    color:white;
    border:1px solid rgba(255,255,255,0.15);
}

h1,h2,h3,h4,p,label{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# SESSION
# ==================================

if "login_type" not in st.session_state:
    st.session_state.login_type = None

# ==================================
# HOME PAGE
# ==================================

if st.session_state.login_type is None:

    st.markdown("""
    <div class="hero">

    <h1>🛡 SafeConnect</h1>

    <h3>
    AI-Powered Child Safety Monitoring Platform
    </h3>

    <p style="font-size:20px;">

    Protect children from cyberbullying,
    online predators, toxic conversations
    and suspicious activities through
    real-time AI monitoring and parental alerts.

    </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="card">

        <h2>👦 Child Portal</h2>

        <p>
        Secure messaging environment
        designed for children.
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Login as Child",
            use_container_width=True
        ):
            st.session_state.login_type = "child"
            st.rerun()

    with col2:

        st.markdown("""
        <div class="card">

        <h2>👨‍👩‍👧 Parent Portal</h2>

        <p>
        Monitor alerts and receive
        AI-generated threat notifications.
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Login as Parent",
            use_container_width=True
        ):
            st.session_state.login_type = "parent"
            st.rerun()

    st.write("")
    st.write("")

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        st.markdown("""
        <div class="feature">
        <h2>🤖</h2>
        <b>AI Detection</b>
        <p>Toxic Message Detection</p>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature">
        <h2>🚨</h2>
        <b>Threat Alerts</b>
        <p>Instant Parent Notifications</p>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature">
        <h2>💬</h2>
        <b>Live Chat</b>
        <p>WhatsApp Style Messaging</p>
        </div>
        """, unsafe_allow_html=True)

    with f4:
        st.markdown("""
        <div class="feature">
        <h2>🔒</h2>
        <b>Secure Access</b>
        <p>Role Based Authentication</p>
        </div>
        """, unsafe_allow_html=True)

# ==================================
# CHILD LOGIN
# ==================================

elif st.session_state.login_type == "child":

    st.markdown("""
    <div class="login-box">
    <h1>👦 Child Login</h1>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        with open("users.json", "r") as file:
            users = json.load(file)

        for user in users:

            if (
                user["username"] == username
                and
                user["password"] == password
                and
                user["role"] == "child"
            ):

                st.session_state.username = username

                st.switch_page(
                    "pages/child_dashboard.py"
                )

        st.error("Invalid Child Login")

    if st.button("⬅ Back"):

        st.session_state.login_type = None
        st.rerun()

# ==================================
# PARENT LOGIN
# ==================================

elif st.session_state.login_type == "parent":

    st.markdown("""
    <div class="login-box">
    <h1>👨‍👩‍👧 Parent Login</h1>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        with open("users.json", "r") as file:
            users = json.load(file)

        for user in users:

            if (
                user["username"] == username
                and
                user["password"] == password
                and
                user["role"] == "parent"
            ):

                st.session_state.username = username

                st.switch_page(
                    "pages/parent_dashboard.py"
                )

        st.error("Invalid Parent Login")

    if st.button("⬅ Back"):

        st.session_state.login_type = None
        st.rerun()