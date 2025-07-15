import streamlit as st
from db import add_user, check_user

def login_ui():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_user(username, password):
            st.success(f"Welcome {username}")
            return username
        else:
            st.error("Invalid credentials")
    return None

def signup_ui():
    st.subheader("Signup")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        try:
            add_user(username, password)
            st.success("Account created! You can now log in.")
        except:
            st.error("Username already exists.")
