from pydub import AudioSegment
import os
import re
import logging

logger = logging.getLogger(__name__)

def combineAudioFiles(audio_folder, output_file="combined.wav"):
    # Supported audio formats
    supported_formats = ('.mp3', '.wav', '.ogg', '.flac', '.aac')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.join(audio_folder, output_file)), exist_ok=True)

    # Get all audio files with supported extensions
    audio_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(supported_formats)]

    # Define a smart sorting key: numeric if possible, otherwise fallback to filename
    def sort_key(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else filename.lower()

    # Sort audio files using the smart key
    audio_files.sort(key=sort_key)

    # print(f"🗂 Found {len(audio_files)} audio files:")
    # for i, f in enumerate(audio_files, 1):
    #     print(f"  {i}. {f}")

    # Initialize empty audio segment
    combined = AudioSegment.empty()

    # Load and concatenate
    for file in audio_files:
        audio_path = os.path.join(audio_folder, file)
        logger.info(f"🔊 Adding: {file}")
        audio = AudioSegment.from_file(audio_path)
        combined += audio

    # Export the final audio
    output_path = os.path.join(audio_folder, output_file)
    combined.export(output_path, format="wav")
    logger.info(f"✅ Combined audio saved to: {output_path}")
