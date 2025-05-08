# Traffic Severity Prediction App

A Streamlit application for predicting traffic severity based on environmental and temporal factors.

## Features

- Interactive map interface for selecting coordinates
- Input controls for all prediction parameters
- Real-time severity prediction
- Historical prediction tracking
- Visualizations of prediction patterns
- Mobile-responsive design

## Technical Details

The application uses a machine learning model to predict traffic severity based on eight input parameters:

1. Longitude
2. Latitude
3. Distance from major intersection
4. Temperature
5. Humidity
6. Pressure
7. Hour of day
8. Time duration

The model predicts one of four severity classes:
- 0: Minimal
- 1: Minor
- 2: Moderate
- 3: Severe

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/traffic-severity-prediction.git
   cd traffic-severity-prediction
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Add your trained model:
   - Place your `traffic_severity_model.pkl` file in the `model/` directory
   - Place your `scaler.pkl` file in the `model/` directory

### Running the Application

To run the application locally:

```
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

## Deployment to Streamlit Cloud

1. Create a Streamlit Cloud account at [streamlit.io](https://streamlit.io/)
2. Connect your GitHub repository to Streamlit Cloud
3. Configure the deployment settings
4. Deploy the application

## Project Structure

```
traffic-severity-prediction/
├── app.py                 # Main Streamlit application
├── components.py          # UI components
├── config.py              # Configuration settings
├── model_loader.py        # Model loading utilities
├── utils.py               # Helper functions
├── requirements.txt       # Dependencies
├── model/                 # Directory for ML model files
│   └── README.md          # Instructions for model files
└── README.md              # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for providing the framework
- Contributors to the various open-source libraries used