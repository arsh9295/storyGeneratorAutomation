from pydub import AudioSegment
import os
import re
import logging
import subprocess

logger = logging.getLogger(__name__)

def boost_volume(input_path, output_path, multiplier=4.0):
    """
    Uses ffmpeg to boost volume of audio file.
    """
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)  # ✅ Ensure directory exists

    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-filter:a", f"volume={multiplier}",
            output_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg volume boost failed: {e}")
        raise

def combineAudioFiles(audio_folder, output_file="combined_audio.mp3", boost=True, boost_multiplier=4.0):
    supported_formats = ('.mp3', '.wav', '.ogg', '.flac', '.aac')

    os.makedirs(audio_folder, exist_ok=True)

    audio_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(supported_formats)]

    def sort_key(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else filename.lower()

    audio_files.sort(key=sort_key)

    combined = AudioSegment.empty()

    for file in audio_files:
        audio_path = os.path.join(audio_folder, file)
        logger.info(f"🔊 Adding: {file}")
        audio = AudioSegment.from_file(audio_path)
        combined += audio

    # Temp WAV path
    temp_wav_path = os.path.join(audio_folder, "temp_combined.wav")
    combined.export(temp_wav_path, format="wav")
    logger.info(f"✅ Temp combined audio saved: {temp_wav_path}")

    final_output_path = os.path.join(audio_folder, output_file)

    # Ensure output dir exists
    os.makedirs(os.path.dirname(final_output_path), exist_ok=True)  # ✅ Fix for your error

    if boost:
        boost_volume(temp_wav_path, final_output_path, multiplier=boost_multiplier)
        logger.info(f"🚀 Boosted and saved final audio: {final_output_path}")
    else:
        combined.export(final_output_path, format="mp3")
        logger.info(f"✅ Combined audio (no boost) saved: {final_output_path}")

    os.remove(temp_wav_path)
    return final_output_path
