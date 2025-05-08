import streamlit as st
from utils import load_css
from components import (
    show_header,
    show_sidebar,
    show_prediction_form,
    show_prediction_history,
    show_about_section
)
from config import APP_TITLE, APP_DESCRIPTION, PAGES

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# Initialize session state if not already initialized
if "predictions" not in st.session_state:
    st.session_state.predictions = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Predict"

# Display header
show_header()

# Display sidebar and get current page
current_page = show_sidebar()

# Main content based on selected page
if current_page == "Predict":
    show_prediction_form()
elif current_page == "History":
    show_prediction_history()
elif current_page == "About":
    show_about_section()