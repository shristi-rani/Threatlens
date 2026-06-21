import streamlit as st
import re
#import os
import pymongo
import pandas as pd
import pickle
#import socket
#from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from datetime import datetime
import plotly.express as px
# ---------------- DATABASE ----------------
#MONGO_URI = os.environ["mongodb+srv://shristir135_db_user:<CPkRapKdAMJLQ1OW>@cluster0.wrldbuv.mongodb.net/?appName=Cluster0"]
conn=pymongo.MongoClient("mongodb+srv://shristir135_db_user:<CPkRapKdAMJLQ1OW>@cluster0.wrldbuv.mongodb.net/?appName=Cluster0")
mydb=conn["threatlens"]
my=mydb["user"]
scan_db = mydb["scan_history"]


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ThreatLens",
    page_icon="🛡️",
    layout="wide"
)


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
try:
    with open("accuracy.txt", "r") as f:
        acc = float(f.read())
except FileNotFoundError:
    acc = 0.0



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

    # Statistics

    total_scans = scan_db.count_documents({})

    safe_count = scan_db.count_documents({
        "status": "safe"
    })

    phishing_count = scan_db.count_documents({
        "status": "phishing"
    })

    # Metrics

    col1, col2, col3 , col4 = st.columns(4)

    with col1:
        st.metric(
            "Total URLs Scanned",
            total_scans
        )

    with col2:
        st.metric(
            "Safe URLs",
            safe_count
        )

    with col3:
        st.metric(
            "Phishing URLs",
            phishing_count
        )
    with col4:
        st.metric(
            "Accuracy",
            f"{acc*100:.2f}%"
        )

    # Pie Chart

    if total_scans > 0:

        pie_data = {
            "Status": [
                "Safe",
                "Phishing"
            ],
            "Count": [
                safe_count,
                phishing_count
            ]
        }

        fig = px.pie(
            values=pie_data["Count"],
            names=pie_data["Status"],
            title="URL Risk Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "📊 No Scan Data Available Yet"
        )

    st.divider()

    # Session State

    if "scan_result" not in st.session_state:
        st.session_state.scan_result = ""

    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False

    # URL Input

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

    # Buttons

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

    # Clear

    if clear_btn:

        st.session_state.scan_result = ""

        st.session_state.clear_input = True

        st.rerun()

    # Scan

    if scan_btn:

        if url.strip() == "":

            st.warning(
                "⚠️ Please Enter URL"
            )

        else:

            input_data = vectorizer.transform(
                [url]
            )

            result = model.predict(
                input_data
            )

            prediction = result[0]
            probability = model.predict_proba(input_data)
            st.write("Prediction:", prediction)
            st.write("Probability:", probability)
            risk_score = probability[0][1] * 100
            
            if prediction == 1:

                st.session_state.scan_result = "safe"

            else:

                st.session_state.scan_result = "phishing"

            # Save History

            scan_db.insert_one({

                "url": url,

                "status":
                st.session_state.scan_result,

                "risk_score":
                float(risk_score),

                "date":
                datetime.now()

            })

            # Risk Score

            if risk_score > 80:

                st.error(
                    f"🚨 High Risk : {risk_score:.2f}%"
                )

            elif risk_score > 50:

                st.warning(
                    f"⚠️ Medium Risk : {risk_score:.2f}%"
                )

            else:

                st.success(
                    f"✅ Low Risk : {risk_score:.2f}%"
                )

    # Final Result

    if st.session_state.scan_result == "safe":

        st.success(
            "✅ Safe Website"
        )

    elif st.session_state.scan_result == "phishing":

        st.error(
            "🚨 Phishing Detected!"
        )

    st.divider()

    # Scan History

    st.subheader(
        "📋 Recent Scan History"
    )

    history = list(

        scan_db.find()

        .sort("date", -1)

        .limit(10)

    )

    if history:

        df_history = pd.DataFrame(
            history
        )

        if "_id" in df_history.columns:

            df_history.drop(
                columns=["_id"],
                inplace=True
            )

        st.dataframe(
            df_history,
            use_container_width=True
        )

    else:

        st.info(
            "No Scan History Available"
        )
                            

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
