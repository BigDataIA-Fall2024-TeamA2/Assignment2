import streamlit as st
from backend.services.auth import authenticate_user
import asyncio

async def login_page():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = await authenticate_user(username, password)
        if user:
            st.success(f"Logged in successfully as {username}")
            st.session_state.user = user
            return True
        else:
            st.error("Invalid username or password")
    return False

def main():
    asyncio.run(login_page())

if __name__ == "__main__":
    main()
