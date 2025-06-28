import streamlit as st
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import bcrypt

# --- Configuration ---
st.set_page_config(
    page_title="PPD Risk Predictor",
    page_icon="🧠",
    layout="centered"
)

# --- Global Variables ---
USER_DATA_FILE = 'users.csv'

# Load model and label encoder
try:
    model = joblib.load('ppd_model_pipeline.pkl')
    le = joblib.load('label_encoder.pkl')
except FileNotFoundError:
    st.error("Model or label encoder not found.")
    st.stop()

# --- User Management ---
@st.cache_data
def load_users():
    try:
        return pd.read_csv(USER_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['username', 'hashed_password', 'age'])

def save_users(df):
    df.to_csv(USER_DATA_FILE, index=False)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- Login/Signup Page ---
def show_login_page():
    st.sidebar.subheader("Account Access")
    choice = st.sidebar.radio("Go to", ["Login", "Signup"], key="login_signup_radio")
    users_df = load_users()

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in users_df['username'].values:
                hashed_pw = users_df.loc[users_df['username'] == username, 'hashed_password'].iloc[0]
                if check_password(password, hashed_pw):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_age = users_df.loc[users_df['username'] == username, 'age'].iloc[0]
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Incorrect password.")
            else:
                st.error("Username not found.")

    elif choice == "Signup":
        st.subheader("Signup")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        new_age = st.slider("Your Age", 18, 45, 25)
        if st.button("Signup"):
            if not new_username or not new_password or not confirm_password:
                st.warning("All fields required.")
            elif new_username in users_df['username'].values:
                st.error("Username exists.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                new_data = pd.DataFrame([{
                    'username': new_username,
                    'hashed_password': hash_password(new_password),
                    'age': new_age
                }])
                save_users(pd.concat([users_df, new_data], ignore_index=True))
                st.success("Account created! Please login.")
                st.session_state.login_signup_radio = "Login"
                st.rerun()

# --- Session Init ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Main App ---
if st.session_state.logged_in:
    st.title("Postpartum Depression Risk Predictor 🧠")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    st.sidebar.write(f"Age: {st.session_state.user_age}")

    st.header("Your Information")
    Age = st.slider("Age", 18, 45, st.session_state.user_age)
    is_pregnant = st.selectbox("Currently pregnant?", ["Select...", "Yes", "No"], index=0)
    has_given_birth_recently = st.selectbox("Recently given birth?", ["Select...", "Yes", "No"], index=0)
    FamilySupport = st.selectbox("Family Support Level", ["Select...", "Low", "Medium", "High"], index=0)

    st.header("EPDS Questionnaire")
    Q_responses = {
        "Q1": {"As much as I always could": 0, "Not quite so much now": 1, "Definitely not so much now": 2, "Not at all": 3},
        "Q2": {"As much as I ever did": 0, "Rather less than I used to": 1, "Definitely less than I used to": 2, "Hardly at all": 3},
        "Q3": {"Yes, most of the time": 3, "Yes, some of the time": 2, "Not very often": 1, "No, never": 0},
        "Q4": {"No, not at all": 0, "Hardly ever": 1, "Yes, sometimes": 2, "Yes, very often": 3},
        "Q5": {"Yes, quite a lot": 3, "Yes, sometimes": 2, "No, not much": 1, "No, not at all": 0},
        "Q6": {"Yes, most of the time I haven't been able to cope at all": 3, "Yes, sometimes I haven't been coping as well as usual": 2,
               "No, most of the time I have coped quite well": 1, "No, I have been coping as well as ever": 0},
        "Q7": {"Yes, most of the time": 3, "Yes, sometimes": 2, "Not very often": 1, "No, not at all": 0},
        "Q8": {"Yes, most of the time": 3, "Yes, quite often": 2, "Not very often": 1, "No, not at all": 0},
        "Q9": {"Yes, most of the time": 3, "Yes, quite often": 2, "Only occasionally": 1, "No, never": 0},
        "Q10": {"Yes, quite often": 3, "Sometimes": 2, "Hardly ever": 1, "Never": 0}
    }

    q_vals = []
    for i in range(1, 11):
        key = f"Q{i}"
        answer = st.selectbox(f"Q{i}.", list(Q_responses[key].keys()))
        q_vals.append(Q_responses[key][answer])

    score = sum(q_vals)

    if st.button("Predict PPD Risk"):
        if "Select..." in [is_pregnant, has_given_birth_recently, FamilySupport]:
            st.error("Please answer all demographic questions.")
        else:
            input_data = pd.DataFrame([{
                "Age": Age,
                "FamilySupport": FamilySupport,
                "Q1": q_vals[0], "Q2": q_vals[1], "Q3": q_vals[2], "Q4": q_vals[3], "Q5": q_vals[4],
                "Q6": q_vals[5], "Q7": q_vals[6], "Q8": q_vals[7], "Q9": q_vals[8], "Q10": q_vals[9],
                "EPDS_Score": score
            }])

            try:
                pred = model.predict(input_data)[0]
                label = le.inverse_transform([pred])[0]
                colors = {"Mild": "green", "Moderate": "orange", "Severe": "red", "Profound": "darkred"}
                st.markdown(f"**Predicted Risk:** <span style='color:{colors[label]}; font-size: 24px;'>{label}</span>", unsafe_allow_html=True)

                st.write("---")
                fig, ax = plt.subplots()
                ax.bar([label], [pred], color=colors[label])
                ax.set_yticks([0, 1, 2, 3])
                ax.set_yticklabels(['Mild', 'Moderate', 'Severe', 'Profound'])
                ax.set_ylim([-0.5, 3.5])
                st.pyplot(fig)

                st.info(f"EPDS Score: **{score}** / 30")

            except Exception as e:
                st.error(f"Prediction error: {e}")

else:
    show_login_page()
