import streamlit as st
import pyperclip
import time
import pandas as pd

from utils import *
from components.master import *
from sql_queries import *


def show_user_login_page():
    if not st.session_state['loggedIn']:
        username = st.text_input(label="Username", value="", placeholder="Enter you user name")
        password = st.text_input(label="Password", value="", placeholder="Enter your password", type="password")
        col_login, col_reg = st.columns([1, 1])
        with col_login:
            if st.button("Login",):
                if verify_user(username, password.encode('utf-8'), key)==1:
                    st.session_state['loggedIn']=True
                    st.session_state['logged_username']=username
                    st.success("Logged in Successfully!")
                    with st.spinner("Redirecting to User page..."):
                        time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.error("Incorrect credentials. Please try again")
        with col_reg:
            if st.button("Register"):
                st.session_state['home'] = False
                st.session_state['register'] = True
                st.session_state['generated_password'] = ""
                st.experimental_rerun()

def user_register_page():
    st.title("Register")

    username = st.text_input(label="Username", value="", placeholder="Enter you user name", key='reg_username')
    password = st.text_input(label="Password", value="", placeholder="Enter your password", type="password")
    
    col_reg, col_login = st.columns([1,1])
    with col_reg:
        if st.button("Register"):
            if not username and not password:
                st.error("Please enter username and password")
            elif not username:
                st.error("Please enter an username")
            elif not password:
                st.error("Please enter password")
            else:
                check_user = verify_user(username, b"random", key)
                if check_user==0:
                    st.error("Username already exists")
                elif check_user==-1:
                    pass_strength = password_strength(password)
                    if pass_strength<4:
                        st.error("Password is weak!. Please enter a strong password\nUse [A-Z, a-z, 0-9, symbols]")
                    elif pass_strength==4:
                        st.error("Password is medium!. Please enter a strong password\nUse [A-Z, a-z, 0-9, symbols]")
                    else:
                        register_user(username, password.encode('utf-8'),key)
                        st.success("User registed successfully")
                        st.session_state['loggedIn'] = True
                        st.session_state['register'] = False
                        st.session_state['logged_username'] = username
                        with st.spinner("Redirecting to User page..."):
                            time.sleep(1)
                        st.experimental_rerun()
                    
    with col_login:
        # if st.markdown("<a style='text-decoration: none; padding: 10px 20px; background-color: #007bff; color: white; border-radius: 5px; cursor: pointer;'>Login</a>", unsafe_allow_html=True):
        if st.button("Go back Login page"):
            st.session_state['register'] = False
            st.experimental_rerun()

    col_pass_len, col_pass_button, col_pass_text, col_copy = st.columns([1,1,3,1])
    with col_pass_len:
        pass_len = st.number_input("Password length", value=8, placeholder="password length")
    
    with col_pass_button:
        if st.button("Generate"):
            generated_pass = password_generator(pass_len)
            st.session_state['generated_password'] = generated_pass
            with col_pass_text:
                st.text(f"Recommended password : {generated_pass}")
    
    print(f"{st.session_state['generated_password']=}")
    if st.session_state['generated_password']!="":
        with col_copy:
            if st.button('Copy'):
                pyperclip.copy(st.session_state['generated_password'])
                st.success('Password copied successfully!')
        

    if username:
        print(f"{key=}")
        check_user = verify_user(username, b"random", key)
        print(f"{check_user=}")
        if check_user==0:
            st.error("Username already exists")

    # if password:
    #     score = password_strength(password)
    #     strength = "Weak"
    #     if score > 3:
    #         strength = "Medium"
    #     if score >= 5:
    #         strength = "Strong"

    #     st.write(f"The entered password strength is {strength}.\n Please use a stronger password. You may use the password generator above.")


def user_login_page():
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn']=False
        show_user_login_page()
    else:
        if st.session_state['loggedIn']:
            master_login_page()
        else:
            show_user_login_page()

def user_page(username):
    col_title, col_logout = st.columns([6, 1])
    with col_title:
        st.title(f"User - {username}")
    with col_logout:
        if st.button("Log Out",):
            st.session_state['loggedIn'] = False
            st.session_state['logged_username'] = ""
            st.experimental_rerun()
            
    web_name_col, web_username_col, web_pass_col, web_add_but_col = st.columns([1,1,1,1])
    with web_name_col:
        website_name = st.text_input(label="Website name", value="", placeholder="website")
    
    with web_username_col:
        website_username = st.text_input(label="username", value="", placeholder="username")
    
    with web_pass_col:
        website_password = st.text_input(label="password", value="", placeholder="password")
    
    with web_add_but_col:
        if st.button("Add"):
            
            if not website_name or not website_username or not website_password:
                st.error("Entries cannot be empty")
            elif password_strength(website_password)<4:
                st.error("Password is weak!. Please enter a stronge password\nUse [A-Z, a-z, 0-9, symbols]")
            elif password_strength(website_password)==4:
                st.error("Password is medium!. Please enter a stronge password\nUse [A-Z, a-z, 0-9, symbols]")
            elif add_website_creds(username, website_name, website_username, website_password.encode('utf-8'), key)==-1:
                st.error("Account already exists")
            else:
                st.success("Account added successfully!")

    st.write("")
    col_pass_len, col_pass_button, col_pass_text, col_copy = st.columns([1,1,3,1])
    with col_pass_len:
        pass_len = st.number_input("Password length", value=8, placeholder="password length")
    
    with col_pass_button:
        if st.button("Generate"):
            generated_pass = password_generator(pass_len)
            st.session_state['generated_password'] = generated_pass
            with col_pass_text:
                st.text(f"Recommended password : {generated_pass}")
    
    if st.session_state['website_generated_password']!="":
        with col_copy:
            if st.button("Copy"):
                pyperclip.copy(st.session_state['website_generated_password'])
                st.success('Password copied successfully!')
    
    # if website_password:
    #     score = password_strength(website_password)
    #     strength = "Weak"
    #     if score > 3:
    #         strength = "Medium"
    #     if score >= 5:
    #         strength = "Strong"

    #     st.write(f"The entered password strength is {strength}.\n Please use a stronger password. You may use the password generator above.")


    st.markdown("### All website Credentials:")
    web_creds = show_user_website_creds(username)
    if web_creds:
        df = pd.DataFrame(web_creds, columns=["index", "user", "website", "username", "password"])
        df = df[["website", "username", "password"]]
        for i in df.index:
            df.loc[i, "password"] = decrypt_data(df.loc[i, "password"], key).decode('utf-8')
        print(df)
        st.table(data=df)
    else:
        st.write("No entries yet!")
