import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)

# Set page config
st.set_page_config(
    page_title="NASA System Engineering Engine",
    initial_sidebar_state="expanded",
)

# Display the title
st.title("NASA System Engineering Engine")

# Loading config file
with open('frontend/config/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)



# Initialize session state for registration success
if 'registration_success' not in st.session_state:
    st.session_state['registration_success'] = False

# Creating a login widget
try:
    authenticator.login()
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    authenticator.logout()
    
    # Create tabs for logged-in users
    tab1, tab2 = st.tabs(["SE Engine", "Account Settings"])
    
    with tab1:
        # Read the content from the SE.md file
        with open('backend/data/nasa/guidelines/SE.md', 'r') as file:
            se_content = file.read()
        st.markdown(se_content)
    
    with tab2:
        # Password reset widget
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success('Password modified successfully')
        except ResetError as e:
            st.error(e)
        except CredentialsError as e:
            st.error(e)

        # Update user details widget
        try:
            if authenticator.update_user_details(st.session_state["username"]):
                st.success('Entries updated successfully')
        except UpdateError as e:
            st.error(e)

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    if not st.session_state['registration_success']:
        
        # Create tabs for non-logged-in users
        tab1, tab2, tab3 = st.tabs(["Register", "Forgot Password", "Forgot Username"])
        
        with tab1:
            # New user registration widget
            try:
                (email_of_registered_user,
                 username_of_registered_user,
                 name_of_registered_user) = authenticator.register_user(pre_authorization=False)
                if email_of_registered_user:
                    st.success('User registered successfully')
                    st.session_state['registration_success'] = True
                    st.rerun()
            except RegisterError as e:
                st.error(e)

        with tab2:
            # Forgot password widget
            try:
                (username_of_forgotten_password,
                 email_of_forgotten_password,
                 new_random_password) = authenticator.forgot_password()
                if username_of_forgotten_password:
                    st.success(f"New password to be sent to user securely")
                    config['credentials']['usernames'][username_of_forgotten_password]['password'] = Hasher([new_random_password]).generate()[0]
                    # Random password to be transferred to the user securely
                elif username_of_forgotten_password == False:
                    st.error('Username not found')
            except ForgotError as e:
                st.error(e)

        with tab3:
            # Forgot username widget
            try:
                (username_of_forgotten_username,
                 email_of_forgotten_username) = authenticator.forgot_username()
                if username_of_forgotten_username:
                    st.success(f"Username to be sent to user securely")
                    # Username to be transferred to the user securely
                elif username_of_forgotten_username == False:
                    st.error('Email not found')
            except ForgotError as e:
                st.error(e)
    else:
        st.success('Registration successful! Please log in.')

# Saving config file
with open('frontend/config/config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)