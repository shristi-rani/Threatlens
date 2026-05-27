import streamlit as st
import re
import pymongo
import pandas as pd
#import pickle
#import socket
#from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
# ---------------- DATABASE ----------------
conn=pymongo.MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.8.3")
mydb=conn["threatlens"]
my=mydb["user"]

# ---------------- LOAD MODEL ----------------
df = pd.read_csv("new_data_urls.csv")

x_train,x_test,y_train,y_test = train_test_split(
    df["url"],
    df["status"],
    test_size=0.1,
    random_state=42
)

vectorizer = TfidfVectorizer()

xv_train = vectorizer.fit_transform(x_train)

model = LogisticRegression()

model.fit(xv_train,y_train)


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ThreatLens",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "url_input" not in st.session_state:
    st.session_state.url_input = ""

# ---------------- HOME PAGE ----------------

def home():

    st.markdown("""
    # 🛡️ ThreatLens
    ### AI Powered Phishing URL Detection System
    """)

    st.image("cyber.jpeg", use_container_width=True)

    st.markdown("""
    🔍 Detect malicious websites instantly  
    🧠 AI-based threat analysis  
    🔐 Protect your cyber safety
    """)

    st.divider()

    st.info("""
    ## 📖 How to use

    1️⃣ Signup  
    2️⃣ Login  
    3️⃣ Open Dashboard  
    4️⃣ Paste URL  
    5️⃣ Click Scan
    """)

# ---------------- LOGIN PAGE ----------------
def login():

    st.markdown("## 🔐 Login")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        with st.form("SignIn"):

            t1 = st.text_input("Email")

            t2 = st.text_input(
                "Password",
                type="password"
            )

            submit = st.form_submit_button(
                "SignIn",
                use_container_width=True
            )

            if submit:

                if not t1 or not t2:

                    st.error("Fill The Fields")

                else:

                    res = my.find({
                        "email": t1,
                        "password": t2
                    })

                    v = 0

                    for data in res:

                        v = v + 1

                        st.success(
                            f"Welcome: {data['name']}"
                        )

                        st.session_state.logged_in = True

                        st.session_state.page = "dashboard"

                        st.rerun()

                    if v == 0:

                        st.error("Invalid Login Details")
# ---------------- SIGNUP PAGE ----------------

def signup():

    st.markdown("## 🆕 Signup")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        with st.form("SignupForm"):

            name = st.text_input("👤 Name")

            email = st.text_input("📧 Email")

            password = st.text_input(
                "🔒 Password",
                type="password"
            )

            submit = st.form_submit_button(
                "Signup",
                use_container_width=True
            )

            if submit:

                # VALIDATION

                if name.strip() == "":

                    st.warning("⚠️ Please enter your name")

                elif email.strip() == "":

                    st.warning("⚠️ Please enter your email")

                elif not re.match(
                    r"[^@]+@[^@]+\.[^@]+",
                    email
                ):

                    st.error("❌ Please enter valid email")

                elif password.strip() == "":

                    st.warning("⚠️ Please enter password")

                elif len(password) < 6:

                    st.error(
                        "❌ Password must be at least 6 characters"
                    )

                else:

                    # CHECK EXISTING USER

                    existing_user = my.find_one({
                        "email": email
                    })

                    if existing_user:

                        st.warning("⚠️ User already exists")

                    else:

                        # INSERT USER

                        my.insert_one({
                            "name": name,
                            "email": email,
                            "password": password
                        })

                        st.success(
                            "✅ Account created successfully"
                        )

                        st.session_state.page = "login"

                        st.rerun()




# ---------------- DASHBOARD ----------------

def dashboard():

    st.markdown("## 🚀 ThreatLens Scanner")

    # SESSION STATE

    if "scan_result" not in st.session_state:
        st.session_state.scan_result = ""

    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False

    # TEXT AREA

    if st.session_state.clear_input:

        url = st.text_area(
            "Enter URL",
            value="",
            key="new_box"
        )

        st.session_state.clear_input = False

    else:

        url = st.text_area(
            "Enter URL",
            key="main_box"
        )

    # BUTTONS

    col1, col2 = st.columns(2)

    with col1:

        scan_btn = st.button(
            "🔍 Scan",
            use_container_width=True
        )

    with col2:

        clear_btn = st.button(
            "🗑️ Clear",
            use_container_width=True
        )

    # CLEAR BUTTON

    if clear_btn:

        st.session_state.scan_result = ""

        st.session_state.clear_input = True

        st.rerun()

    # SCAN BUTTON

    if scan_btn:

        if url.strip() == "":

            st.warning("⚠️ Please Enter URL")

        else:

            input_data = vectorizer.transform([url])

            result = model.predict(input_data)

            prediction = result[0]

            st.write("Prediction =", prediction)

            # RESULT

            if prediction == 0:

                st.session_state.scan_result = "safe"

            else:

                st.session_state.scan_result = "phishing"

    # SHOW RESULT

    if st.session_state.scan_result == "safe":

        st.success("✅ Safe Website")

    elif st.session_state.scan_result == "phishing":

        st.error("🚨 Phishing Detected!")
                            

# ---------------- SIDEBAR ----------------
st.sidebar.image("logo.png", width=120)

st.sidebar.title("🛡️ ThreatLens")
# BEFORE LOGIN

if not st.session_state.logged_in:

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"

    if st.sidebar.button("🆕 Register", use_container_width=True):
        st.session_state.page = "signup"

    if st.sidebar.button("🔐 Login", use_container_width=True):
        st.session_state.page = "login"


# AFTER LOGIN

else:

     if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"

     if st.sidebar.button("🚀 Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"

     if st.sidebar.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.page = "home"

        st.success("✅ Logged out successfully")

        st.rerun()


# ---------------- ROUTING ----------------

if st.session_state.page == "home":

    home()

elif st.session_state.page == "signup":

    signup()

elif st.session_state.page == "login":

    login()

elif st.session_state.page == "dashboard":

    dashboard()
