import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from components.header import display_header
from components.login import handle_login, handle_signup, init_firebase
from utilities.data_utils import load_models, predict_rf, parameter_display_mapping

# Initialize Firebase Admin at the start of your app
init_firebase()

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = None
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []
if 'location' not in st.session_state:
    st.session_state.location = None
if 'prediction_data' not in st.session_state:
    st.session_state.prediction_data = None
if 'weekly_prediction_data' not in st.session_state:
    st.session_state.weekly_prediction_data = None

def main():
    st.set_page_config(page_title="Hyper Localized Weather Prediction System")
    display_header()  # This will now set the background as well

    # Home Page and Navigation
    if st.session_state.logged_in:
        logged_in_menu()
    else:
        logged_out_menu()

    if st.session_state.view == 'home':
        home_page()
    elif st.session_state.view == 'about':
        about_page()
    elif st.session_state.view == 'contact':
        contact_page()
    elif st.session_state.view == 'login':
        login_page()
    elif st.session_state.view == 'signup':
        signup_page()
    elif st.session_state.view == 'predictions':
        predictions_page()
    elif st.session_state.view == 'history':
        history_page()

    # Add footer to all pages
    add_footer()

def add_footer():
    footer = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.8);
            text-align: center;
            padding: 10px;
            font-family: 'Arial', sans-serif;
            font-size: 14px;
        }
    </style>
    <div class="footer">
        <p>© Matthew Daniel 2024</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

def logged_out_menu():
    st.sidebar.button('Home', on_click=set_view, args=('home',))
    st.sidebar.button('About the Website', on_click=set_view, args=('about',))
    st.sidebar.button('Contact Us', on_click=set_view, args=('contact',))
    st.sidebar.button('Login', on_click=set_view, args=('login',))

def logged_in_menu():
    st.sidebar.button('Home', on_click=set_view, args=('home',))
    st.sidebar.button('About the Website', on_click=set_view, args=('about',))
    st.sidebar.button('Get Weather Predictions', on_click=set_view, args=('predictions',))
    st.sidebar.button('Prediction History', on_click=set_view, args=('history',))
    st.sidebar.button('Contact Us', on_click=set_view, args=('contact',))
    st.sidebar.button('Sign Out', on_click=logout_user)

def set_view(view):
    st.session_state.view = view

def home_page():
    st.markdown("<h2 style='text-align: center; color: white;'>Welcome to the Hyper Localized Weather Prediction System!</h2>", unsafe_allow_html=True)
    if st.session_state.logged_in:
        st.markdown(f"<h3 style='text-align: center; color: white;'>Logged in as: {st.session_state.username}</h3>", unsafe_allow_html=True)

def about_page():
    st.markdown("<h3 style='text-align: center; color: white;'>About Hyper-Localized Weather Prediction System</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color: black; font-size: 18px;'>
    This Hyper-Localized Weather Prediction System was built for Nsukka and Anyigba cities in Nigeria to revolutionize the region's preparedness for climatic variations leveraging IoT and Embedded Systems to gather real-time data on nine critical weather parameters: air temperature, barometric pressure, relative humidity, rainfall rate, soil temperature, solar radiation, wind direction, wind speed, and soil moisture. Each parameter plays a vital role in monitoring climatic changes, ensuring comprehensive coverage for accurate predictions. Localized prediction would help residents, farmers, individuals, businesses, government agencies, and researchers by providing more accurate and detailed information for improved decision-making and risk mitigation, whether it is planning agricultural activities, managing water resources, health issues, transportation, urban planning, and disaster management by preparing for extreme weather occurrences like floods or droughts thereby, ultimately improving overall quality of life.
    
    You should take your time to explore the system!
    </div>
    """, unsafe_allow_html=True)

def contact_page():
    st.markdown("<h2 style='text-align: center; color: white;'>Contact Information</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color: black; font-size: 18px;'>
    <p>Email: daniel.matthew.pg0303076@unn.edu.ng</p>
    <p>Phone: +2348063132442</p>
    </div>
    """, unsafe_allow_html=True)

def login_page():
    user = handle_login()
    if user:
        st.session_state.logged_in = user
        st.session_state.username = user.display_name
        st.session_state.view = 'home'
        st.experimental_rerun()
    else:
        st.markdown("<div style='color: black;'>Don't have an account?</div>", unsafe_allow_html=True)
        if st.button('Sign up here'):
            st.session_state.view = 'signup'
            st.experimental_rerun()

def signup_page():
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

