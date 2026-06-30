# 🛡️ ThreatLens - AI Powered Phishing URL Detection System

ThreatLens is an AI-powered phishing URL detection web application that helps users identify whether a website URL is **Safe** or **Phishing** using Machine Learning.

The application is built with **Python**, **Streamlit**, **Scikit-learn**, and **MongoDB Atlas**, providing secure user authentication, scan history, profile management, and real-time phishing detection.

---

## 🚀 Features

- 🔐 User Registration & Login
- 🔒 Secure Password Hashing using bcrypt
- 👤 User Profile Management
- ✏️ Update Name
- 🔑 Change Password
- 🗑️ Delete Account
- 🚪 Logout
- 🤖 AI-Based URL Detection
- 📊 Risk Score Calculation
- 🔍 Threat Analysis
- 📈 Dashboard Statistics
- 📋 Scan History
- 🔎 Search Scan History
- 📥 Download Scan History as CSV
- ☁️ MongoDB Atlas Integration
- 🌐 Streamlit Cloud Deployment
- 🎨 Modern Responsive UI

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Scikit-learn
- Logistic Regression
- TF-IDF Vectorizer
- Pandas
- Plotly
- MongoDB Atlas
- PyMongo
- bcrypt

---

## 📂 Project Structure

```
ThreatLens/
│
├── main.py
├── new_data_urls.csv
├── logo.png
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/shristi-rani/ThreatLens.git
```

Go to project folder

```bash
cd ThreatLens
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run main.py
```

---

## 📊 Machine Learning Model

The phishing detection model uses:

- TF-IDF Vectorizer
- Logistic Regression Classifier

The model predicts whether a URL is:

- ✅ Safe
- 🚨 Phishing

It also generates a Risk Score and Threat Analysis based on URL characteristics.

---

## 🗄️ Database

MongoDB Atlas is used to store:

- User Accounts
- Encrypted Passwords
- Scan History
- User Profile Information

---

## 🔐 Security Features

- Password Hashing using bcrypt
- Secure User Authentication
- MongoDB Atlas Cloud Database
- URL Validation
- Threat Pattern Analysis

---

## 📸 Application Modules

- Home
- Register
- Login
- Dashboard
- URL Scanner
- Threat Analysis
- Scan History
- User Profile
- Password Update
- Account Management

---

## 📸 Screenshots

### 🏠 Home Page

![Home](screenshots/home.png)

---

### 🔐 Login Page

![Login](screenshots/login.png)

---

### 📝 Register Page

![Register](screenshots/register.png)

---

### 🚀 Dashboard

![Dashboard](screenshots/dashboard.png)

---

### 🔍 URL Scanner

![Scanner](screenshots/scan.png)

---

### 📋 Scan History

![History](screenshots/history.png)

---

### 👤 User Profile

![Profile](screenshots/profile.png)

## 📌 Future Improvements

- Deep Learning Based Detection
- Domain Reputation API
- WHOIS Information
- Blacklist Checking
- Browser Extension
- Email Phishing Detection
- Real-time Threat Intelligence

---

## 👩‍💻 Developer

**Shristi Rani**

Bachelor in Informatiom Technology (B.SC IT)

---

## 📄 License

This project is developed for educational and academic purposes.
