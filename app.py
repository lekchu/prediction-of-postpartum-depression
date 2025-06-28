import streamlit as st
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import bcrypt

# --- Configuration (This should be the FIRST Streamlit command) ---
st.set_page_config(
    page_title="PPD Risk Predictor",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for enhanced aesthetics (BLUE SHADES) ---
st.markdown("""
<style>
    /* Main app background - Very light blue */
    .reportview-container {
        background: #e3f2fd; /* Lightest blue (e.g., from Material Design Blue 50) */
    }
    .main .block-container {
        padding-top: 2rem; /* Reduce top padding */
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    /* Sidebar background - Slightly deeper light blue */
    .st-emotion-cache-1wvz7m { /* Streamlit's auto-generated class for sidebar background */
        background-color: #bbdefb; /* Light blue (e.g., Material Design Blue 100) */
    }
    .sidebar .sidebar-content {
        background-color: #bbdefb; /* Ensure compatibility for older versions/different setups */
    }
    h1 {
        color: #1565c0; /* Darker blue for main title for good contrast */
        text-align: center;
    }
    h2, h3, h4, h5, h6 {
        color: #2196f3; /* Medium blue for other headers */
    }
    .css-10jb6m0 { /* Card-like background for main content - keep it white for contrast */
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green button - can change to blue if preferred, e.g., #2196f3 */
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #45a049; /* Darker green on hover */
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #90caf9; /* Light blue border for inputs */
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #90caf9; /* Light blue border for selectboxes */
    }
</style>
""", unsafe_allow_html=True)


# --- Global Variables / Model Loading ---
# User data file
USER_DATA_FILE = 'users.csv'

# Load trained model and label encoder
try:
    model = joblib.load('ppd_model_pipeline.pkl')
    le = joblib.load('label_encoder.pkl')
except FileNotFoundError:
    st.error("Error: Model or label encoder files not found. Please ensure 'ppd_model_pipeline.pkl' and 'label_encoder.pkl' are in the same directory.")
    st.stop() # This stops the app if the files aren't there, so it doesn't crash later

# --- Functions for User Management ---

# Function to load user data from CSV
@st.cache_data # Cache this function so it doesn't re-read the file every time
def load_users():
    try:
        users_df = pd.read_csv(USER_DATA_FILE)
        return users_df
    except FileNotFoundError:
        # Create an empty DataFrame if file doesn't exist
        return pd.DataFrame(columns=['username', 'hashed_password', 'age'])

# Function to save user data to CSV
def save_users(df):
    df.to_csv(USER_DATA_FILE, index=False)

# Hash password
def hash_password(password):
    # Generates a salt and hashes the password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Check password
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- Login/Signup Page Functions ---
def show_login_page():
    st.sidebar.subheader("Account Access 🔑")
    choice = st.sidebar.radio("Go to", ["Login", "Signup"], key="login_signup_radio")

    users_df = load_users()

    # Add an image or graphic to the login/signup page
    # IMPORTANT: Ensure 'ppd_banner.png' is in your GitHub repo in the same folder as app.py
    # Or replace with a direct URL to an image if hosted elsewhere.
    st.image("ppd_banner.png", use_column_width=True, caption="Welcome to PPD Risk Predictor")

    if choice == "Login":
        st.subheader("Login to Your Account 🚀")
        username = st.text_input("Username 👇")
        password = st.text_input("Password 🔒", type="password")

        if st.button("Login"):
            if username in users_df['username'].values:
                stored_hashed_password = users_df[users_df['username'] == username]['hashed_password'].iloc[0]
                if check_password(password, stored_hashed_password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['user_age'] = users_df[users_df['username'] == username]['age'].iloc[0] # Store user's age
                    st.success(f"Welcome, {username}! 🎉")
                    st.rerun() # Rerun to switch to the main app
                else:
                    st.error("Incorrect password. 🚫")
            else:
                st.error("Username not found. 🤔")

    elif choice == "Signup":
        st.subheader("Create a New Account ✨")
        new_username = st.text_input("Choose a Username 👇")
        new_password = st.text_input("Create a Password 🔒", type="password")
        confirm_password = st.text_input("Confirm Password 🔒", type="password")
        new_age = st.slider("Your Age 🎂", 18, 45, 25) # User can select age during signup

        if st.button("Signup"):
            if not new_username or not new_password or not confirm_password:
                st.warning("All fields are required. ⚠️")
            elif new_username in users_df['username'].values:
                st.error("Username already exists. Please choose a different one. ❌")
            elif new_password != confirm_password:
                st.error("Passwords do not match. 🚫")
            else:
                hashed_pw = hash_password(new_password)
                new_user_data = pd.DataFrame([{'username': new_username, 'hashed_password': hashed_pw, 'age': new_age}])
                updated_users_df = pd.concat([users_df, new_user_data], ignore_index=True)
                save_users(updated_users_df)
                st.success("Account created successfully! Please login. ✅")
                st.session_state['login_signup_radio'] = "Login"
                st.rerun()


# --- Main Application Logic (Conditional Display) ---

# Initialize session state for login status if not already set
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    # --- Start of your main app.py content that shows when logged in ---

    st.title("Postpartum Depression Risk Predictor 🧠")

    # --- Logout button (in sidebar for convenience) ---
    if st.sidebar.button("Logout 🚪"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['user_age'] = None # Clear stored age on logout
        st.rerun()

    st.sidebar.markdown(f"Logged in as: **{st.session_state['username']}** 👋")
    st.sidebar.markdown(f"Age: **{st.session_state['user_age']}**")

    # Add a graphic to the main page
    # IMPORTANT: Ensure 'health_graphic.png' is in your GitHub repo in the same folder as app.py
    st.image("health_graphic.png", use_column_width=True, caption="Understanding your mental well-being")


    with st.container():
        st.header("About This Tool ℹ️", divider="gray")
        st.markdown("""
        This application is designed to **assess and predict the risk levels** of postpartum depression (PPD)
        using a machine learning model trained on questionnaire responses and demographic inputs.

        It aims to provide:
        * **Insights** into potential mental health conditions.
        * **Personalized risk categories**: *Mild*, *Moderate*, *Severe*, or *Profound*.
        * **Supportive feedback** based on the model’s prediction.
        """)

        with st.expander("⚠️ Important Disclaimer"):
            st.warning("""
            This tool is for informational and educational purposes only. It is **not a substitute for professional diagnosis or medical advice**.
            If you are experiencing symptoms, please consult a healthcare provider. Early intervention is key.
            """)

    st.write("---") # Visual separator

    # --- User Input Section ---
    st.header("Your Information 📝", divider="blue")

    # Demographics in columns for a cleaner look
    col1, col2 = st.columns(2)
    with col1:
        # Age will now be pre-filled from signup, but user can change it if they want
        Age = st.slider("1. Age", 18, 45, st.session_state['user_age'], help="Your current age.")
    with col2:
        is_pregnant = st.selectbox("2. Are you currently pregnant? 🤰", ["Select...", "Yes", "No"], index=0)
        has_given_birth_recently = st.selectbox("3. Have you given birth recently? 👶", ["Select...", "Yes", "No"], index=0)

    # Input validation for these selectboxes
    if is_pregnant == "Select..." or has_given_birth_recently == "Select...":
        st.warning("Please select an option for questions 2 and 3. ⚠️")

    FamilySupport = st.selectbox("4. Do you have Family Support? 👨‍👩‍👧‍👦", ["Select...", "Low", "Medium", "High"], index=0)
    if FamilySupport == "Select...":
        st.warning("Please select an option for family support. ⚠️")


    st.write("---") # Another separator line
    st.header("Edinburgh Postnatal Depression Scale (EPDS) Questionnaire 📋", divider="orange")
    st.markdown("""
    Please answer the following questions based on how you have felt **over the past 7 days**.
    Choose the answer that comes closest to how you have been feeling.
    """)

    # Define responses once (cleaner code, replacing your individual Q1_response etc.)
    Q_responses = {
        "Q1": {"As much as I always could": 0, "Not quite so much now": 1, "Definitely not so much now": 2, "Not at all": 3},
        "Q2": {"As much as I ever did": 0, "Rather less than I used to": 1, "Definitely less than I used to": 2, "Hardly at all": 3},
        "Q3": {"Yes, most of the time": 3, "Yes, some of the time": 2, "Not very often": 1, "No, never": 0},
        "Q4": {"No, not at all": 0, "Hardly ever": 1, "Yes, sometimes": 2, "Yes, very often": 3},
        "Q5": {"Yes, quite a lot": 3, "Yes, sometimes": 2, "No, not much": 1, "No, not at all": 0},
        "Q6": {"Yes, most of the time I haven't been able to cope at all": 3, "Yes, sometimes I haven't been coping as well as usual": 2, "No, most of the time I have coped quite well": 1, "No, I have been coping as well as ever": 0},
        "Q7": {"Yes, most of the time": 3, "Yes, sometimes": 2, "Not very often": 1, "No, not at all": 0},
        "Q8": {"Yes, most of the time": 3, "Yes, quite often": 2, "Not very often": 1, "No, not at all": 0},
        "Q9": {"Yes, most of the time": 3, "Yes, quite often": 2, "Only occasionally": 1, "No, never": 0},
        "Q10": {"Yes, quite often": 3, "Sometimes": 2, "Hardly ever": 1, "Never": 0}
    }

    # Collect all question responses (your existing selectboxes, but make sure to use Q_responses)
    Q1 = st.selectbox("1. I have been able to laugh and see the funny side of things. 😂", list(Q_responses["Q1"].keys()))
    Q2 = st.selectbox("2. I have looked forward with enjoyment to things. 😊", list(Q_responses["Q2"].keys()))
    Q3 = st.selectbox("3. I have blamed myself unnecessarily when things went wrong. 😔", list(Q_responses["Q3"].keys()))
    Q4 = st.selectbox("4. I have been anxious or worried for no good reason. 😟", list(Q_responses["Q4"].keys()))
    Q5 = st.selectbox("5. I have felt scared or panicky for no very good reason. 😨", list(Q_responses["Q5"].keys()))
    Q6 = st.selectbox("6. Things have been getting on top of me. 😩", list(Q_responses["Q6"].keys()))
    Q7 = st.selectbox("7. I have been so unhappy that I have had difficulty sleeping. 😴", list(Q_responses["Q7"].keys()))
    Q8 = st.selectbox("8. I have felt sad or miserable. 😞", list(Q_responses["Q8"].keys()))
    Q9 = st.selectbox("9. I have been so unhappy that I have been crying. 😭", list(Q_responses["Q9"].keys()))
    Q10 = st.selectbox("10. The thought of harming myself has occurred to me. 🔪", list(Q_responses["Q10"].keys()))

    # Get numerical values
    q1_val = Q_responses["Q1"][Q1]
    q2_val = Q_responses["Q2"][Q2]
    q3_val = Q_responses["Q3"][Q3]
    q4_val = Q_responses["Q4"][Q4]
    q5_val = Q_responses["Q5"][Q5]
    q6_val = Q_responses["Q6"][Q6]
    q7_val = Q_responses["Q7"][Q7]
    q8_val = Q_responses["Q8"][Q8]
    q9_val = Q_responses["Q9"][Q9]
    q10_val = Q_responses["Q10"][Q10]

    score = q1_val + q2_val + q3_val + q4_val + q5_val + q6_val + q7_val + q8_val + q9_val + q10_val

    # --- Prediction Button and Logic ---
    st.write("---")
    # Add a button to trigger prediction, making it more explicit
    if st.button("Predict PPD Risk 📊", type="primary"):
        # Perform input validation before proceeding with prediction
        if (is_pregnant == "Select..." or
            has_given_birth_recently == "Select..." or
            FamilySupport == "Select..."):
            st.error("Please ensure all demographic questions are answered before predicting. 🚨")
        else:
            input_data = pd.DataFrame([{
                "Age": Age, # Use the Age from the slider
                "FamilySupport": FamilySupport, # Your model's pipeline should handle this categorical feature
                "Q1": q1_val,
                "Q2": q2_val,
                "Q3": q3_val,
                "Q4": q4_val,
                "Q5": q5_val,
                "Q6": q6_val,
                "Q7": q7_val,
                "Q8": q8_val,
                "Q9": q9_val,
                "Q10": q10_val,
                "EPDS_Score": score
            }])

            try:
                prediction_encoded = model.predict(input_data)[0]
                prediction_label = le.inverse_transform([prediction_encoded])[0]

                st.subheader("Prediction Results 🎉")
                risk_color = "green"
                feedback = "" # Initialize feedback message
                if prediction_label == "Mild":
                    risk_color = "green"
                    feedback = "Your responses indicate a **Mild** risk. Remember, early support can be beneficial. Consider discussing your feelings with a trusted person or healthcare professional if concerns arise. 💚"
                elif prediction_label == "Moderate":
                    risk_color = "orange"
                    feedback = "Your responses indicate a **Moderate** risk. It's highly recommended to speak with a healthcare provider or mental health professional for further evaluation and support. 🧡"
                elif prediction_label == "Severe":
                    risk_color = "red"
                    feedback = "Your responses indicate a **Severe** risk. Please seek immediate professional medical advice. Support is available, and you don't have to go through this alone. ❤️"
                elif prediction_label == "Profound":
                    risk_color = "darkred" # Streamlit doesn't have a direct 'darkred' but it works with custom HTML
                    feedback = "Your responses indicate a **Profound** risk. This is a critical indicator. Please seek immediate professional medical attention. Reach out to an emergency service or mental health crisis line if you are in distress. 🚨"

                # Display predicted risk with dynamic color
                st.markdown(f"**Predicted Postpartum Depression Risk:** <span style='color:{risk_color}; font-size: 24px; font-weight: bold;'>{prediction_label}</span>", unsafe_allow_html=True)
                st.info(feedback) # Display the feedback message

                st.write("---")
                st.subheader("Risk Level Visualization 📊")
                # Customize the bar chart for better presentation
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar([prediction_label], [prediction_encoded], color=risk_color) # Use the color from above
                ax.set_ylim([-0.5, 3.5]) # Adjust y-limits to accommodate 0 to 3 clearly
                ax.set_yticks([0, 1, 2, 3])
                ax.set_yticklabels(['Mild (0)', 'Moderate (1)', 'Severe (2)', 'Profound (3)'])
                ax.set_ylabel("Risk Level")
                ax.set_title("Predicted PPD Risk Level")
                ax.grid(axis='y', linestyle='--', alpha=0.7) # Add light grid lines
                st.pyplot(fig)

                # Optional: Display EPDS Score
                st.info(f"Your calculated EPDS Score: **{score}** (Max: 30) 🎯")

            except Exception as e:
                st.error(f"An error occurred during prediction: {e}. Please check your model pipeline. 🛑")

    else:
        st.info("Click 'Predict PPD Risk' to see your results. ▶️")

    # --- End of your main app.py content (this marks the end of the logged-in section) ---

else:
    # Show the login/signup page if not logged in
    show_login_page()
```
