import streamlit as st
from utils import set_page_style, Q_RESPONSES # Import shared styling and responses

# Apply consistent page style
set_page_style()

st.title("PPD Risk Questionnaire 📝")
st.markdown("Please answer the following questions honestly to help us assess your risk.")

# Ensure models are loaded from session_state (they should be loaded by root app.py)
if 'model' not in st.session_state or 'le' not in st.session_state:
    st.error("Error: Model not loaded. Please go back to the Home page and refresh. 🛑")
    st.stop()

# --- Demographic Questions (Always visible at the top) ---
st.subheader("Your Information (Demographics) 👤", divider="blue")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("1. Age", 18, 45, st.session_state.demographics['Age'], help="Your current age.")
    with col2:
        is_pregnant = st.selectbox("2. Are you currently pregnant? 🤰", ["Select...", "Yes", "No"],
                                   index=["Select...", "Yes", "No"].index(st.session_state.demographics['is_pregnant']))
        has_given_birth_recently = st.selectbox("3. Have you given birth recently? 👶", ["Select...", "Yes", "No"],
                                                index=["Select...", "Yes", "No"].index(st.session_state.demographics['has_given_birth_recently']))

    family_support = st.selectbox("4. Do you have Family Support? 👨‍👩‍👧‍👦", ["Select...", "Low", "Medium", "High"],
                                  index=["Select...", "Low", "Medium", "High"].index(st.session_state.demographics['FamilySupport']))

    # Store demographics in session state as they are updated
    st.session_state.demographics['Age'] = age
    st.session_state.demographics['is_pregnant'] = is_pregnant
    st.session_state.demographics['has_given_birth_recently'] = has_given_birth_recently
    st.session_state.demographics['FamilySupport'] = family_support

# Validate demographics
demographics_valid = (
    st.session_state.demographics['is_pregnant'] != "Select..." and
    st.session_state.demographics['has_given_birth_recently'] != "Select..." and
    st.session_state.demographics['FamilySupport'] != "Select..."
)

if not demographics_valid:
    st.warning("Please complete all demographic questions before proceeding. ⚠️")

st.write("---")

# --- EPDS Questions (One by One) ---
st.subheader("Edinburgh Postnatal Depression Scale (EPDS) 📋", divider="orange")
st.markdown("Answer the following based on how you've felt **over the past 7 days**.")

epds_questions = [
    "I have been able to laugh and see the funny side of things. 😂",
    "I have looked forward with enjoyment to things. 😊",
    "I have blamed myself unnecessarily when things went wrong. 😔",
    "I have been anxious or worried for no good reason. 😟",
    "I have felt scared or panicky for no very good reason. 😨",
    "Things have been getting on top of me. 😩",
    "I have been so unhappy that I have had difficulty sleeping. 😴",
    "I have felt sad or miserable. 😞",
    "I have been so unhappy that I have been crying. 😭",
    "The thought of harming myself has occurred to me. 🔪"
]
num_epds_questions = len(epds_questions)

# Store epds_questions in session state for Results page
st.session_state['epds_questions_list'] = epds_questions


# Progress bar
progress_percent = (st.session_state.current_q_index / num_epds_questions) * 100
st.progress(int(progress_percent), text=f"Progress: {st.session_state.current_q_index}/{num_epds_questions} questions answered")

# Display current question
if st.session_state.current_q_index < num_epds_questions:
    q_key = f"Q{st.session_state.current_q_index + 1}"
    question_text = epds_questions[st.session_state.current_q_index]
    options = list(Q_RESPONSES[q_key].keys())

    # Get the previously selected answer for this question, if any
    current_answer_index = 0
    if st.session_state.epds_answers[q_key] is not None:
        try:
            current_answer_index = options.index(st.session_state.epds_answers[q_key])
        except ValueError:
            # If the stored answer is not in options (e.g., from an old version), reset to 0
            current_answer_index = 0


    selected_option = st.selectbox(
        f"{st.session_state.current_q_index + 1}. {question_text}",
        options,
        index=current_answer_index, # Pre-select previous answer
        key=f"epds_q_{st.session_state.current_q_index}" # Unique key for each selectbox
    )
    st.session_state.epds_answers[q_key] = selected_option # Store the selected answer

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Previous Question", disabled=(st.session_state.current_q_index == 0)):
            st.session_state.current_q_index -= 1
            st.rerun()
    with col_nav2:
        if st.button("Next Question ➡️", disabled=(selected_option is None or selected_option == "Select...")):
            st.session_state.current_q_index += 1
            st.rerun()
else:
    # All EPDS questions answered
    st.success("All questions answered! 🎉")
    st.markdown("You can now proceed to see your predicted PPD risk.")

    # Calculate total EPDS score
    total_epds_score = 0
    all_epds_answered_validly = True
    for i in range(1, 11):
        q_key = f"Q{i}"
        answer = st.session_state.epds_answers.get(q_key)
        if answer is None or answer not in Q_RESPONSES[q_key]:
            all_epds_answered_validly = False
            break
        total_epds_score += Q_RESPONSES[q_key][answer]

    if st.button("View My PPD Risk! 📊", use_container_width=True, type="primary", disabled=not (demographics_valid and all_epds_answered_validly)):
        if all_epds_answered_validly and demographics_valid:
            st.session_state.epds_score = total_epds_score
            # Navigate to the results page
            st.page_link("pages/2_Results.py", label="Go to Results", icon="📊")
            st.stop()
        else:
            st.error("Please ensure all questions are answered and demographics are selected. 🚨")
