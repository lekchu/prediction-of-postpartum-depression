import streamlit as st

def set_page_style():
    """Applies consistent page configuration and custom CSS for blue shades."""
    st.set_page_config(
        page_title="PPD Risk Predictor",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="auto"
    )

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
            background-color: #4CAF50; /* Green */
            color: white;
            border-radius: 8px; /* Rounded buttons */
            padding: 10px 24px;
            border: none;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2); /* Shadow for depth */
            transition: background-color 0.3s ease; /* Smooth hover effect */
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
        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background-color: #4CAF50; /* Green progress bar */
        }
    </style>
    """, unsafe_allow_html=True)

# Define responses for questionnaire here so all pages can access them
Q_RESPONSES = {
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
