from gradio_client import Client, handle_file
import shutil
import os

def generateVoice(inputText, storyPath, fileName):
    try:
        client = Client("http://127.0.0.1:9000/")
        result = client.predict(
                text=inputText,
                model_name="kokoro-v0_19.pth",
                voice_name="am_echo",
                speed=0.85,
                pad_between_segments=0.3,
                remove_silence=False,
                minimum_silence=0.05,
                custom_voicepack=None,
                api_name="/text_to_speech"
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
