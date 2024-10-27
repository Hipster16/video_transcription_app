import streamlit as st
from get_audio import download_bilibili_audio
from get_transcription import get_transcription
import shutil

hide_menu_style = """
<style>
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stAppDeployButton {display: none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
# Set the title of the app

st.title("Video Transcription")

# Create a text input field
user_input = st.text_input("Enter the video URL:")

# Create a button to trigger the processing
if st.button("Transcribe"):
    # Ensure user has entered a URL
    if user_input:
        # Initialize a placeholder for the progress and messages
        progress_bar = st.progress(0)

        # Step 1: Download audio
        st.write("Downloading audio...")
        file_name = download_bilibili_audio(user_input)
        progress_bar.progress(50)  # Update progress to 50%

        # Step 2: Get transcription
        st.write("Getting transcription...")
        transcription_text = get_transcription(file_name)
        progress_bar.progress(100)  # Update progress to 100%
        shutil.rmtree("downloads")
        # Final message
        st.success("Transcription done")

        # Add download button for the transcription
        st.download_button(
            label="Download Transcription",
            data=transcription_text,
            file_name="transcribe.txt",
            mime="text/plain"
        )
    else:
        st.error("Please enter a valid video URL.")
