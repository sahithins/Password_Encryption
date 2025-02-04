from components.master import *
from components.user import *
import streamlit as st

def home_page():
    if 'register' in st.session_state and st.session_state['register']:
        user_register_page()
    elif 'loggedIn' in st.session_state and st.session_state['loggedIn']:
        st.session_state['website_generated_password'] = ""
        user_page(st.session_state['logged_username'])
    elif 'masterLoggedIn' in st.session_state and st.session_state['masterLoggedIn']:
        master_page()
    else:
        page = st.sidebar.selectbox("Choose a page", ["User login", "Master login"])

        if page == "User login":
            st.title("User Login")
            user_login_page()
        elif page == "Master login":
            master_login_page()

if __name__ == "__main__":
    init_DB()
    home_page()