import os
from gtts import gTTS

def text_to_speech(text: str, filename: str = "caption_audio.mp3") -> str:
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def play_audio(filename: str):
    # This will be handled by Streamlit media player
    pass
