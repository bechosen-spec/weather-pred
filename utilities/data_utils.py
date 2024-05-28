import numpy as np
import joblib

# Define location-specific targets
location_targets = {
    'Ayingba': ['AirTemp_Avg', 'BarPress_Avg', 'Rainfallrate_mm_Tot', 'RelativeHumidity',
                'SoilTemp_Avg', 'SolarRadiation_Avg', 'WindDir', 'WindSpeed_Avg', 'SoilMoisture'],
    'Nsukka': ['AirTemp_Avg', 'BarPress_Avg', 'Rainfallrate_mm_Tot', 'RelativeHumidity',
               'SoilTemp_Avg', 'SolarRadiationr_Avg', 'WindDir', 'WindSpeed_Avg', 'SoilMoisture']
}

# Mapping of original parameter names to display names with units
parameter_display_mapping = {
    'Ayingba': {
        'AirTemp_Avg': 'Air Temperature (°C)',
        'BarPress_Avg': 'Barometric Pressure (mbar)',
        'Rainfallrate_mm_Tot': 'Rainfall Rate (mm)',
        'RelativeHumidity': 'Relative Humidity (%)',
        'SoilTemp_Avg': 'Soil Temperature (°C)',
        'SolarRadiation_Avg': 'Solar Radiation (w/m²)',
        'WindDir': 'Wind Direction (°)',
        'WindSpeed_Avg': 'Wind Speed (m/s)',
        'SoilMoisture': 'Soil Volumetric Water Content'
    },
    'Nsukka': {
        'AirTemp_Avg': 'Air Temperature (°C)',
        'BarPress_Avg': 'Barometric Pressure (mbar)',
        'Rainfallrate_mm_Tot': 'Rainfall Rate (mm)',
        'RelativeHumidity': 'Relative Humidity (%)',
        'SoilTemp_Avg': 'Soil Temperature (°C)',
        'SolarRadiationr_Avg': 'Solar Radiation (w/m²)',  # Correct the name here to match the display
        'WindDir': 'Wind Direction (°)',
        'WindSpeed_Avg': 'Wind Speed (m/s)',
        'SoilMoisture': 'Soil Volumetric Water Content'
    }
}

# Function to load RF models for a specific location
def load_models(location):
    if location not in location_targets:
        raise KeyError(f"Location '{location}' not found in location_targets.")
    
    models = {}
    targets = location_targets[location]
    for target in targets:
        models[target] = joblib.load(f'Models/{location}/{target}_random_forest_model.joblib')
    return models

# RF prediction function
def predict_rf(models, features):
    results = {}
    for target, model in models.items():
        rf_pred = model.predict(features)
        results[target] = rf_pred[0]
    return results
