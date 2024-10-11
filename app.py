import streamlit as st
from dotenv import load_dotenv
from frontend import home, login, register, chat

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="GAIA OpenAI Model Evaluator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS (unchanged)
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #f3e7e9 0%, #e3eeff 99%, #e3eeff 100%);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #f3e7e9 0%, #e3eeff 99%, #e3eeff 100%);
    }
    h1 {
        color: #1e3d59;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #1e3d59;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

PAGES = {
    "Home": home,
    "Login": login,
    "Register": register,
    "Chat": chat
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.main()  # Changed from page.app() to page.main()

if __name__ == "__main__":
    main()
