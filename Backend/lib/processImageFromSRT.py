import os,sys
import logging

from datetime import datetime
logger = logging.getLogger(__name__)

from lib.imageLib.imageGenerator import GenerateImage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

def parse_srt_time(t):
    """Convert SRT time format to datetime object."""
    return datetime.strptime(t, "%H:%M:%S,%f")

def generateImagePrompt(text):
    storyLanguage=gv.storyLanguage
    backgroundTheme = "This story is from India so Keep Indian theme and indian things in each prompt" if storyLanguage.lower() == 'hindi' else ""
    imagePrompt = f"image prompt in sdxl format, for the below text.\n{text}'. Please do not write any description or heading or 'Image Prompt' or number in output, I want only prompt. Write prompt in english language only. {backgroundTheme}"
    return imagePrompt

def processSRTFromImage(srtFilePath, outputFinalPath, key):

    time_diff_dict = {}
    totalDuration = 0

    with open(srtFilePath, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n\n')

    for block in content:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            number = int(lines[0].strip())
            time_range = lines[1].strip()
            text = ' '.join(lines[2:]).strip()

            start_time_str, end_time_str = time_range.split(' --> ')
            start = parse_srt_time(start_time_str)
            end = parse_srt_time(end_time_str)
            duration = (end - start).total_seconds()

            time_diff_dict[number] = duration
            totalDuration = totalDuration + duration
            if(getattr(gv, 'slidDurationInImage') and gv.slidDurationInImage >= 0) and (totalDuration >= gv.slidDurationInImage):
                break
            imagePrompt = generateImagePrompt(text)
            if imagePrompt:
                GenerateImage(imagePrompt, f"{outputFinalPath}/Images/", f"chapter_{key}_{number}")

    return time_diff_dict

# # Example usage
# srt_file_path = 'C:/Utkarsh/VideoGenerator/Channels/Agyat Gaathayein/shorts/Backend/lib/subtitleLib/output_clean.srt'
# durations = process_srt(srt_file_path)
# print("\nSubtitle Durations:")
# print(durations)
