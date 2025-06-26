import os,sys
import logging
import shutil

from datetime import datetime
logger = logging.getLogger(__name__)

from lib.imageLib.imageGenerator import GenerateImage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

def parse_srt_time(t):
    """Convert SRT time format to datetime object."""
    return datetime.strptime(t, "%H:%M:%S,%f")

def generateImagePrompt(text):
    imagePrompt = f'''
    Generate 1 highly detailed and vivid image prompts based on the story provided below. The prompts must follow the narrative sequence and capture key moments, emotions, and transitions in the story. Each prompt must visually describe a specific scene like a cinematic frame, with strong attention to atmosphere, lighting, and realism.
    For every character mentioned in the story (e.g., "Leena"), describe their appearance (age, facial features, hairstyle, clothing, and expression) in the first prompt where they appear. In all following prompts, keep their visual appearance consistent without repeating their full description — just refer to them naturally (e.g., "Leena stands near the window"). The same rule applies to key objects, buildings, creatures, or locations (e.g., “a rusty wooden cabin” should be described once, and referenced consistently thereafter).
    Avoid generic or symbolic descriptions — focus on realism and precise visual storytelling. Do not write any headings, descriptions, labels, or numbers. Only output 1 pure image prompts, one per line, in English.
    Story: '{text}'
    '''
    storyLanguage=gv.storyLanguage
    if storyLanguage.lower() == 'hindi':
        imagePrompt = f'''
        Generate exactly 1 highly detailed and vivid image prompts based on the story provided below. The prompts must follow the narrative sequence and capture key moments, emotions, and transitions in the story. Each prompt must visually describe a specific scene like a cinematic frame, with strong attention to atmosphere, lighting, and realism.
        All characters, locations, outfits, objects, and environments must reflect Indian cultural, social, and geographical context. This includes traditional Indian clothing (like sarees, kurtas, or school uniforms), Indian facial features, rural or urban Indian architecture, natural Indian landscapes, and authentic accessories or vehicles (such as auto-rickshaws, scooters, Indian temples, or banyan trees). 
        For every character mentioned in the story (e.g., "Leena"), describe their appearance (age, facial features, hairstyle, traditional attire, and expression) in the first prompt where they appear. In all following prompts, keep their visual appearance consistent without repeating the full description — just refer to them naturally (e.g., "Leena runs through the dusty street"). Do the same for recurring settings or objects — describe them in detail once, then reference them consistently.
        Avoid generic or symbolic visuals. Focus on cinematic realism and culturally grounded visual storytelling. Do not write any headings, descriptions, labels, or numbers. Only output 1 pure image prompts, one per line, in English.
        Story: '{text}'
        '''
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

    destination_path = os.path.dirname(f"{outputFinalPath}")
    shutil.move(srtFilePath, destination_path)
    return time_diff_dict

# # Example usage
# srt_file_path = 'C:/Utkarsh/VideoGenerator/Channels/Agyat Gaathayein/shorts/Backend/lib/subtitleLib/output_clean.srt'
# durations = process_srt(srt_file_path)
# print("\nSubtitle Durations:")
# print(durations)
