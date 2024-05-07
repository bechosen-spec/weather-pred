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
    
    # Display the header of the application
    display_header()

    # Session state initialization for 'logged_in' and 'view'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = None
    if 'view' not in st.session_state:
        st.session_state['view'] = 'login'  # Default view

    # Handle navigation between login and signup
    if st.session_state.logged_in is None:
        if st.session_state.view == 'signup':
            user = handle_signup()
            if user:
                st.session_state.logged_in = user
                st.session_state.username = user.display_name
                st.session_state.view = 'home'
                st.experimental_rerun()
        elif st.session_state.view == 'login':
            user = handle_login()
            if user:
                st.session_state.logged_in = user
                st.session_state.username = user.display_name
                st.session_state.view = 'home'
                st.experimental_rerun()
    else:
        st.sidebar.success(f"Logged in as {st.session_state.username}")
        if st.sidebar.button("Sign Out"):
            st.session_state.logged_in = None
            st.session_state.view = 'login'
            st.experimental_rerun()

    # App interface after login
    if st.session_state.logged_in:
        if st.session_state.view == 'home':
            st.write(f"Welcome to the Hyper Localized Weather Prediction System, {st.session_state.username}!")

        location = st.sidebar.selectbox("Select Location", ["Nsukka", "Ayingba"])
        models = load_models(location)

        # Prediction form
        submit_button = False  # Define submit_button outside the form to use it for conditional logic later
        with st.form(key='prediction_form'):
            year = st.number_input('Year', min_value=2015, max_value=2025, value=2021)
            month = st.number_input('Month', min_value=1, max_value=12, value=1)
            day = st.number_input('Day', min_value=1, max_value=31, value=1)
            day_of_week = st.number_input('Day of Week', min_value=0, max_value=6, value=0)
            week_of_year = st.number_input('Week of Year', min_value=1, max_value=52, value=1)
            quarter = st.number_input('Quarter', min_value=1, max_value=4, value=1)
            submit_button = st.form_submit_button(label='Predict')

        if submit_button:
            features = np.array([[year, month, day, day_of_week, week_of_year, quarter]])
            prediction = predict_rf(models, features)
            today = datetime.now().strftime("%Y-%m-%d")
            # Reformat the prediction results for vertical display
            results_df = pd.DataFrame(list(prediction.items()), columns=['Weather Parameters', 'Predicted Values'])
            results_df['Date'] = today  # Add today's date to the DataFrame
            st.write("Predicted Weather Parameters:")
            st.table(results_df)  # Display the DataFrame in Streamlit vertically
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download as CSV", csv, "weather_predictions.csv", "text/csv", key='download-csv')

if __name__ == "__main__":
    main()
