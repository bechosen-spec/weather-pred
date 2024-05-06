import pandas as pd
import joblib

def load_model(location):
    return joblib.load(f'models/model_{location.lower()}.joblib')

def make_prediction(model, features):
    df = pd.DataFrame([features], columns=['Year', 'Month', 'Day', 'DayOfWeek', 'WeekOfYear', 'Quarter'])
    return pd.DataFrame(model.predict(df), columns=['AirTemp_Avg', 'BarPress_Avg', ...])
