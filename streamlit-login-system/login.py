import streamlit as st
import sqlite3
import hashlib
import re

st.set_page_config(page_title="Pro Login System", page_icon="🔐", layout="centered")

# -------------------- DB SETUP --------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# -------------------- FUNCTIONS --------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def is_strong_password(password):
    # Minimum 6 chars + at least 1 number + 1 letter
    if len(password) < 6:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True

def create_user(fullname, email, username, password):
    try:
        cursor.execute(
            "INSERT INTO users (fullname, email, username, password) VALUES (?, ?, ?, ?)",
            (fullname, email, username, hash_password(password))
        )
        conn.commit()
        return True, "Account created successfully ✅"
    except sqlite3.IntegrityError:
        return False, "Username or Email already exists ❌"

def login_user(username, password):
    cursor.execute("SELECT fullname, email, username FROM users WHERE username=? AND password=?",
                   (username, hash_password(password)))
    return cursor.fetchone()

# -------------------- SESSION --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_data" not in st.session_state:
    st.session_state.user_data = None

# -------------------- STYLING (COOL UI) --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}
.main {
    background: transparent;
}
.card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}
.subtitle {
    text-align: center;
    font-size: 15px;
    color: rgba(255,255,255,0.7);
    margin-bottom: 25px;
}
.stTextInput label, .stCheckbox label {
    color: rgba(255,255,255,0.85) !important;
}
.stTextInput input {
    border-radius: 12px !important;
    padding: 12px !important;
}
.stButton button {
    width: 100%;
    border-radius: 12px;
    padding: 12px;
    font-weight: 700;
    background: linear-gradient(90deg, #6366f1, #a855f7);
    color: white;
    border: none;
}
.stButton button:hover {
    opacity: 0.92;
    transform: scale(1.01);
}
.smalltext {
    text-align:center;
    color: rgba(255,255,255,0.65);
    font-size: 13px;
}
hr {
    border: 0;
    height: 1px;
    background: rgba(255,255,255,0.15);
    margin: 18px 0px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- UI --------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='title'>🔐 Secure Login</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Professional Login + Signup System (Streamlit + SQLite)</div>", unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------
if st.session_state.logged_in:
    fullname, email, username = st.session_state.user_data

    st.success(f"✅ Welcome back, {fullname}!")
    st.write("### 📌 Dashboard")
    st.info(f"👤 Username: `{username}`")
    st.info(f"📧 Email: `{email}`")

    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.rerun()

    with col2:
        st.button("⚙️ Settings (Demo)")

else:
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Signup"])

    # -------------------- LOGIN TAB --------------------
    with tab1:
        show_pass = st.checkbox("Show Password")
        password_type = "default" if show_pass else "password"

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type=password_type, placeholder="Enter your password")
            remember = st.checkbox("Remember Me")
            login_btn = st.form_submit_button("Login")

        if login_btn:
            if username.strip() == "" or password.strip() == "":
                st.error("❌ Please fill all fields")
            else:
                user = login_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

        st.markdown("<p class='smalltext'>Tip: Create a new account from Signup tab 👇</p>", unsafe_allow_html=True)

    # -------------------- SIGNUP TAB --------------------
    with tab2:
        with st.form("signup_form"):
            fullname = st.text_input("Full Name", placeholder="Enter full name")
            email = st.text_input("Email", placeholder="example@gmail.com")
            new_username = st.text_input("Username", placeholder="Create a username")
            new_password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            signup_btn = st.form_submit_button("Create Account")

        if signup_btn:
            if fullname.strip() == "" or email.strip() == "" or new_username.strip() == "" or new_password.strip() == "":
                st.error("❌ Please fill all fields")
            elif not is_valid_email(email):
                st.error("❌ Enter a valid email")
            elif not is_strong_password(new_password):
                st.error("❌ Password must be 6+ characters and include letters + numbers")
            elif new_password != confirm_password:
                st.error("❌ Passwords do not match")
            else:
                ok, msg = create_user(fullname, email, new_username, new_password)
                if ok:
                    st.success(msg)
                    st.info("Now go to Login tab and login 🔥")
                else:
                    st.error(msg)

st.markdown("</div>", unsafe_allow_html=True)
