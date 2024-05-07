import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from components.header import display_header
from components.login import handle_login, handle_signup, init_firebase
from utilities.data_utils import load_models, predict_rf

# Initialize Firebase Admin at the start of your app
init_firebase()

def main():
    st.set_page_config(page_title="Hyper Localized Weather Prediction System")
    display_header()

    # Session state initialization for 'logged_in' and 'view'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = None
    if 'view' not in st.session_state:
        st.session_state['view'] = 'login'  # Default view

    # Navigation between login and signup
    navigate_login_signup()

    # Handle user actions post-login
    if st.session_state.logged_in:
        handle_user_actions()

def navigate_login_signup():
    if st.session_state.logged_in is None:
        if st.session_state.view == 'login':
            login_view()
        elif st.session_state.view == 'signup':
            signup_view()

def login_view():
    user = handle_login()
    if user:
        st.session_state.logged_in = user
        st.session_state.username = user.display_name
        st.session_state.view = 'home'
        st.experimental_rerun()
    else:
        st.write("Don't have an account?")
        if st.button('Sign up here'):
            st.session_state.view = 'signup'
            st.experimental_rerun()

def signup_view():
    user = handle_signup()
    if user:
        st.session_state.logged_in = user
        st.session_state.username = user.display_name
        st.session_state.view = 'home'
        st.experimental_rerun()
    else:
        if st.button('Already have an account? Log in here'):
            st.session_state.view = 'login'
            st.experimental_rerun()

def handle_user_actions():
    choice = st.sidebar.selectbox("Menu", ["Home Page", "Location", "About the App", "Sign Out"])
    if choice == "Home Page":
        st.write(f"Welcome to the Hyper Localized Weather Prediction System, {st.session_state.username}!")
    elif choice == "Location":
        handle_location_selection()
    elif choice == "About the App":
        st.write("This app predicts weather parameters based on historical data.")
    elif choice == "Sign Out":
        logout_user()

    if st.session_state.get('location'):
        handle_predictions()

def handle_location_selection():
    st.session_state.location = st.sidebar.selectbox("Select Location", ["Nsukka", "Ayingba"])

def logout_user():
    st.session_state.logged_in = None
    st.session_state.view = 'login'
    st.experimental_rerun()

def handle_predictions():
    models = load_models(st.session_state.location)
    with st.form(key='prediction_form'):
        year, month, day, day_of_week, week_of_year, quarter = get_user_input()
        submit_button = st.form_submit_button(label='Predict')
    
    if submit_button:
        st.session_state['prediction_data'] = display_prediction_results(year, month, day, day_of_week, week_of_year, quarter, models)

def get_user_input():
    year = st.number_input('Year', min_value=2015, max_value=2025, value=2021)
    month = st.number_input('Month', min_value=1, max_value=12, value=1)
    day = st.number_input('Day', min_value=1, max_value=31, value=1)
    day_of_week = st.number_input('Day of Week', min_value=0, max_value=6, value=0)
    week_of_year = st.number_input('Week of Year', min_value=1, max_value=52, value=1)
    quarter = st.number_input('Quarter', min_value=1, max_value=4, value=1)
    return year, month, day, day_of_week, week_of_year, quarter

def display_prediction_results(year, month, day, day_of_week, week_of_year, quarter, models):
    features = np.array([[year, month, day, day_of_week, week_of_year, quarter]])
    prediction = predict_rf(models, features)
    today = datetime.now().strftime("%Y-%m-%d")
    data = [(param, value, today) for param, value in prediction.items()]
    results_df = pd.DataFrame(data, columns=['Weather Parameters', 'Predicted Values', 'Date'])
    st.table(results_df)
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV", csv, "weather_predictions.csv", "text/csv", key='download-csv')
    return results_df

if __name__ == "__main__":
    main()
