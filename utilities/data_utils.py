import numpy as np
import joblib

# Define location-specific targets
location_targets = {
    'Ayingba': ['AirTemp_Avg', 'BarPress_Avg', 'Rainfallrate_mm_Tot', 'RelativeHumidity',
                'SoilTemp_Avg', 'SolarRadiation_Avg', 'WindDir', 'WindSpeed_Avg', 'SoilMoisture'],
    'Nsukka': ['AirTemp_Avg', 'BarPress_Avg', 'Rainfallrate_mm_Tot', 'RelativeHumidity',
               'SoilTemp_Avg', 'SolarRadiationr_Avg', 'WindDir', 'WindSpeed_Avg', 'SoilMoisture']
}

# Function to load RF models for a specific location
def load_models(location):
    models = {}
    targets = location_targets[location]
    for target in targets:
        models[target] = joblib.load(f'/home/oem/weather-pred/Models/{location}/{target}_random_forest_model.joblib')
    return models

# RF prediction function
def predict_rf(models, features):
    results = {}
    for target, model in models.items():
        rf_pred = model.predict(features)
        results[target] = rf_pred[0]
    return results
