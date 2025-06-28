import streamlit as st
import joblib
from utils import set_page_style # Import our shared styling function

# Apply consistent page style
set_page_style()

# --- Model Loading (Load once and store in session state) ---
# This ensures models are loaded only once when the app starts
# and are available across all pages.
if 'model' not in st.session_state:
    try:
        st.session_state.model = joblib.load('ppd_model_pipeline.pkl')
        st.session_state.le = joblib.load('label_encoder.pkl')
        st.success("Model and Label Encoder loaded successfully! ✅")
    except FileNotFoundError:
        st.error("Error: Model or label encoder files not found. Please ensure 'ppd_model_pipeline.pkl' and 'label_encoder.pkl' are in the same directory as app.py.")
        st.stop() # Stop the app if files are missing
    except Exception as e:
        st.error(f"An unexpected error occurred loading models: {e}. 🛑")
        st.stop()

# --- Initialize Session State for Questionnaire (if not already set) ---
# This prepares the session state variables that will store user answers
# and questionnaire progress across the pages.
if 'demographics' not in st.session_state:
    st.session_state.demographics = {
        'Age': 25, # Default age
        'is_pregnant': "Select...",
        'has_given_birth_recently': "Select...",
        'FamilySupport': "Select..."
    }
if 'epds_answers' not in st.session_state:
    # Initialize all EPDS answers to None or a default value
    st.session_state.epds_answers = {f"Q{i}": None for i in range(1, 11)}
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0 # To track questionnaire progress

# --- Home Page Content ---
st.title("Welcome to the PPD Risk Predictor 🏡")

# Add a striking image at the top
try:
    st.image("ppd_banner.png", use_column_width=True, caption="Supporting new mothers and families")
except Exception:
    st.warning("💡 Tip: Add 'ppd_banner.png' to your repository for a beautiful header image!")

st.markdown("""
<div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
    <h2 style="color:#2196f3;">Understand Your Well-being 🌟</h2>
    <p>This application is designed to help **assess potential risk levels** for postpartum depression (PPD)
    using a machine learning model. It's built to be a supportive tool, providing insights based on your responses.</p>

    <h3>What You'll Find:</h3>
    <ul>
        <li>A guided questionnaire to gather relevant information.</li>
        <li>Personalized risk predictions: <i>Mild</i>, <i>Moderate</i>, <i>Severe</i>, or <i>Profound</i>.</li>
        <li>Helpful feedback and guidance based on the assessment.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.write("---") # Visual separator

st.subheader("Why Use This Tool? 🤔")
st.markdown("""
Navigating the postpartum period can be challenging. Our goal is to offer a confidential space
where you can reflect on your feelings and gain a better understanding of your mental health.
Early awareness is a powerful step towards seeking the right support.
""")

st.write("---")

# Call to action to start the questionnaire
st.subheader("Ready to Begin? 👇")
st.markdown("""
Click the button below to start the questionnaire. Your responses are confidential and used only for the prediction.
""")

# Use a link button to navigate to the questionnaire page
if st.button("Start Questionnaire Now! 🚀", use_container_width=True):
    # This will simulate navigating to the '1_Questionnaire' page.
    # In a deployed Streamlit app, clicking this would usually just switch page if '1_Questionnaire.py' is in 'pages/'
    # For local development, st.experimental_rerun() might be needed or simply navigating via sidebar.
    # For deployment, Streamlit's multi-page handling will manage the navigation.
    st.markdown("[Click here to go to Questionnaire](/Questionnaire)") # This creates a clickable link
    st.stop() # Stop execution of the current page
