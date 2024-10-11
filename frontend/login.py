# login.py
import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

def get_auth_token(username, password):
    """
    Function to get the authentication token.
    """
    data = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/auth/token", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get authentication token")
        return None

def refresh_auth_token(refresh_token):
    """
    Function to refresh the authentication token.
    """
    data = {"refresh_token": refresh_token}
    response = requests.post(f"{BASE_URL}/auth/refresh", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to refresh authentication token")
        return None

def user_login():
    """
    Function to handle user login.
    """
    st.header("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        tokens = get_auth_token(username, password)
        if tokens:
            st.session_state["access_token"] = tokens["access_token"]
            st.session_state["refresh_token"] = tokens["refresh_token"]
            st.success("Login successful!")

def main():
    user_login()
