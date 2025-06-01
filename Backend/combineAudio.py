from pydub import AudioSegment
import os

def combineAudioFiles(audio_folder, output_file):
    # Directory containing audio files
    # audio_folder = "path_to_your_audio_files"  # Replace with your path
    # output_file = "combined_output.mp3"        # Change extension as needed

    # Supported audio formats (you can modify this list)
    supported_formats = ('.mp3', '.wav', '.ogg', '.flac', '.aac')

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Get all audio files in the directory
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith(supported_formats)]
    audio_files.sort()  # Optional: ensures files are combined in order

    # Initialize the final audio segment
    combined = AudioSegment.empty()

    # Combine each file
    for file in audio_files:
        audio_path = os.path.join(audio_folder, file)
        print(f"Adding {file}...")
        audio = AudioSegment.from_file(audio_path)
        combined += audio

    # Export the final combined audio
    output_path = os.path.join(audio_folder, output_file)
    combined.export(output_path, format="wav")  # You can change format
    print(f"\n✅ Combined audio saved as: {output_path}")
