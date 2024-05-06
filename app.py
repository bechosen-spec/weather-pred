import streamlit as st
from components.header import display_header
from components.login import handle_login
from utilities.data_utils import load_model, make_prediction, download_link

def main():
    # Initialize Firebase or any other setup
    st.set_page_config(page_title="Hyper Localized Weather Prediction System")

    # Display header with celebration balloons
    display_header()

    # Handle user authentication
    user = handle_login()
    if user is None:
        st.warning("Please login to continue.")
        return

    # Layout for the main app
    location = st.sidebar.selectbox("Select Location", ["Nsukka", "Ayingba"])
    model = load_model(location)

    if st.sidebar.button("Sign Out"):
        # Firebase sign out logic
        pass

    if st.sidebar.button("Home Page"):
        st.write("Welcome to the Hyper Localized Weather Prediction System")

    # Prediction input form
    with st.form(key='prediction_form'):
        year = st.number_input('Year', min_value=2015, max_value=2025, value=2021)
        month = st.number_input('Month', min_value=1, max_value=12, value=1)
        day = st.number_input('Day', min_value=1, max_value=31, value=1)
        day_of_week = st.number_input('Day of Week', min_value=0, max_value=6, value=0)
        week_of_year = st.number_input('Week of Year', min_value=1, max_value=52, value=1)
        quarter = st.number_input('Quarter', min_value=1, max_value=4, value=1)
        submit_button = st.form_submit_button(label='Predict')

        if submit_button:
            features = [year, month, day, day_of_week, week_of_year, quarter]
            prediction = make_prediction(model, features)
            st.write("Predicted Weather Parameters:")
            st.table(prediction)
            csv = prediction.to_csv().encode('utf-8')
            st.download_button("Download as CSV", csv, "prediction.csv", "text/csv", key='download-csv')

if __name__ == "__main__":
    main()
