"""
Configuration settings for the Traffic Severity Prediction app.
"""

# App information
APP_TITLE = "Traffic Severity Prediction"
APP_DESCRIPTION = "Predict traffic severity based on environmental and temporal factors."
APP_VERSION = "1.0.0"

# Pages
PAGES = {
    "Predict": "🚦 Predict Severity",
    "History": "📊 Prediction History",
    "About": "ℹ️ About"
}

# Model parameters
DEFAULT_VALUES = {
    "longitude": -73.9857,
    "latitude": 40.7484,
    "distance": 5.0,
    "temperature": 25.0,
    "humidity": 65.0,
    "pressure": 1013.0,
    "hour": 12,
    "time_duration": 30.0
}

PARAMETER_RANGES = {
    "longitude": (-180.0, 180.0),
    "latitude": (-90.0, 90.0),
    "distance": (0.1, 50.0),
    "temperature": (-30.0, 50.0),
    "humidity": (0.0, 100.0),
    "pressure": (950.0, 1050.0),
    "hour": (0, 23),
    "time_duration": (1.0, 180.0)
}

PARAMETER_UNITS = {
    "longitude": "°",
    "latitude": "°",
    "distance": "km",
    "temperature": "°C",
    "humidity": "%",
    "pressure": "hPa",
    "hour": "",
    "time_duration": "min"
}

PARAMETER_HELP = {
    "longitude": "Geographic longitude coordinate",
    "latitude": "Geographic latitude coordinate",
    "distance": "Distance from a major intersection or landmark",
    "temperature": "Ambient temperature",
    "humidity": "Relative humidity in the air",
    "pressure": "Atmospheric pressure",
    "hour": "Hour of the day (0-23)",
    "time_duration": "Duration of the traffic incident or observation"
}

# Severity classes
SEVERITY_CLASSES = {
    0: {"label": "Minimal", "color": "#4CAF50", "description": "Minimal impact on traffic flow"},
    1: {"label": "Minor", "color": "#FFC107", "description": "Minor delays and slowdowns"},
    2: {"label": "Moderate", "color": "#FF9800", "description": "Moderate congestion affecting travel time"},
    3: {"label": "Severe", "color": "#F44336", "description": "Severe congestion with significant delays"}
}

# Map settings
DEFAULT_MAP_ZOOM = 13
MAP_STYLE = "OpenStreetMap"