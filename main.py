import streamlit as st
import re
import pymongo
import pandas as pd
import pickle
import bcrypt
import socket
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
conn=pymongo.MongoClient("mongodb+srv://shristir135_db_user:CPkRapKdAMJLQ1OW@cluster0.wrldbuv.mongodb.net/threatlens?retryWrites=true&w=majority&appName=Cluster0")
mydb=conn["threatlens"]
my=mydb["user"]
scan_db = mydb["scan_history"]


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ThreatLens",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main app background */
.stApp {
    background: linear-gradient(to right, #f4f9ff, #eef5ff);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: bold;
    height: 45px;
    background-color: #2563eb;
    color: white;
    border: none;
}
.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

/* Text Input & TextArea */
.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dbe4f0;
}

</style>
""", unsafe_allow_html=True)



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
<div style="
padding:20px;
border-radius:12px;
background:linear-gradient(to right,#2563eb,#06b6d4);
text-align:center;
color:white;
">
<h1>🛡️ ThreatLens</h1>
<h4>AI-Powered Phishing URL Detection System</h4>
<p>Protect yourself from malicious websites with intelligent URL scanning.</p>
🔍 Detect malicious websites instantly    🔐 Protect your cyber safety
</div>
    """,unsafe_allow_html=True)

    st.divider()

    


    

    st.image("cyber.jpeg", use_container_width=True)
    st.divider()
    
    st.info(
        "🛡️ ThreatLens uses Machine Learning to identify potentially malicious URLs. "
        "Always verify suspicious links before opening them."
    )

    st.info("""
    ## 📖 How to use

    1️⃣ Signup  
    2️⃣ Login  
    3️⃣ Open Dashboard  
    4️⃣ Paste URL  
    5️⃣ Click Scan
    """)
    st.markdown("---")
    st.caption(
        "🛡️ ThreatLens | Built with Streamlit, Machine Learning & MongoDB"
    )

# ---------------- LOGIN PAGE ----------------
def login():
    #st.markdown("## 🔐 Login")

    st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background:linear-gradient(to right,#4f46e5,#06b6d4);
color:white;
text-align:center;
">
<h2>👤 Login Your Account </h2>

</div>
""", unsafe_allow_html=True)

    st.divider()
    

    
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
                t1 = t1.strip().lower()

                if not t1 or not t2:

                    st.error("Fill The Fields")

                else:

                    user = my.find_one({"email": t1})
                    #st.write("Email entered:", repr(t1))
                    #st.write("User found:", user)
                    if user is None:
                        st.error("❌ User not found. Check your email.")
                    else:
                        stored_password = user["password"]
                        if stored_password.startswith("$2b$"):
                            #st.write("Stored password:", user["password"])
                            if bcrypt.checkpw(
                                t2.encode("utf-8"),
                                user["password"].encode("utf-8")
                            ):
                                st.success(f"Welcome: {user['name']}")
                                st.session_state.logged_in = True
                                st.session_state["user_email"] = t1
                                st.session_state["user_name"] = user["name"]
                                st.session_state.page = "dashboard"
                                st.rerun()
                            else:
                                st.error("Invalid Login Details")
                        else:
                            st.error(
                                "⚠️ This account uses an old password format. ""Please create a new account or update the stored password."
                            )
    st.markdown("---")
    st.caption(
        "🛡️ ThreatLens | Built with Streamlit, Machine Learning & MongoDB"
    )
                    
# ---------------- SIGNUP PAGE ----------------

def signup():
    #st.markdown("## 🆕 Signup")
    st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background:linear-gradient(to right,#4f46e5,#06b6d4);
color:white;
text-align:center;
">
<h2>👤 Register  </h2>
<p>SignUp first for searching URL.</p>
</div>
""", unsafe_allow_html=True)
    

    st.divider()

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        with st.form("SignupForm"):

            name = st.text_input("👤 Name")

            email = st.text_input("📧 Email")
            email = email.strip().lower()

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
                elif not re.search(r"[A-Z]", password):
                    st.error("Password must contain one uppercase letter.")
                elif not re.search(r"[a-z]", password):
                    st.error("Password must contain one lowercase letter.")
                elif not re.search(r"[0-9]", password):
                    st.error("Password must contain one number.")

                else:

                    # CHECK EXISTING USER

                    existing_user = my.find_one({
                        "email": email
                    })

                    if existing_user:

                        st.warning("⚠️ User already exists")

                    else:

                        # INSERT USER
                        hashed_password = bcrypt.hashpw(
                            password.encode("utf-8"),
                            bcrypt.gensalt()
                        ).decode("utf-8")

                        my.insert_one({
                            "name": name,
                            "email": email,
                            "password": hashed_password
                        })

                        st.success(
                            "✅ Account created successfully"
                        )

                        st.session_state.page = "login"
                        st.rerun()
    st.markdown("---")
    st.caption(
        "🛡️ ThreatLens | Built with Streamlit, Machine Learning & MongoDB"
    )
                


