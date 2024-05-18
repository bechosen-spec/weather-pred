import streamlit as st

def display_header():
    add_background()  # Set the background image
    st.markdown("<h1 style='text-align: center; color: white;'>Hyper Localized Weather Prediction System</h1>", unsafe_allow_html=True)

def add_background():
    bg_image_path = "https://wallpaperaccess.com/full/1442216.jpg"
    bg_style = f"""
    <style>
    .stApp {{
        background: url("{bg_image_path}") no-repeat center center fixed;
        background-size: cover;
        font-family: 'Arial', sans-serif;
    }}
    .sidebar .sidebar-content {{
        background: rgba(255, 255, 255, 0.8);
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: white;
    }}
    p, div {{
        color: black;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)
