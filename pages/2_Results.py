
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import set_page_style, Q_RESPONSES # Import shared styling and responses

# Apply consistent page style
set_page_style()

st.title("Your PPD Risk Results ✨")

# Ensure all necessary data is in session state
if 'demographics' not in st.session_state or \
   'epds_answers' not in st.session_state or \
   'epds_score' not in st.session_state or \
   'model' not in st.session_state or \
   'le' not in st.session_state:
    st.warning("It looks like you haven't completed the questionnaire. Please start from the Home page. ↩️")
    st.page_link("pages/0_Home.py", label="Go to Home Page") # Link to the new Home page
    st.stop() # Stop execution if data is missing

# Load data from session state
demographics = st.session_state.demographics
epds_answers = st.session_state.epds_answers
epds_score = st.session_state.epds_score
model = st.session_state.model
le = st.session_state.le

st.header("Summary of Your Responses 📊", divider="blue")
with st.expander("Show Demographics"):
    st.json(demographics) # Display demographics in a clean JSON format
with st.expander("Show EPDS Answers"):
    # Display EPDS answers in a more readable format
    epds_questions = st.session_state.get('epds_questions_list', [f"Question {i+1}." for i in range(10)])
    for i, (q_key, answer) in enumerate(epds_answers.items()):
        question_text_short = epds_questions[i] if i < len(epds_questions) else f"Question {i+1}."
        st.markdown(f"**{i+1}. {question_text_short}:** {answer}")
    st.markdown(f"**Total EPDS Score:** {epds_score}")

st.write("---")

# --- Perform Prediction ---
st.header("Prediction Analysis 🧠", divider="orange")

# Validate EPDS answers before creating input_data (FIX for KeyError)
all_epds_answered_validly = True
epds_numerical_values = {}
for i in range(1, 11):
    q_key = f"Q{i}"
    selected_option = epds_answers.get(q_key) # Use .get() to avoid KeyError if key is missing
    if selected_option is None or selected_option not in Q_RESPONSES[q_key]:
        all_epds_answered_validly = False
        break
    epds_numerical_values[q_key] = Q_RESPONSES[q_key][selected_option]

if not all_epds_answered_validly:
    st.error("It seems some questionnaire answers are missing or invalid. Please retake the questionnaire. 🚨")
    if st.button("Retake Questionnaire 🔄"):
        st.session_state.current_q_index = 0
        st.session_state.epds_answers = {f"Q{i}": None for i in range(1, 11)}
        st.session_state.demographics = {
            'Age': 25,
            'is_pregnant': "Select...",
            'has_given_birth_recently': "Select...",
            'FamilySupport': "Select..."
        }
        st.page_link("pages/1_Questionnaire.py", label="Go to Questionnaire") # Link to the questionnaire page
        st.stop()
    st.stop()


# Prepare input data for the model
input_data = pd.DataFrame([{
    "Age": demographics['Age'],
    "FamilySupport": demographics['FamilySupport'],
    "Q1": epds_numerical_values["Q1"], # Use the validated numerical values
    "Q2": epds_numerical_values["Q2"],
    "Q3": epds_numerical_values["Q3"],
    "Q4": epds_numerical_values["Q4"],
    "Q5": epds_numerical_values["Q5"],
    "Q6": epds_numerical_values["Q6"],
    "Q7": epds_numerical_values["Q7"],
    "Q8": epds_numerical_values["Q8"],
    "Q9": epds_numerical_values["Q9"],
    "Q10": epds_numerical_values["Q10"],
    "EPDS_Score": epds_score # This should also be correct if all answers are valid
}])

try:
    prediction_encoded = model.predict(input_data)[0]
    prediction_label = le.inverse_transform([prediction_encoded])[0]

    st.subheader("Your Predicted PPD Risk Level: 🎉")
    risk_color = "green"
    feedback = ""
    if prediction_label == "Mild":
        risk_color = "green"
        feedback = "Your responses indicate a **Mild** risk. This suggests good overall well-being. Continue to monitor your feelings and practice self-care. If concerns arise, don't hesitate to reach out. 💚"
    elif prediction_label == "Moderate":
        risk_color = "orange"
        feedback = "Your responses indicate a **Moderate** risk. It's a good time to reflect on what might be contributing to these feelings. We highly recommend talking to a healthcare provider, a therapist, or a trusted friend/family member. Early support can make a significant difference. 🧡"
    elif prediction_label == "Severe":
        risk_color = "red"
        feedback = "Your responses indicate a **Severe** risk. This is a strong signal for concern. It is crucial to **seek professional medical advice immediately**. Please contact your doctor, a mental health professional, or an emergency service. Support is available, and you are not alone. ❤️"
    elif prediction_label == "Profound":
        risk_color = "darkred"
        feedback = "Your responses indicate a **Profound** risk. This requires urgent attention. Please **seek immediate professional medical attention**. If you are in distress or feel overwhelmed, please reach out to an emergency service or a mental health crisis line without delay. Your well-being is paramount. 🚨"

    st.markdown(f"**Predicted Postpartum Depression Risk:** <span style='color:{risk_color}; font-size: 28px; font-weight: bold;'>{prediction_label}</span>", unsafe_allow_html=True)
    st.info(feedback)

    st.write("---")
    st.subheader("Risk Level Visualization 📊")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar([prediction_label], [prediction_encoded], color=risk_color)
    ax.set_ylim([-0.5, 3.5])
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['Mild (0)', 'Moderate (1)', 'Severe (2)', 'Profound (3)'])
    ax.set_ylabel("Risk Level")
    ax.set_title("Predicted PPD Risk Level based on EPDS Score")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.info(f"Your calculated EPDS Score: **{epds_score}** (out of a maximum of 30) 🎯")

except Exception as e:
    st.error(f"An error occurred during prediction: {e}. Please ensure the questionnaire was fully completed and the model is correctly loaded. 🛑")

st.write("---")
st.subheader("What to do next? ➡️")
st.markdown("""
<div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
    <p>Regardless of your predicted risk level, remember that seeking support is a sign of strength.</p>
    <ul>
        <li><b>Talk to someone:</b> Share your feelings with a partner, friend, family member, or healthcare provider.</li>
        <li><b>Self-care:</b> Prioritize sleep, nutrition, and gentle exercise. Even small steps help.</li>
        <li><b>Professional Help:</b> If you're struggling, consult a doctor or a mental health specialist (e.g., therapist, psychiatrist). They can offer diagnosis and personalized treatment plans.</li>
    </ul>
    <p>You can always revisit the questionnaire or start over.</p>
</div>
""", unsafe_allow_html=True)

col_footer1, col_footer2 = st.columns(2)
with col_footer1:
    if st.button("Retake Questionnaire 🔄"):
        # Reset questionnaire progress and answers
        st.session_state.current_q_index = 0
        st.session_state.epds_answers = {f"Q{i}": None for i in range(1, 11)}
        st.session_state.demographics = { # Reset demographics too for a clean start
            'Age': 25,
            'is_pregnant': "Select...",
            'has_given_birth_recently': "Select...",
            'FamilySupport': "Select..."
        }
        st.page_link("pages/1_Questionnaire.py", label="Go to Questionnaire") # Navigate back to start
        st.stop()
with col_footer2:
    if st.button("Back to Home Page 🏠"):
        st.page_link("pages/0_Home.py", label="Go to Home Page") # Navigate back to home
        st.stop()
