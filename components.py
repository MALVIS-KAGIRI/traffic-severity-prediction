"""
UI components for the Traffic Severity Prediction app.
"""
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    get_severity_color, 
    get_severity_label, 
    save_prediction, 
    plot_prediction_history,
    plot_parameter_importance,
    get_predictions_dataframe,
    generate_download_link
)
from model_loader import predict_severity
from config import (
    APP_TITLE, 
    APP_DESCRIPTION, 
    PAGES, 
    DEFAULT_VALUES,
    PARAMETER_RANGES,
    PARAMETER_UNITS,
    PARAMETER_HELP,
    SEVERITY_CLASSES,
    DEFAULT_MAP_ZOOM,
    MAP_STYLE
)

def show_header():
    """Display the app header."""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(
            f"""
            <div style="font-size: 54px; text-align: center;">
                🚦
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <h1 class="app-header">{APP_TITLE}</h1>
            <p>{APP_DESCRIPTION}</p>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown("---")

def show_sidebar():
    """Display the sidebar navigation and return the selected page."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 40px;">🚦</div>
                <h2>{APP_TITLE}</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        selected_page = st.radio("Navigation", list(PAGES.values()))
        
        # Get the key for the selected page value
        for key, value in PAGES.items():
            if value == selected_page:
                st.session_state.current_page = key
                break
        
        st.markdown("---")
        st.markdown("### About This App")
        st.markdown(
            """
            This application predicts traffic severity based on environmental 
            and temporal factors using machine learning.
            """
        )
        
        st.markdown("---")
        st.markdown("### Input Parameters")
        st.markdown(
            """
            - **Location**: Longitude and latitude coordinates
            - **Distance**: Distance from major intersection (km)
            - **Weather**: Temperature, humidity, and pressure
            - **Time**: Hour of day and duration
            """
        )
        
        st.markdown("---")
        st.markdown("© 2025 Traffic Severity Predictor")
    
    return st.session_state.current_page

def create_map(longitude, latitude):
    """Create an interactive map centered at the specified coordinates."""
    # Create a map centered at the specified location
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=DEFAULT_MAP_ZOOM,
        tiles=MAP_STYLE
    )
    
    # Add a marker at the specified location
    folium.Marker(
        location=[latitude, longitude],
        popup="Selected Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    # Add traffic severity visualization (for demonstration)
    folium.Circle(
        location=[latitude, longitude],
        radius=500,  # 500 meters radius
        color="blue",
        fill=True,
        fill_opacity=0.2,
        popup="Traffic Impact Zone"
    ).add_to(m)
    
    return m

def show_prediction_form():
    """Display the prediction input form."""
    with st.container():
        st.subheader("Enter Traffic Parameters")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Location parameters
            st.markdown("#### 📍 Location Parameters")
            
            lon_col, lat_col = st.columns(2)
            with lon_col:
                longitude = st.number_input(
                    "Longitude",
                    min_value=PARAMETER_RANGES["longitude"][0],
                    max_value=PARAMETER_RANGES["longitude"][1],
                    value=DEFAULT_VALUES["longitude"],
                    step=0.0001,
                    format="%.4f",
                    help=PARAMETER_HELP["longitude"]
                )
            
            with lat_col:
                latitude = st.number_input(
                    "Latitude",
                    min_value=PARAMETER_RANGES["latitude"][0],
                    max_value=PARAMETER_RANGES["latitude"][1],
                    value=DEFAULT_VALUES["latitude"],
                    step=0.0001,
                    format="%.4f",
                    help=PARAMETER_HELP["latitude"]
                )
            
            # Display the map
            st.markdown("##### Selected Location")
            m = create_map(longitude, latitude)
            folium_static(m, width=600, height=300)
            
            # Distance parameter
            distance = st.slider(
                "Distance from major intersection (km)",
                min_value=PARAMETER_RANGES["distance"][0],
                max_value=PARAMETER_RANGES["distance"][1],
                value=DEFAULT_VALUES["distance"],
                step=0.1,
                help=PARAMETER_HELP["distance"]
            )
            
            # Environmental parameters
            st.markdown("#### 🌡️ Environmental Parameters")
            
            env_col1, env_col2, env_col3 = st.columns(3)
            
            with env_col1:
                temperature = st.slider(
                    "Temperature (°C)",
                    min_value=PARAMETER_RANGES["temperature"][0],
                    max_value=PARAMETER_RANGES["temperature"][1],
                    value=DEFAULT_VALUES["temperature"],
                    step=0.5,
                    help=PARAMETER_HELP["temperature"]
                )
            
            with env_col2:
                humidity = st.slider(
                    "Humidity (%)",
                    min_value=PARAMETER_RANGES["humidity"][0],
                    max_value=PARAMETER_RANGES["humidity"][1],
                    value=DEFAULT_VALUES["humidity"],
                    step=1.0,
                    help=PARAMETER_HELP["humidity"]
                )
            
            with env_col3:
                pressure = st.slider(
                    "Pressure (hPa)",
                    min_value=PARAMETER_RANGES["pressure"][0],
                    max_value=PARAMETER_RANGES["pressure"][1],
                    value=DEFAULT_VALUES["pressure"],
                    step=0.5,
                    help=PARAMETER_HELP["pressure"]
                )
            
            # Time parameters
            st.markdown("#### ⏱️ Time Parameters")
            
            time_col1, time_col2 = st.columns(2)
            
            with time_col1:
                hour = st.slider(
                    "Hour of day (0-23)",
                    min_value=PARAMETER_RANGES["hour"][0],
                    max_value=PARAMETER_RANGES["hour"][1],
                    value=DEFAULT_VALUES["hour"],
                    step=1,
                    help=PARAMETER_HELP["hour"]
                )
            
            with time_col2:
                time_duration = st.slider(
                    "Time duration (minutes)",
                    min_value=PARAMETER_RANGES["time_duration"][0],
                    max_value=PARAMETER_RANGES["time_duration"][1],
                    value=DEFAULT_VALUES["time_duration"],
                    step=1.0,
                    help=PARAMETER_HELP["time_duration"]
                )
        
        with col2:
            st.markdown("#### 🔍 Prediction Results")
            
            # Collect all input features
            features = [
                longitude, latitude, distance, temperature, 
                humidity, pressure, hour, time_duration
            ]
            
            # Make predictions when the user clicks the button
            if st.button("Predict Traffic Severity", use_container_width=True):
                with st.spinner("Analyzing traffic conditions..."):
                    # Get prediction
                    severity_class = predict_severity(features)
                    
                    if severity_class is not None:
                        # Get severity details
                        severity_info = SEVERITY_CLASSES.get(severity_class, {
                            "label": "Unknown",
                            "color": "#CCCCCC",
                            "description": "Unable to determine severity"
                        })
                        
                        # Display result
                        st.markdown(
                            f"""
                            <div class="prediction-result" style="background-color: {severity_info['color']}30; 
                                                                 color: {severity_info['color']}; 
                                                                 border: 2px solid {severity_info['color']}">
                                <div style="font-size: 32px; margin-bottom: 10px;">{severity_info['label']}</div>
                                <div style="font-size: 16px;">{severity_info['description']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        # Save prediction
                        prediction_data = {
                            "longitude": longitude,
                            "latitude": latitude,
                            "distance": distance,
                            "temperature": temperature,
                            "humidity": humidity,
                            "pressure": pressure,
                            "hour": hour,
                            "time_duration": time_duration,
                            "severity_class": severity_class,
                            "severity_label": severity_info["label"]
                        }
                        save_prediction(prediction_data)
                        
                        # Show details
                        st.markdown("#### Prediction Details")
                        
                        # Format timestamp
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        st.markdown(f"**Time of prediction**: {timestamp}")
                        st.markdown(f"**Severity class**: {severity_class} ({severity_info['label']})")
                        
                        # Display parameter importance
                        st.markdown("#### Parameter Values")
                        
                        params_df = pd.DataFrame({
                            "Parameter": [
                                "Longitude", "Latitude", "Distance (km)", 
                                "Temperature (°C)", "Humidity (%)", 
                                "Pressure (hPa)", "Hour", "Duration (min)"
                            ],
                            "Value": features
                        })
                        
                        st.dataframe(params_df, hide_index=True, use_container_width=True)
                    else:
                        st.error("Failed to make prediction. Please check the input parameters.")
            
            # Show severity scale reference
            st.markdown("#### Severity Scale Reference")
            
            for severity in range(4):
                severity_info = SEVERITY_CLASSES.get(severity, {})
                
                st.markdown(
                    f"""
                    <div style="padding: 10px; 
                                margin-bottom: 10px; 
                                border-radius: 5px; 
                                background-color: {severity_info.get('color', '#CCCCCC')}30;
                                border-left: 5px solid {severity_info.get('color', '#CCCCCC')}">
                        <strong>{severity_info.get('label', 'Unknown')}</strong>: {severity_info.get('description', '')}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

def show_prediction_history():
    """Display the history of predictions."""
    st.subheader("Prediction History")
    
    # Get prediction history as dataframe
    df = get_predictions_dataframe()
    
    if df is not None and not df.empty:
        # Show visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Plot prediction distribution
            fig = plot_prediction_history(df)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Plot parameter importance
            fig = plot_parameter_importance(df)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
        
        # Show history table
        st.markdown("#### Recent Predictions")
        
        # Select and reorder columns for display
        display_columns = [
            "timestamp", "severity_label", "distance", "temperature", 
            "humidity", "hour", "time_duration"
        ]
        
        # Filter to only columns that exist in the dataframe
        display_columns = [col for col in display_columns if col in df.columns]
        
        # Rename columns for better display
        rename_dict = {
            "timestamp": "Time",
            "severity_label": "Severity",
            "distance": "Distance (km)",
            "temperature": "Temp (°C)",
            "humidity": "Humidity (%)",
            "hour": "Hour",
            "time_duration": "Duration (min)"
        }
        
        # Create display dataframe
        display_df = df[display_columns].copy()
        display_df.rename(columns=rename_dict, inplace=True)
        
        # Sort by timestamp (most recent first)
        if "Time" in display_df.columns:
            display_df.sort_values(by="Time", ascending=False, inplace=True)
        
        # Show table
        st.dataframe(display_df, hide_index=True, use_container_width=True)
        
        # Add download button
        st.markdown("#### Download Data")
        st.markdown(generate_download_link(df, "traffic_severity_predictions.csv", "Download Complete Prediction History"), unsafe_allow_html=True)
    else:
        st.info("No prediction history available. Make some predictions first!")
        
        # Show demo data
        st.markdown("#### Demo Visualization")
        
        # Create dummy data for demonstration
        demo_data = {
            "Severity": ["Minimal", "Minor", "Moderate", "Severe"],
            "Count": [12, 8, 5, 3],
            "Color": [
                SEVERITY_CLASSES[0]["color"],
                SEVERITY_CLASSES[1]["color"],
                SEVERITY_CLASSES[2]["color"],
                SEVERITY_CLASSES[3]["color"]
            ]
        }
        
        demo_df = pd.DataFrame(demo_data)
        
        fig = px.bar(
            demo_df,
            x="Severity",
            y="Count",
            color="Severity",
            color_discrete_map=dict(zip(demo_df["Severity"], demo_df["Color"])),
            title="Sample Prediction Distribution (Demo)"
        )
        
        fig.update_layout(
            xaxis_title="Severity Level",
            yaxis_title="Number of Predictions",
            showlegend=False,
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_about_section():
    """Display information about the app."""
    st.subheader("About Traffic Severity Prediction")
    
    st.markdown(
        """
        This application uses machine learning to predict traffic severity based on various environmental 
        and temporal factors. The prediction model has been trained on historical traffic data and can 
        classify traffic conditions into four severity levels.
        
        ### Prediction Inputs
        
        The model uses the following inputs to make predictions:
        
        - **Longitude & Latitude**: Geographic coordinates of the location
        - **Distance**: Distance from a major intersection or landmark (in kilometers)
        - **Temperature**: Ambient temperature in degrees Celsius
        - **Humidity**: Relative humidity percentage
        - **Pressure**: Atmospheric pressure in hectopascals (hPa)
        - **Hour**: Hour of the day (0-23)
        - **Time Duration**: Duration of the traffic observation in minutes
        
        ### Severity Classes
        
        The model classifies traffic severity into four categories:
        
        1. **Minimal**: Little to no impact on traffic flow
        2. **Minor**: Slight delays but generally smooth traffic
        3. **Moderate**: Noticeable congestion with moderate delays
        4. **Severe**: Heavy congestion with significant delays
        
        ### How to Use
        
        1. Navigate to the **Predict** page
        2. Enter the required parameters
        3. Click the "Predict Traffic Severity" button
        4. View the prediction results
        5. Check the **History** page to see past predictions and trends
        
        ### Deployment
        
        This application is deployed on Streamlit Cloud and can be accessed online. For local deployment, 
        follow these steps:
        
        1. Clone the repository
        2. Install required dependencies: `pip install -r requirements.txt`
        3. Place your trained model in the `model` folder
        4. Run the app: `streamlit run app.py`
        
        ### Model Information
        
        The prediction model is a machine learning classifier trained on historical traffic data. 
        It uses the input parameters to predict the likely severity of traffic conditions.
        
        For more information or to contribute to this project, please contact the development team.
        """
    )
    
    # Add a section about model limitations
    st.markdown("### Model Limitations")
    
    st.markdown(
        """
        While the traffic severity prediction model provides valuable insights, it has some limitations:
        
        - The model is based on historical data and may not account for unusual events
        - Predictions are most accurate for areas similar to those in the training data
        - The model does not account for traffic accidents or road closures
        - Weather conditions beyond the input parameters (e.g., snow, rain) are not directly modeled
        - The model is updated periodically but may not reflect very recent changes in traffic patterns
        """
    )