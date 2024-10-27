import yt_dlp
from typing import Optional
import hashlib
import os


def download_bilibili_audio(url: str, output_path: str = 'downloads/', audio_format: str = 'mp3') -> str:
    """
    Downloads audio from a given Bilibili video URL and saves it in the specified format.

    This function utilizes yt-dlp to download only the audio from a Bilibili video.
    It converts the audio into a user-specified format (default is mp3) and saves it to a given directory.

    Args:
        url (str): The URL of the Bilibili video to download the audio from.
        output_path (str, optional): The directory where the audio file will be saved. Defaults to 'downloads/'.
        audio_format (str, optional): The desired audio format for the output file (e.g., 'mp3', 'm4a', 'wav'). Defaults to 'mp3'.

    Raises:
        ValueError: If an invalid audio format is provided.
    """
    # Supported audio formats for validation
    supported_formats = {"mp3", "m4a", "wav"}

    os.makedirs("downloads", exist_ok=True)

    if audio_format not in supported_formats:
        raise ValueError(f"Invalid audio format '{audio_format}'. Supported formats are: {', '.join(supported_formats)}")

    # yt-dlp options to download only audio and convert to the desired format
    md5_hash = hashlib.md5(url.encode()).hexdigest()
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best available audio
        'outtmpl': f'{output_path}{md5_hash}.%(ext)s',  # Set the output filename format
        'postprocessors': [{  # Postprocess the audio file
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,  # Convert to the desired format (e.g., mp3)
            'preferredquality': '192',# Set audio quality (in kbps)
        }],
        "postprocessor_args":['-ar', '16000'],  # Set the audio sample rate to 16 kHz
        'noplaylist': True,  # Only download a single video if it's part of a playlist
    }

    # Use yt-dlp to download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio from {url}...")
        ydl.download([url])
        return md5_hash+"."+audio_format