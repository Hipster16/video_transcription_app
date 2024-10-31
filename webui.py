import streamlit as st
from get_audio import download_bilibili_audio
from get_transcription import get_transcription
import shutil
import markdown2  # type: ignore

# Custom CSS with fixed markdown container styling
if "disabled" not in st.session_state:
    st.session_state.disabled = False


st.set_page_config(page_title="Video Transcription", page_icon="public/writing.ico")

hide_menu_style = """
<style>
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stAppDeployButton {display: none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}

    /* Custom styling for the download button */
    .stDownloadButton > button {
        width: 100%;
        max-width: 300px;
    }
    .stDownloadButton > button:hover {
        border-color: #28a745;
        color: #28a745;
    }
    .stDownloadButton > button:active {
        background-color: #1e7e34;
        color: white;
    }
    
    /* Fixed markdown container styling */
    .custom-markdown-container {
        background-color: #FFFDD0;
        color: black;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin: 10px 0;
        max-height: 300px;
        overflow-y: auto;
    }

    /* Style markdown content within container */
    .custom-markdown-container h1,
    .custom-markdown-container h2,
    .custom-markdown-container h3,
    .custom-markdown-container h4,
    .custom-markdown-container h5,
    .custom-markdown-container h6 {
        color: #333;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }

    .custom-markdown-container p {
        margin-bottom: 1em;
        line-height: 1.6;
    }

    .custom-markdown-container ul,
    .custom-markdown-container ol {
        margin-left: 1.5em;
        margin-bottom: 1em;
    }

    .custom-markdown-container code {
        background-color: #f0f0f0;
        padding: 2px 4px;
        border-radius: 3px;
    }

    .custom-markdown-container pre {
        background-color: #f0f0f0;
        padding: 1em;
        border-radius: 5px;
        overflow-x: auto;
    }
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

transcription_options = ["Word By Word", "Summary"]

# Set the title of the app
st.title("Video Transcription")

# Create a text input field
user_input = st.text_input("Enter the video URL:", disabled=st.session_state.disabled)
mode = st.selectbox(
    "Select mode of transcription",
    transcription_options,
    disabled=st.session_state.disabled,
)

# Create a button to trigger the processing
if st.button("Transcribe", disabled=st.session_state.disabled):
    # Ensure user has entered a URL
    if user_input:
        try:
            st.session_state.disabled = True
            # Initialize a placeholder for the progress and messages
            progress_bar = st.progress(0)
            msg = st.empty()

            # Step 1: Download audio
            msg.write("Downloading audio...")
            file_name = download_bilibili_audio(user_input)
            progress_bar.progress(50)  # Update progress to 50%

            # Step 2: Get transcription
            msg.write("Getting transcription...")
            transcription_text = get_transcription(file_name, mode)

            progress_bar.progress(100)  # Update progress to 100%

            # Convert markdown to HTML for display
            html_content = markdown2.markdown(transcription_text)

            # Display transcription
            st.markdown(
                f"""
                <div class="custom-markdown-container">
                    {html_content}
            """,
                unsafe_allow_html=True,
            )

            # Add download button
            st.download_button(
                label="Download Transcription",
                data=transcription_text,
                file_name="transcribe.txt",
                mime="text/plain",
            )
        except Exception as e:
            st.error(f"Error occured during transcription:{e}")
        finally:
            try:
                shutil.rmtree("downloads")
            except Exception:
                pass
            msg.empty()
            progress_bar.empty()
            st.session_state.disabled = False
    else:
        st.error("Please enter a valid video URL.")
