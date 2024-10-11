# frontend/register.py
import streamlit as st
import requests
from pydantic import ValidationError
from backend.schemas.users import UserRequest

BASE_URL = "http://localhost:8000"


def register_user():
    st.subheader("Register")

    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    new_email = st.text_input("Email")
    new_full_name = st.text_input("Full Name")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return False

        try:
            # Create UserRequest object
            user_request = UserRequest(
                username=new_username,
                password=new_password,
                email=new_email,
                full_name=new_full_name
            )
        except ValidationError as e:
            st.error(f"Validation error: {e}")
            return False

        # Make a POST request to the FastAPI endpoint
        response = requests.post(f"{BASE_URL}/users/", json=user_request.dict())

        if response.status_code == 201:
            st.success("User registered successfully!")
            return True
        elif response.status_code == 409:
            st.error("Failed to register user. Username or email may already be in use.")
        else:
            st.error(f"Failed to register user. Error: {response.text}")

    return False


def main():
    register_user()


if __name__ == "__main__":
    main()
