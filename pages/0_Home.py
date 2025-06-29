import streamlit as st
from utils import set_page_style # Import our shared styling function

# Apply consistent page style
set_page_style()

# Ensure models are loaded from session state (they should be loaded by root app.py)
if 'model' not in st.session_state or 'le' not in st.session_state:
    st.error("Model not loaded. Please go back to the app's main URL and refresh. 🛑")
    st.stop()

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
# Note: Streamlit's native multi-page links use the file name without extension
if st.button("Start Questionnaire Now! 🚀", use_container_width=True):
    st.page_link("pages/1_Questionnaire.py", label="Go to Questionnaire", icon="🚀") # This creates a clickable link
    st.stop() # Stop execution of the current page
