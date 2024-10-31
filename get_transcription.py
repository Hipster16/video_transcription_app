import os
import google.generativeai as genai  # type: ignore
from typing import Optional
from google.generativeai.files import file_types


def prompt_selector(mode: str) -> str:
    """Selects the appropriate prompt based on the given mode.

    Args:
        mode (str): The mode for the transcription, either "transcribe text" or "Summary".

    Returns:
        str: The selected prompt for the specified mode.
    """
    if mode == "Word By Word":
        return """Detect the language in the audio file provided and transcribe it to English, ensuring each full sentence is displayed in a Markdown list format compatible with Streamlit. Each sentence should appear as a single bullet point, as shown in the example below:

        Recently, just about to come out of 22 years old young Maldini, leg length is 11, compared to previous Maldini, they are all longer.
        So I'll use August 15th latest updated original data base package out the model file.

        """
    elif mode == "Summary":
        return """
#     give me a descriptive summary of the topics along with the actual transcription that is discussed. I want the output to be summary of the text that is being said and the time intervals in the video at with that is mentioned.
#     sample output

# 0:00 - 0:35: Introduction and Overview

#  The speaker introduces the topic of the video: an analysis of the impact of various game mechanics on dribbling in FIFA.
#  He mentions that the free trial for FIFA is ending soon and that he's releasing his analysis. 
#  He notes the complexity of the analysis and that he is trying to present the most crucial conclusions in a clear and concise way.
#  He wants to help viewers understand the key factors that influence dribbling.

# 0:36 - 1:00: Dribbling Speed and Touch

#  0:36 - 0:37: The first point is that dribbling speed and touch are both essential.
#  0:38 - 0:41: The speaker explains that a player's touch when dribbling plays a significant role.
#  0:42 - 0:46: He emphasizes that the frequency of a player's touch is more important than speed, giving a ratio of 5:4.
#  0:47 - 0:52: The speaker explains that dribbling speed can indirectly affect the accuracy of the dribble. 
#  0:53 - 1:00: He explains that the game's design prioritizes touch over speed and that the "speed burst" mechanic is more about quick acceleration than actual top speed. 

# 1:01 - 1:20: Dribbling Speed Burst

#  1:01 - 1:10: The speaker describes the mechanics of how a player accelerates in the game, including the difference between "slow dribbling" and "fast dribbling."
#  1:11 - 1:16: He explains that the distance a player needs to reach full speed is shorter than the distance needed to reach top speed.
#  1:17 - 1:20: The speaker emphasizes that a player's touch and reaction time are crucial for reaching top speed. 

# 1:21 - 1:37: Touch Frequency and Dribbling Skill

#  1:21 - 1:23:  He explains that touch frequency influences the responsiveness of the dribble.
#  1:24 - 1:29: The speaker defines the "touch frequency" as the time it takes the player to react to the controls.
#  1:30 - 1:32: The speaker explains that this reaction time affects how a player can perform other actions.
#  1:33 - 1:37:  He explains that a longer touch frequency means longer reaction times, which can lead to slower reactions in various situations.

# 1:38 - 2:00: Touch Frequency, Reaction Time, and Responsiveness

#  1:38 - 1:49: The speaker connects touch frequency with a player's ability to perform various actions like passing, tackling, and changing direction while dribbling.
#  1:50 - 1:52: The speaker re-emphasizes that touch frequency plays a vital role in the feel of dribbling.
#  1:53 - 1:59: He explains that a higher touch frequency makes dribbling faster and more responsive.
#  2:00 - 2:02: Higher touch frequency also helps the player to be more agile and avoid interceptions.

# 2:03 - 2:14: Touch Frequency and Player Height

#  2:03 - 2:10: The speaker explains that player height affects touch frequency, even at the same "touch" statistic. 
#  2:11 - 2:14: He suggests that taller players benefit more from higher touch frequencies. 

# 2:15 - 2:28: Game Design and Dribbling Speed

#  2:15 - 2:17: The speaker highlights the game's design philosophy for dribbling. 
#  2:18 - 2:22: He explains that the game's engine simply combines speed and dribbling statistics into a single number that governs dribbling.
#  2:23 - 2:27: He notes that the game doesn't have a separate mechanic for players with high speed but low touch or vice versa. 
#  2:28 - 2:31: The speaker acknowledges that this design simplifies the game but leads to odd results.
#   """

    else:
        return ""


def upload_to_gemini(path: str, mime_type: Optional[str] = None) -> file_types.File:
    """Uploads a file to the Gemini API.

    Args:
        path (str): The path to the file to be uploaded.
        mime_type (Optional[str]): The MIME type of the file (default is None).
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


def get_transcription(file_name: str, transcription_mode: str) -> str:
    """Generates a transcription of the specified audio file using the Gemini API.

    Args:
        file_name (str): The name of the audio file to be transcribed.
        transcription_mode (str): The mode for transcription (e.g., "transcribe text" or "Summary").

    Returns:
        str: The transcription result as text.
    """
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=prompt_selector(transcription_mode),
    )

    # Upload the audio file to Gemini
    files = [
        upload_to_gemini(f"downloads/{file_name}", mime_type="audio/mpeg"),
    ]

    # Start a chat session with the model
    chat_session = model.start_chat()

    # Send the uploaded file and get the transcription response
    response = chat_session.send_message(files[0])
    return response.text or ""
