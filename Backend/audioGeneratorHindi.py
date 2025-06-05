from gradio_client import Client, handle_file
import shutil
import os

def generateVoiceHindi(inputText, storyPath, fileName, voiceName="am_echo"):
    try:
        client = Client("http://127.0.0.1:7860/")
        result = client.predict(
                text=inputText,
                Language="Hindi",
                voice="hm_omega",
                speed=0.85,
                # pad_between_segments=0.3,
                translate_text=False,
                remove_silence=False,
                api_name="/KOKORO_TTS_API_1"
        )        
        print(f"Result: {result}")
        if result:
            fileName = moveFile(result[0], fr"{storyPath}/{fileName}.wav")
            return fileName
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def moveFile(source_path, destination_path):
    try:
        # Ensure the source file exists
        if not os.path.isfile(source_path):
            print(f"Source file does not exist: {source_path}")
            return

        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Move the file
        shutil.move(source_path, destination_path)
        print(f"File moved from {source_path} to {destination_path}")
        return destination_path
    except Exception as e:
        print(f"Error: {e}")
