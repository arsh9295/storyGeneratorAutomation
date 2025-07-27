from gradio_client import Client, handle_file
import shutil
import os
import logging

logger = logging.getLogger(__name__)

def generateVoice(inputText, storyPath, fileName, voiceName="am_echo", remove_silence=True, minimum_silence=0.05):
    try:
        # client = Client("http://127.0.0.1:7860/")
        client = Client("http://127.0.0.1:9000/")
        result = client.predict(
                text=inputText,
                model_name="kokoro-v0_19.pth",
                voice_name=voiceName,
                speed=0.85,
                pad_between_segments=0.3,
                remove_silence=True,
                minimum_silence=0.05,
                custom_voicepack=None,
                api_name="/text_to_speech"
                # api_name="/KOKORO_TTS_API"
                # autoplay=True,
                # api_name="/toggle_autoplay"        
        )
        if result:
            fileName = moveFile(result, fr"{storyPath}/{fileName}.wav")
            return fileName
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def moveFile(source_path, destination_path):
    try:
        # Ensure the source file exists
        if not os.path.isfile(source_path):
            logger.error(f"Source file does not exist: {source_path}")
            return

        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Move the file
        shutil.move(source_path, destination_path)
        # print(f"File moved from {source_path} to {destination_path}")
        return destination_path
    except Exception as e:
        print(f"Error: {e}")
