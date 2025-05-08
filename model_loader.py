"""
Functions for loading and using the traffic severity prediction model.
"""
import pickle
import os
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler

# Cache the model loading to improve performance
@st.cache_resource
def load_model():
    """
    Load the traffic severity prediction model from the pickle file.
    Returns the model or None if the file doesn't exist.
    """
    try:
        # Check if the model file exists
        model_path = os.path.join(os.path.dirname(__file__), "model", "traffic_severity_model.pkl")
        
        if not os.path.exists(model_path):
            # For demonstration, create a dummy model folder and return None
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            return None
            
        # Load the model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Cache the scaler loading to improve performance
@st.cache_resource
def load_scaler():
    """
    Load the scaler used to normalize the input features.
    Returns the scaler or a new standard scaler if the file doesn't exist.
    """
    try:
        # Check if the scaler file exists
        scaler_path = os.path.join(os.path.dirname(__file__), "model", "scaler.pkl")
        
        if not os.path.exists(scaler_path):
            # For demonstration, return a new scaler
            return StandardScaler()
            
        # Load the scaler
        with open(scaler_path, 'rb') as file:
            scaler = pickle.load(file)
        return scaler
    except Exception as e:
        st.error(f"Error loading scaler: {str(e)}")
        return StandardScaler()

def predict_severity(features):
    """
    Predict traffic severity using the loaded model.
    
    Args:
        features: List of input features [Longitude, Latitude, Distance, Temperature, 
                                          Humidity, Pressure, Hour, Time Duration]
    
    Returns:
        Predicted severity class (0-3) or None if prediction fails
    """
    try:
        model = load_model()
        scaler = load_scaler()
        
        # If model is not available, use a dummy prediction for demonstration
        if model is None:
            # Simple dummy model for demonstration purposes
            # This will be replaced by the real model when available
            features_array = np.array(features).reshape(1, -1)
            normalized_features = features_array
            
            # Simple rule-based prediction for demonstration
            hour = features[6]
            distance = features[2]
            duration = features[7]
            
            if hour in [7, 8, 9, 16, 17, 18] and distance < 10:  # Rush hours
                if duration > 60:
                    return 3  # Severe
                elif duration > 30:
                    return 2  # Moderate
                else:
                    return 1  # Minor
            elif distance > 30 or duration < 15:
                return 0  # Minimal
            else:
                return 1  # Minor
        
        # Preprocess the input features
        features_array = np.array(features).reshape(1, -1)
        normalized_features = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(normalized_features)[0]
        return int(prediction)
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None