# ---------------- DASHBOARD ----------------

def dashboard():

    st.markdown("""
<div style="
padding:20px;
border-radius:12px;
background:linear-gradient(to right,#2563eb,#06b6d4);
text-align:center;
color:white;
">
<h1>🛡️Dashboard </h1>

<p>Protect yourself from malicious websites with intelligent URL scanning.</p>
</div>
""", unsafe_allow_html=True)
    st.divider()
    trusted_domains = {
        "google.com",
        "youtube.com",
        "facebook.com",
        "instagram.com",
        "whatsapp.com",
        "web.whatsapp.com",
        "chatgpt.com",
        "openai.com",
        "github.com",
        "linkedin.com",
        "amazon.com"
        "mongodb.com",
    }

    st.info(
        "🛡️ ThreatLens uses Machine Learning to identify potentially malicious URLs. "
        "Always verify suspicious links before opening them."
    )
    
    # Statistics

    total_scans = scan_db.count_documents({
        "user_email": st.session_state.get("user_email")
    })

    safe_count = scan_db.count_documents({
        "user_email": st.session_state.get("user_email"),
        "status": "safe"
    })

    phishing_count = scan_db.count_documents({
        "user_email": st.session_state.get("user_email"),
        "status": "phishing"
    })
# Metrics

    safe_rate = 0
    if total_scans > 0:
        safe_rate = (safe_count / total_scans) * 100
    

    col1, col2, col3 , col4 ,col5 = st.columns(5)

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
    with col5:
        st.metric(
            "🛡️ Safe Rate",
            f"{safe_rate:.1f}%"
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
        fig.update_traces(
            textinfo="percent+label"
        )
        fig.update_layout(
            title_x=0.3
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
    st.subheader("🔍 Scan a Website")
    st.caption("Paste any URL below and ThreatLens will analyze whether it is safe or potentially phishing.")

    # Session State

    if "scan_result" not in st.session_state:
        st.session_state.scan_result = ""

    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False

    # URL Input

    if st.session_state.clear_input:
        url = st.text_area(
            "🌐 Enter Website URL",
            value="",
            key="new_box",
            placeholder="https://example.com",
            height=100
            )
        st.session_state.clear_input = False

    else:
        url = st.text_area(
            "🌐 Enter Website URL",
            key="main_box",
            placeholder="https://example.com",
            height=100
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
            st.warning("⚠️ Please Enter URL")
            st.stop()
        # URL validation
        if not re.match(
            r"^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}",
            url
        ):
            st.error("❌ Invalid Website URL")
            st.stop()
        # Protocol add
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        with st.spinner("🔍 Scanning URL... Please wait"):
            domain = (
                url.replace("https://", "")
                .replace("http://", "")
                .split("/")[0]
                .lower()
            )
            # Trusted domains
            if domain in trusted_domains:
                st.session_state.scan_result = "safe"
                risk_score = 0
            else:
                input_data = vectorizer.transform([url])
                prediction = model.predict(input_data)[0]
                probability = model.predict_proba(input_data)
                #st.write("Prediction =", prediction)
                #st.write("Classes =", model.classes_)
                #st.write("Probability =", probability)
                # IMPORTANT
                #phishing_probability = probability[0][0]
                #risk_score = phishing_probability * 100
                phishing_index = list(model.classes_).index(0)
                risk_score = probability[0][phishing_index] * 100
                if prediction == 1:
                    status = "safe"
                else:
                    status = "phishing"
                st.session_state.scan_result = status
        # Save history for BOTH safe and phishing
        scan_db.insert_one({
            "user_email": st.session_state.get("user_email"),
            "url": url,
            "status": st.session_state.scan_result,
            "risk_score": float(risk_score),
            "date": datetime.now()
        })
        # Risk Display
        if risk_score > 80:
            st.error(f"🚨 High Risk : {risk_score:.2f}%")
        elif risk_score > 50:
            st.warning(f"⚠️ Medium Risk : {risk_score:.2f}%")
        else:
            st.success(f"✅ Low Risk : {risk_score:.2f}%")
        st.metric(
            "🎯 Risk Score",
            f"{risk_score:.2f}%"
        )
        st.progress(
            min(int(risk_score), 100)
        )
        # Threat Analysis
        st.subheader("🔍 Threat Analysis")
        reasons = []
        if "login" in url.lower():
            reasons.append("⚠️ URL contains 'login'")
        if "verify" in url.lower():
            reasons.append("⚠️ URL contains 'verify'")
        if "update" in url.lower():
            reasons.append("⚠️ URL contains 'update'")
        if "secure" in url.lower():
            reasons.append("⚠️ URL contains 'secure'")
        if "bank" in url.lower():
            reasons.append("⚠️ URL contains 'bank'")
        if "@" in url:
            reasons.append("⚠️ URL contains '@'")
        if len(url) > 75:
            reasons.append("⚠️ URL is unusually long")
        if url.count("-") > 3:
            reasons.append("⚠️ Too many hyphens")
        if url.startswith("http://"):
            reasons.append("⚠️ Website is not using HTTPS")
        if url.count(".") > 4:
            reasons.append("⚠️ Too many subdomains")
        if reasons:
            for reason in reasons:
                st.warning(reason)
        else:
            st.success(
                "✅ No obvious suspicious URL patterns detected."
            )

    st.divider()


    # Final Result
    st.subheader("📢 Scan Result")
    if st.session_state.scan_result == "safe":
        st.success(
            "✅ **Status: SAFE**\n\n"
            "No obvious phishing indicators were detected by the model."
        )
    elif st.session_state.scan_result == "phishing":
        st.error(
            "🚨 **Status: PHISHING**\n\n"
            "This URL appears suspicious. Avoid entering personal or financial information."
        )
    if st.button("🗑️ Clear My Scan History", use_container_width=True):
        scan_db.delete_many({
            "user_email": st.session_state.get("user_email")
        })
        st.success("✅ Your scan history has been cleared.")
        st.rerun()


    st.divider()



    # Scan History
    
    st.subheader("📋 Recent Scan History")
    st.caption("Showing the latest 10 scanned URLs.")
    history = list(
        scan_db.find({
            "user_email": st.session_state.get("user_email")
        })
        .sort("date", -1)
        .limit(10)
    )
    st.caption(
        f"📌 Total scans in your history: {total_scans}"
    )
    if history:
        df_history = pd.DataFrame(history)
        if "_id" in df_history.columns:
            df_history.drop(columns=["_id"], inplace=True)
        if "date" in df_history.columns:
            df_history["date"] = pd.to_datetime(
                df_history["date"]
            ).dt.strftime("%d-%m-%Y %H:%M")
        if "status" in df_history.columns:
            df_history["status"] = df_history["status"].replace({
                "safe": "🟢 Safe",
                "phishing": "🔴 Phishing"
            })
        #search
        search_query = st.text_input(
            "🔍 Search in Scan History",
            placeholder="Type part of a URL...",
            key="history_search"
        )
        if search_query:
            df_history = df_history[
                df_history["url"].str.contains(
                    search_query,
                    case=False,
                    na=False
                )
            ]
            if df_history.empty:
                st.warning("No matching URLs found.")
        #cvs
        csv_data = df_history.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Scan History (CSV)",
            data=csv_data,
            file_name="threatlens_scan_history.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.dataframe(
            df_history,
            use_container_width=True
        )
    else:
        st.info("No Scan History Available")



    st.markdown("---")
    st.caption(
        "🛡️ ThreatLens | Built with Streamlit, Machine Learning & MongoDB"
        )

#-------profile-------

def profile():

    #st.title("👤 My Profile")

    #st.write("### Your Details")
    st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background:linear-gradient(to right,#4f46e5,#06b6d4);
color:white;
text-align:center;
">
<h2>👤 My Profile</h2>
<p>Manage your account settings securely.</p>
</div>
""", unsafe_allow_html=True)


    

    #st.write("👤 Name:", st.session_state.get("user_name", "User"))

    #st.write("📧 Email:", st.session_state.get("user_email", "Not Available"))

    st.markdown("### 📋 Account Information")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"👤 **Name**\n\n{st.session_state.get('user_name')}")
    with col2:
        st.info(f"📧 **Email**\n\n{st.session_state.get('user_email')}")



    st.divider()
    st.info("✏️ Your display name will be updated across your account.")
    st.subheader("✏️ Update Name")
    new_name = st.text_input(
        "Enter New Name",
        value=st.session_state.get("user_name", ""),
        placeholder="Enter your new name"
        #key="update_name"
    )
    if st.button("💾 Save Name"):
        if new_name.strip() == "":
            st.error("❌ Name cannot be empty.")
        elif new_name == st.session_state["user_name"]:
            st.warning("⚠️ You entered the same name.")
        else:
            st.session_state["confirm_name"] = True
    if st.session_state.get("confirm_name", False):
        st.warning(f"Are you sure you want to change your name to **{new_name}** ?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Update Name", use_container_width=True):
                my.update_one(
                    {"email": st.session_state["user_email"]},
                    {"$set": {"name": new_name}}
                )
                st.session_state["user_name"] = new_name
                st.session_state["confirm_name"] = False
                st.success("✅ Name updated successfully!")
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state["confirm_name"] = False
                st.rerun()



    st.divider()
    #st.subheader("🔒 Change Password")
    st.markdown("### 🔐 Security")
    st.caption("Update your account password securely.")
    current_password = st.text_input(
        "Current Password",
        type="password",
        key="current_pwd"
    )
    new_password = st.text_input(
        "New Password",
        type="password",
        key="new_pwd"
    )
    confirm_password = st.text_input(
        "Confirm New Password",
        type="password",
        key="confirm_pwd"
    )
    if st.button("🔄 Update Password"):
        user = my.find_one({
            "email": st.session_state["user_email"]
        })
        if not bcrypt.checkpw(
            current_password.encode("utf-8"),
            user["password"].encode("utf-8")
        ):
            st.error("❌ Current password is incorrect.")
        elif new_password != confirm_password:
            st.error("❌ New passwords do not match.")
        elif len(new_password) < 6:
            st.error("❌ Password must be at least 6 characters.")
        else:
            hashed_password = bcrypt.hashpw(
                new_password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")
            my.update_one(
                {"email": st.session_state["user_email"]},
                {"$set": {"password": hashed_password}}
            )
            st.success("✅ Password updated successfully!")



    st.divider()
    #st.subheader("📊 My Statistics")
    st.markdown("### 📊 Your Statistics")
    total_scans = scan_db.count_documents({
        "user_email": st.session_state.get("user_email")
    })
    safe_count = scan_db.count_documents({
        "user_email": st.session_state.get("user_email"),
        "status": "safe"
    })
    phishing_count = scan_db.count_documents({
        "user_email": st.session_state.get("user_email"),
        "status": "phishing"
    })
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔍Total Scans", total_scans)
    with col2:
        st.metric("✅Safe URLs", safe_count)
    with col3:
        st.metric("🚨Phishing URLs", phishing_count)

    st.divider()
    #st.markdown("## 🚨 Danger Zone")


    #st.error("🚨 Permanent Action")
    st.caption("Once deleted, your account cannot be recovered.")
    

    
    if st.button("🗑️ Delete My Account", use_container_width=True):
        st.session_state["confirm_delete"] = True
    if st.session_state.get("confirm_delete", False):
        st.write("""⚠️ Deleting your account will permanently remove:\n\n
           Your account
           Your scan history
           Your saved data
        """)
        st.write("Are you sure you want to permanently delete your account?""")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete",use_container_width=True):
                my.delete_one({
                    "email": st.session_state["user_email"]
                })
                scan_db.delete_many({
                    "user_email": st.session_state["user_email"]
                })
                st.session_state.clear()
                st.success("✅ Account deleted successfully.")
                st.rerun()
        with col2:
            if st.button("❌ Keep My Account ",use_container_width=True):
                st.session_state["confirm_delete"] = False
                st.rerun()
    


    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown("---")
    st.caption(
        "🛡️ ThreatLens | Built with Streamlit, Machine Learning & MongoDB"
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

    st.sidebar.success(f"👋 {st.session_state.get('user_name', 'User')}")

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"

    if st.sidebar.button("🚀 Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"

    if st.sidebar.button("👤 Profile", use_container_width=True):
        st.session_state.page = "profile"

    if st.sidebar.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.page = "home"

        st.session_state.pop("user_email", None)
        st.session_state.pop("user_name", None)

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

elif st.session_state.page == "profile":
    profile()
