import streamlit as st
import auth_manager as am

def show_login():
    st.title("🔐 Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("Login")
        with col2:
            if st.form_submit_button("Register Instead"):
                st.session_state.show_register = True
                st.rerun()
        
        if submit:
            try:
                user = am.authenticate_user(email, password)
                st.session_state.user = user
                st.session_state.authenticated = True
                st.success("Successfully logged in!")
                st.rerun()
            except ValueError as e:
                st.error(str(e))

def show_register():
    st.title("📝 Register")
    
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("Register")
        with col2:
            if st.form_submit_button("Login Instead"):
                st.session_state.show_register = False
                st.rerun()
        
        if submit:
            if password != confirm_password:
                st.error("Passwords do not match!")
                return
            
            try:
                user = am.register_user(username, email, password)
                st.session_state.user = user
                st.session_state.authenticated = True
                st.success("Successfully registered!")
                st.rerun()
            except ValueError as e:
                st.error(str(e))

def show():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if not st.session_state.authenticated:
        if st.session_state.show_register:
            show_register()
        else:
            show_login()
        return False
    
    return True