def predictions_page():
    st.session_state.location = st.selectbox("Select Location", ["Nsukka", "Anyigba"])
    with st.form(key='prediction_form'):
        date = st.date_input('Select Date', datetime.now())
        submit_button = st.form_submit_button(label='Predict')
    
    if submit_button:
        handle_predictions(date)

    # Display prediction results if available
    if st.session_state.prediction_data is not None:
        st.markdown("<h3 style='text-align: center; color: white;'>Prediction Results</h3>", unsafe_allow_html=True)
        display_prediction_table(st.session_state.prediction_data)
        csv = st.session_state.prediction_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download as CSV", csv, "weather_predictions.csv", "text/csv", key='download-csv')

    # Display weekly prediction graph if available
    if st.session_state.weekly_prediction_data is not None:
        st.markdown("<h3 style='text-align: center; color: white;'>Weekly Prediction Graph</h3>", unsafe_allow_html=True)
        fig = plot_weekly_predictions(st.session_state.weekly_prediction_data)
        st.plotly_chart(fig)

def display_prediction_table(data):
    fig = go.Figure(data=[go.Table(
        header=dict(values=[f"<b>{col}</b>" for col in data.columns],
                    line_color='black', fill_color='royalblue',
                    font=dict(color='white', size=14), height=32),
        cells=dict(values=[data[col] for col in data.columns],
                   line_color='black',
                   fill_color=['paleturquoise', ['palegreen', '#fdbe72'] * len(data)],
                   font=dict(size=14),
                   height=32)
    )])

    fig.update_layout(margin=dict(l=10, r=10, b=10, t=10), height=350)
    st.plotly_chart(fig, use_container_width=True)

def handle_predictions(date):
    models = load_models(st.session_state.location)
    results_df = display_prediction_results(date, models)
    results_df['Location'] = st.session_state.location  # Add location to the results dataframe
    st.session_state.prediction_data = results_df
    st.session_state.predictions_history.append(results_df)

    # Generate weekly predictions
    weekly_predictions = generate_weekly_predictions(date, models)
    st.session_state.weekly_prediction_data = weekly_predictions

def display_prediction_results(date, models):
    year = date.year
    month = date.month
    day = date.day
    day_of_week = date.weekday()
    week_of_year = date.isocalendar()[1]
    quarter = (month - 1) // 3 + 1

    features = np.array([[year, month, day, day_of_week, week_of_year, quarter]])
    prediction = predict_rf(models, features)
    prediction_date = date.strftime("%Y-%m-%d")
    
    data = [(parameter_display_mapping[st.session_state.location].get(param, param), f"{value}", prediction_date) for param, value in prediction.items()]
    results_df = pd.DataFrame(data, columns=['Weather Parameters', 'Predicted Values', 'Date'])
    return results_df

def generate_weekly_predictions(start_date, models):
    dates = [start_date + timedelta(days=i) for i in range(7)]
    all_predictions = []

    for date in dates:
        year = date.year
        month = date.month
        day = date.day
        day_of_week = date.weekday()
        week_of_year = date.isocalendar()[1]
        quarter = (month - 1) // 3 + 1

        features = np.array([[year, month, day, day_of_week, week_of_year, quarter]])
        prediction = predict_rf(models, features)
        for param, value in prediction.items():
            display_name = parameter_display_mapping[st.session_state.location].get(param, param)
            all_predictions.append({'Date': date.strftime("%Y-%m-%d"), 'Weather Parameter': display_name, 'Predicted Value': f"{value}"})

    weekly_predictions_df = pd.DataFrame(all_predictions)
    return weekly_predictions_df

def plot_weekly_predictions(weekly_data):
    fig = px.line(weekly_data, x='Date', y='Predicted Value', color='Weather Parameter',
                  title='Weekly Weather Predictions')
    return fig

def history_page():
    st.markdown("<h2 style='text-align: center; color: white;'>Prediction History</h2>", unsafe_allow_html=True)
    for i, df in enumerate(st.session_state.predictions_history):
        st.write(f"Prediction {i+1} for {df['Location'].iloc[0]}")
        display_prediction_table(df)
        if st.button(f'Delete Prediction {i+1}'):
            del st.session_state.predictions_history[i]
            st.experimental_rerun()

def logout_user():
    st.session_state.logged_in = None
    st.session_state.view = 'home'
    st.session_state.location = None
    st.session_state.prediction_data = None
    st.session_state.weekly_prediction_data = None
    st.experimental_rerun()

if __name__ == "__main__":
    main()
