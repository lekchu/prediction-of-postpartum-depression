import streamlit as st
import joblib

# This minimal app.py ensures models are loaded only once and stored in session state.
# It acts as the primary entry point for Streamlit Cloud and initializes session state.

if 'model' not in st.session_state:
    try:
        st.session_state.model = joblib.load('ppd_model_pipeline.pkl')
        st.session_state.le = joblib.load('label_encoder.pkl')
    except FileNotFoundError:
        st.error("Error: Model or label encoder files not found. Please ensure 'ppd_model_pipeline.pkl' and 'label_encoder.pkl' are in the same directory as app.py.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred loading models: {e}. 🛑")
        st.stop()

# Initialize Session State variables if not already set
if 'demographics' not in st.session_state:
    st.session_state.demographics = {
        'Age': 25, # Default age
        'is_pregnant': "Select...",
        'has_given_birth_recently': "Select...",
        'FamilySupport': "Select..."
    }
if 'epds_answers' not in st.session_state:
    st.session_state.epds_answers = {f"Q{i}": None for i in range(1, 11)}
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0 # To track questionnaire progress

# This app.py itself doesn't display much; it simply sets up the environment.
# Your actual "Home" page content is now in pages/0_Home.py
st.markdown("### Initializing Application...")
st.markdown("Please select a page from the sidebar.")
# In deployment, Streamlit will automatically show the sidebar pages.
# The user will now see "Home" instead of "App" as the first page.
