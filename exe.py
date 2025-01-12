import streamlit as st

# Page configuration
st.set_page_config(page_title="Login Page", page_icon="🔒", layout="centered")

# CSS for modern styling
st.markdown("""
    <style>
        .stApp {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
        }
        .login-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: auto;
        }
        .login-header {
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: bold;
            font-size: 1.5rem;
            color: #333;
        }
        .login-btn {
            background-color: #007bff;
            color: #fff;
            font-size: 1rem;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        .login-btn:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

# Login page layout
def login_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="login-header">Login</div>', unsafe_allow_html=True)
    
    # Input fields
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    # Login button
    if st.button("Login", key="login", help="Click to log in"):
        if username == "admin" and password == "password123":
            st.success("Login successful!")
        elif username and password:
            st.error("Invalid username or password!")
        else:
            st.warning("Please fill out all fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Render the login page
login_page()
