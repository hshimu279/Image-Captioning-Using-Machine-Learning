import streamlit as st
from PIL import Image
import os

from database import init_db, add_user, validate_user, save_caption, get_user_captions
from image_captioning import generate_caption, analyze_caption
from text_to_speech import text_to_speech
from utils import save_uploaded_image

# Initialize DB
init_db()

st.set_page_config(page_title="Image Captioning App with Login", page_icon="🖼️")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = ""

# Styles (optional - simple)
st.markdown("""
<style>
body {
    background-color: #f0f2f6;
}
h1 {
    color: #4B87FC;
    font-weight: 700;
}
.stButton>button {
    background-color: #4B87FC;
    color: white;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Detailed Image Captioning App with Custom Login")

def login_form():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        user_id = validate_user(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.username = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")

def register_form():
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="reg_username")
    new_password = st.text_input("Choose a password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm password", type="password", key="reg_confirm_password")

    if st.button("Register"):
        if not new_username or not new_password:
            st.warning("Username and password cannot be empty.")
        elif new_password != confirm_password:
            st.warning("Passwords do not match.")
        else:
            success = add_user(new_username, new_password)
            if success:
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists.")

if not st.session_state.logged_in:
    option = st.sidebar.selectbox("Select option", ["Login", "Register"])
    if option == "Login":
        login_form()
    else:
        register_form()
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.experimental_rerun()

    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png","jpg","jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        image_path = save_uploaded_image(uploaded_file)

        with st.spinner("Generating caption and analysis..."):
            caption = generate_caption(image)
            analysis = analyze_caption(caption)

        st.markdown("### Caption")
        st.write(caption)

        st.markdown("### Analysis")
        st.write(analysis)

        audio_path = text_to_speech(caption, filename="caption_audio.mp3")
        st.audio(audio_path)

        save_caption(st.session_state.user_id, image_path, caption, analysis)
    
    st.markdown("---")
    st.markdown("### Your previous captions and analysis")
    captions = get_user_captions(st.session_state.user_id)
    for idx, (img_path, caption, analysis) in enumerate(captions):
        st.markdown(f"**Image {idx + 1}:**")
        st.image(img_path, width=150)
        st.write(f"Caption: {caption}")
        st.write(f"Analysis: {analysis}")
        st.markdown("---")
