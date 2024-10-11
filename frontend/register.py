import streamlit as st
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.users import UserRequest, UserCreateRequest
from backend.services.users import _create_user
from backend.database import db_session as get_async_session
from backend.utils import get_password_hash
from backend.config import settings
from pydantic import ValidationError

async def register_user():
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

        # Hash the password
        hashed_password = get_password_hash(new_password)

        # Convert to UserCreateRequest with hashed password
        user_create_request = UserCreateRequest(
            **user_request.model_dump(exclude={'password'}),
            password=hashed_password
        )

        async for session in get_async_session():
            user = await _create_user(user_create_request, session)
            if user:
                st.success("User registered successfully!")
                return True
            else:
                st.error("Failed to register user. Username or email may already be in use.")

    return False

def main():
    asyncio.run(register_user())

if __name__ == "__main__":
    main()
