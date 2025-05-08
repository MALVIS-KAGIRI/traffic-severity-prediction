"""
Utility functions for the Traffic Severity Prediction app.
"""
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from config import SEVERITY_CLASSES
import base64
from datetime import datetime
import os

def load_css():
    """Load custom CSS styles."""
    css = """
    <style>
        .severity-card {
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        .severity-card:hover {
            transform: translateY(-5px);
        }
        .header-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .app-header {
            color: #1E3A8A;
            margin-bottom: 0;
        }
        .parameter-container {
            padding: 15px;
            border-radius: 10px;
            background-color: #F3F4F6;
            margin-bottom: 15px;
        }
        .prediction-result {
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .tooltip-icon {
            color: #9CA3AF;
            margin-left: 5px;
            font-size: 14px;
        }
        .map-container {
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        .stApp {
            background-color: #F9FAFB;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def save_prediction(prediction_data):
    """Save a prediction to the session state history."""
    if "predictions" not in st.session_state:
        st.session_state.predictions = []
    
    # Add timestamp to the prediction data
    prediction_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add to history (limit to last 50 predictions)
    st.session_state.predictions.append(prediction_data)
    if len(st.session_state.predictions) > 50:
        st.session_state.predictions.pop(0)

def get_severity_color(severity_class):
    """Get the color associated with a severity class."""
    return SEVERITY_CLASSES.get(severity_class, {}).get("color", "#CCCCCC")

def get_severity_label(severity_class):
    """Get the label associated with a severity class."""
    return SEVERITY_CLASSES.get(severity_class, {}).get("label", "Unknown")

def get_predictions_dataframe():
    """Convert prediction history to a dataframe."""
    if not st.session_state.predictions:
        return None
    
    return pd.DataFrame(st.session_state.predictions)

def plot_prediction_history(df):
    """Plot the history of predictions."""
    if df is None or df.empty:
        return None
    
    # Create a bar chart of severity levels
    severity_counts = df["severity_class"].value_counts().reset_index()
    severity_counts.columns = ["Severity", "Count"]
    severity_counts["Severity Label"] = severity_counts["Severity"].apply(get_severity_label)
    severity_counts["Color"] = severity_counts["Severity"].apply(get_severity_color)
    
    fig = px.bar(
        severity_counts, 
        x="Severity Label", 
        y="Count", 
        color="Severity Label",
        color_discrete_map={label: get_severity_color(sev) for sev, label in 
                           [(0, "Minimal"), (1, "Minor"), (2, "Moderate"), (3, "Severe")]},
        title="Prediction Distribution"
    )
    
    fig.update_layout(
        xaxis_title="Severity Level",
        yaxis_title="Number of Predictions",
        showlegend=False,
        plot_bgcolor="white",
        font=dict(size=14)
    )
    
    return fig

def plot_parameter_importance(df):
    """Create a visualization of parameter importance or trends."""
    if df is None or df.empty or len(df) < 5:
        return None
    
    # Calculate correlation between parameters and severity
    corr_data = []
    
    params = ["longitude", "latitude", "distance", "temperature", 
              "humidity", "pressure", "hour", "time_duration"]
    
    for param in params:
        if param in df.columns:
            correlation = df[param].corr(df["severity_class"])
            corr_data.append({"Parameter": param, "Correlation": abs(correlation)})
    
    corr_df = pd.DataFrame(corr_data)
    corr_df = corr_df.sort_values(by="Correlation", ascending=False)
    
    # Create horizontal bar chart
    fig = px.bar(
        corr_df,
        x="Correlation",
        y="Parameter",
        orientation="h",
        title="Parameter Importance (Correlation with Severity)",
        color="Correlation",
        color_continuous_scale=["#90CAF9", "#1E88E5", "#0D47A1"]
    )
    
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        plot_bgcolor="white",
        font=dict(size=14)
    )
    
    return fig

def generate_download_link(df, filename="prediction_history.csv", button_text="Download Data"):
    """Generate a download link for the prediction history data."""
    if df is None or df.empty:
        return None
    
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-button">{button_text}</a>'
    return href

def create_demo_model_folder():
    """Create a demo model folder structure if it doesn't exist."""
    model_dir = os.path.join(os.path.dirname(__file__), "model")
    os.makedirs(model_dir, exist_ok=True)
    
    # Create a README file explaining how to add the real model
    readme_path = os.path.join(model_dir, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write("""# Traffic Severity Prediction Model

This folder should contain your trained model files:

1. `traffic_severity_model.pkl` - The trained machine learning model
2. `scaler.pkl` - The scaler used to normalize input features

For the demo version, a simulated prediction is used when these files are not present.
""")