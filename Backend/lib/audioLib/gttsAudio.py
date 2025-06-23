# Install dependencies:
# pip install gTTS playsound
import logging

logger = logging.getLogger(__name__)
from gtts import gTTS
# from playsound import playsound  # pure-Python player
import os

def text_to_speech(text: str, filepath, language, filename: str = "output_hindi.mp3", slow: bool = False, tld='co.in'):
    """
    Convert Hindi text to speech, save it, and play it.

    :param text: Text in Hindi (or any supported language)
    :param filename: Output MP3 filename
    :param slow: If True, speech will be slower
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    tts = gTTS(text=text, lang=language, slow=slow, tld=tld)
    tts.save(f"{filepath}/{filename}")
    logger.info(f"Saved voice to '{filepath}/{filename}'")
    # playsound(filename)

