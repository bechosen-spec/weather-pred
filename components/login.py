import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st

# Initialize Firebase Admin SDK
def init_firebase():
    if not firebase_admin._apps:
        cred_path = "/weather-forecast-e6321-firebase-adminsdk-gvb72-5a12750ba5.json"
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

# Function to create a new user in Firebase Authentication
def create_user(email, password, username):
    try:
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            display_name=username,
            disabled=False
        )
        return "Account created successfully!", user
    except Exception as e:
        return f"Failed to create account: {str(e)}", None

# Function to sign in an existing user in Firebase Authentication
def sign_in_user(email, password):
    try:
        # This is a placeholder as Firebase Admin SDK does not support direct password check
        user = auth.get_user_by_email(email)
        # Assuming a successful login for demonstration
        return "Logged in successfully!", user
    except Exception as e:
        return f"Failed to log in: {str(e)}", None

# Function to render the sign-up form and handle user creation
def handle_signup():
    st.subheader("Create New Account")
    username = st.text_input("Username", key='signup_username')
    email = st.text_input("Email", key='signup_email')
    password = st.text_input("Password", type='password', key='signup_password')

    if st.button("SignUp", key='signup_button'):
        message, user = create_user(email, password, username)
        if user:
            st.success(message)
            return user
        else:
            st.error(message)
            return None

# Function to render the login form and handle user authentication
def handle_login():
    st.subheader("Login")
    email = st.text_input("Email", key='login_email')
    password = st.text_input("Password", type='password', key='login_password')

    if st.button("Login", key='login_button'):
        message, user = sign_in_user(email, password)
        if user:
            st.success(message)
            return user
        else:
            st.error(message)
            return None

