import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page

# Set page config
st.set_page_config(page_title="Postpartum Depression Predictor", layout="wide")

# --- Background Image ---
def get_base64_bg(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_file):
    bg = get_base64_bg(image_file)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("assets/background.png")

# --- Page Content ---
st.title("Welcome to the PPD Risk Predictor 🏡")

# Add a striking image at the top
try:
    st.image("assets/mom_baby.png", use_column_width=False, width=300, caption="Supporting new mothers and families")
except Exception:
    st.warning("💡 Add 'assets/mom_baby.png' for header image.")

# Introduction
st.markdown("""
<div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
    <h2 style="color:#2196f3;">Understand Your Well-being 🌟</h2>
    <p>This tool helps assess potential risk levels for postpartum depression (PPD)
    using the clinically validated Edinburgh Postnatal Depression Scale (EPDS) and a machine learning model.</p>

    <h3>What You'll Get:</h3>
    <ul>
        <li>10-question step-by-step assessment</li>
        <li>Personalized risk prediction: Low / Moderate / High</li>
        <li>Confidential, instant feedback</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.write("---")

# Motivation
st.subheader("Why Use This Tool? 🤔")
st.markdown("""
Postpartum depression affects many mothers, yet often goes undetected.
This simple and supportive tool gives you an early snapshot of your emotional well-being.
""")

st.write("---")

# Start Button
st.subheader("Ready to Begin? 👇")
st.markdown("Click the button below to start the questionnaire. Your responses are private.")

if st.button("Start Questionnaire Now! 🚀", use_container_width=True):
    switch_page("2_Questionnaire")
