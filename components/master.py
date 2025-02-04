import streamlit as st
import pandas as pd
import time
import base64

from password_encryption import *
from sql_queries import *

def master_login_page():
    st.title("Master Login")
    username = st.text_input(label="Username", value="", placeholder="Enter you user name")
    password = st.text_input(label="Password", value="", placeholder="Enter your password", type="password")
    if st.button("Login",):
        if username==admin_username and password==master_password.decode('utf-8'):
            st.session_state['masterLoggedIn']=True
            st.success("Logged in Successfully!")
            with st.spinner("Redirecting to Master page..."):
                time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("Incorrect credentials. Please try again")

def master_page():
    col_title, col_logout = st.columns([6, 1])
    with col_title:
        st.title(f"Master Page")
    with col_logout:
        if st.button("Log Out",):
            st.session_state['masterLoggedIn'] = False
            st.experimental_rerun()
    st.markdown("### All Users' Accounts :")
    web_creds = show_all_website_creds()
    if web_creds:
        df = pd.DataFrame(web_creds, columns=["index", "user", "website", "username", "password"])
        print(df)
        df = df[["user", "website", "username", "password"]]
        for i in df.index:
            df.loc[i, "password"] = str(df.loc[i, "password"])
        print(df)
        st.table(data=df)
    else:
        st.write("No entries yet!")

