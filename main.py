import streamlit as st
from googleapiclient.discovery import build
from requests.exceptions import RequestException
from functions import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set the dark theme and page config
st.set_page_config(page_title="EduTube Demo", layout="centered", initial_sidebar_state="collapsed")
tags = []

# Apply custom CSS for dark theme and brighter headers
st.markdown("""
    <style>
        body {
            background-color: #DCDCDC;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background-color: #DCDCDC;
        }
        .css-18e3th9 {
            background-color: #DCDCDC;
        }
        .css-1d391kg {
            background-color: #DCDCDC;
        }
        .stButton>button {
            background-color: #1f1f1f;
            color: #ffffff;
            border: 1px solid #ffffff;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            margin-top: 20px;
        }
        .stButton>button:hover {
            background-color: #333333;
        }
        .stSelectbox>div {
            background-color: #1f1f1f;
            color: #ffffff;
            border: 1px solid #ffffff;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        .stTextInput>div>div input {
            background-color: #1f1f1f;
            color: #ffffff;
            border: 1px solid #ffffff;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #FFFAF0;
        }
        .stVideo {
            border-radius: 10px;
        }
        .sidebar .sidebar-content {
            background-color: #1f1f1f;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# Structure of the Website
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

if 'active_users' not in st.session_state:
    st.session_state.active_users = 0

# Function to handle login
def login():
    if st.session_state.active_users < st.secrets["max_user"]:
        st.session_state.is_logged_in = True
        st.session_state.active_users += 1
        st.success("You are logged in.")
    else:
        st.error("Maximum number of users reached. Please try again later.")

# Function to handle logout
def logout():
    st.session_state.is_logged_in = False
    if st.session_state.active_users > 0:
        st.session_state.active_users -= 1
    st.success("You are logged out.")

# Function to handle sending email
def send_email(to_email, subject, message):
    from_email = st.secrets["email"]["from_email"]
    from_password = st.secrets["email"]["from_password"]

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email. Error: {e}")

# Main application logic
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Contact Us", "About Us"])

    if page == "Home":
        st.title("EduTube Demo")
        st.write(f" Maximum User is {st.secrets['max_user']}. We're Trying Survey and Increase APIs Limit")

        # Initialize session state if it doesn't exist
        if 'is_logged_in' not in st.session_state:
            st.session_state.is_logged_in = False

        # Display the login button if the user is not logged in
        if not st.session_state.is_logged_in:
            st.button("Enter the Demo EduTube Website", on_click=login)

        # Display the main content if the user is logged in
        if st.session_state.is_logged_in:
            st.title("Educational Video Recommendation")
            global tags
            if st.button('Generate tags'):
                tags = generate_tags()
            if len(tags) > 0:
                selected_tag = st.selectbox("Choose an educational tag:", tags)
                videos = search_videos(selected_tag)
                st.header(f"Suggested Videos for '{selected_tag}':")
                for video in videos:
                    video_title = video['snippet']['title']
                    video_id = video['id']['videoId']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"

                    st.subheader(video_title)
                    st.video(video_url)

            deep_search()

            if st.button("Logout"):
                logout()
                st.experimental_rerun()  # Rerun the script to clear the content

    elif page == "Contact Us":
        st.title("Contact Us")
        st.write("If you have any questions or feedback, feel free to contact us using the form below.")

        contact_form = st.form(key='contact_form')
        with contact_form:
            email = st.text_input("Your email address")
            subject = st.text_input("Subject")
            message = st.text_area("Message")
            submit_button = st.form_submit_button(label='Send')

        if submit_button:
            send_email(st.secrets["target_email"], subject, f"From: {email}\n\n{message}")

    elif page == "About Us":
        st.title("About Us")
        st.write("""
            ### EduTube Demo
            The objective of EduTube Demo is to provide a platform for users to find educational videos based on various advanced and diverse subjects. 
            By leveraging AI and machine learning, EduTube recommends high-quality educational content to enhance the learning experience.
        """)

if __name__ == "__main__":
    try:
        main()
    except RequestException:
        st.error("Error connecting to the APIs. Please try again next 24 hours.")


