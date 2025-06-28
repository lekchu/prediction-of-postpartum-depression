import streamlit as st
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
# bcrypt import is removed as login system is not included

# --- Configuration (This should be the FIRST Streamlit command) ---
st.set_page_config(
    page_title="PPD Risk Predictor",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto" # 'auto' or 'expanded' works fine without sidebar content
)

# --- Custom CSS for enhanced aesthetics (BLUE SHADES) ---
# This section defines the colors, fonts, and layout to make the app attractive.
st.markdown("""
<style>
    /* Main app background - Very light blue, provides a calming base */
    .reportview-container {
        background: #e3f2fd; /* Lightest blue (e.g., from Material Design Blue 50) */
    }
    .main .block-container {
        padding-top: 2rem; /* Reduce top padding for a tighter look */
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    /* Sidebar background - Slightly deeper light blue for visual separation */
    .st-emotion-cache-1wvz7m { /* Streamlit's auto-generated class for sidebar background */
        background-color: #bbdefb; /* Light blue (e.g., Material Design Blue 100) */
    }
    .sidebar .sidebar-content {
        background-color: #bbdefb; /* Fallback for sidebar content background */
    }
    h1 {
        color: #1565c0; /* Darker blue for the main title for strong contrast */
        text-align: center; /* Center align the main title */
    }
    h2, h3, h4, h5, h6 {
        color: #2196f3; /* Medium blue for other headers */
    }
    /* Card-like background for main content sections, keeps forms contained and attractive */
    .css-10jb6m0 { /* This targets the default Streamlit container styling */
        background-color: white; /* Keep content areas white for readability */
        padding: 20px;
        border-radius: 10px; /* Rounded corners for a softer look */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        margin-bottom: 20px;
    }
    /* Stylish buttons */
    .stButton>button {
        background-color: #4CAF50; /* Green (can be changed to blue like #2196f3 if desired) */
        color: white;
        border-radius: 8px; /* Rounded buttons */
        padding: 10px 24px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2); /* Shadow for depth */
    }
    .stButton>button:hover {
        background-color: #45a049; /* Darker green on hover */
    }
    /* Styling for text input fields */
    .stTextInput>div>div>input {
        border-radius: 8px; /* Rounded input fields */
        border: 1px solid #90caf9; /* Light blue border */
    }
    /* Styling for select boxes */
    .stSelectbox>div>div>div {
        border-radius: 8px; /* Rounded select boxes */
        border: 1px solid #90caf9; /* Light blue border */
    }
</style>
""", unsafe_allow_html=True)


# --- Global Variables / Model Loading ---
# User data file and related functions removed as login is not included

# Load trained model and label encoder
try:
    model = joblib.load('ppd_model_pipeline.pkl')
    le = joblib.load('label_encoder.pkl')
except FileNotFoundError:
    st.error("Error: Model or label encoder files not found. Please ensure 'ppd_model_pipeline.pkl' and 'label_encoder.pkl' are in the same directory.")
    st.stop() # This stops the app if the files aren't there, so it doesn't crash later

# --- Main Application Logic (Directly displayed without login) ---

st.title("Postpartum Depression Risk Predictor 🧠")

# Add a graphic to the main page header to enhance visual appeal
# IMPORTANT: Ensure 'ppd_banner.png' is in your GitHub repo in the same folder as app.py
# This image will appear prominently at the top of the app.
try:
    st.image("ppd_banner.png", use_column_width=True, caption="Understanding Postpartum Mental Well-being")
except Exception:
    st.info("💡 Tip: Add 'ppd_banner.png' to your repository for a visual header!")


with st.container(): # Use a container to group the 'About' section with a distinct background/shadow
    st.header("About This Tool ℹ️", divider="gray")
    st.markdown("""
    This application is designed to **assess and predict the risk levels** of postpartum depression (PPD)
    using a machine learning model trained on questionnaire responses and demographic inputs.

    It aims to provide:
    * **Insights** into potential mental health conditions.
    * **Personalized risk categories**: *Mild*, *Moderate*, *Severe*, or *Profound*.
    * **Supportive feedback** based on the model’s prediction.
    """)

    with st.expander("⚠️ Important Disclaimer"): # Use an expander to keep the disclaimer compact
        st.warning("""
        This tool is for informational and educational purposes only. It is **not a substitute for professional diagnosis or medical advice**.
        If you are experiencing symptoms, please consult a healthcare provider. Early intervention is key.
        """)

st.write("---") # Visual separator to break up sections

# --- User Input Section ---
st.header("Your Information 📝", divider="blue")

# Demographics in columns for a cleaner, less 'form-like' layout
col1, col2 = st.columns(2)
with col1:
    Age = st.slider("1. Age", 18, 45, 25, help="Your current age.")
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

# Define responses once for all questions
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

# Collect all question responses with clear labels and emojis
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

# Get numerical values from responses
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
# Add a prominent button to trigger prediction
if st.button("Predict PPD Risk 📊", type="primary"):
    # Perform input validation before proceeding with prediction
    if (is_pregnant == "Select..." or
        has_given_birth_recently == "Select..." or
        FamilySupport == "Select..."):
        st.error("Please ensure all demographic questions are answered before predicting. 🚨")
    else:
        input_data = pd.DataFrame([{
            "Age": Age,
            "FamilySupport": FamilySupport,
            "Q1": q1_val, "Q2": q2_val, "Q3": q3_val, "Q4": q4_val, "Q5": q5_val,
            "Q6": q6_val, "Q7": q7_val, "Q8": q8_val, "Q9": q9_val, "Q10": q10_val,
            "EPDS_Score" :score
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
                risk_color = "darkred"
                feedback = "Your responses indicate a **Profound** risk. This is a critical indicator. Please seek immediate professional medical attention. Reach out to an emergency service or mental health crisis line if you are in distress. 🚨"

            # Display predicted risk with dynamic color and bold text
            st.markdown(f"**Predicted Postpartum Depression Risk:** <span style='color:{risk_color}; font-size: 24px; font-weight: bold;'>{prediction_label}</span>", unsafe_allow_html=True)
            st.info(feedback) # Display the feedback message for user guidance

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
