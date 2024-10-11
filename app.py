import streamlit as st
from dotenv import load_dotenv
from frontend.pages import _bkp_chat, user_creation, home, user_login
from frontend.pages.chat import qa_interface
from frontend.pages.user_creation import create_user
from frontend.pages.user_login import login

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

# PAGES = {
#     "Home": home,
#     "Login": login,
#     "Register": None,
#     "Chat": chat
# }
#
# st.sidebar.title("Navigation")
# selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
#
# page = PAGES[selection]
# page.main()  # Changed from page.app() to page.main()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="User Login", icon=":material/login:")
logout_page = st.Page(logout, title="Log Out", icon=":material/logout:")
user_creation_page = st.Page(create_user, title="User Registration", default=True)
qa_page = st.Page(qa_interface, title="Question Answering", icon=":material/chat:")


if st.session_state.logged_in:
    pg = st.navigation({
            "Question Answering Interface": [qa_page],
            "Logout": [logout_page]
        })
else:
    pg = st.navigation({
        "User Creation": [user_creation_page],
        "User Login": [login_page],
    })

pg.run()
