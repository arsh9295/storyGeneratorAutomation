import json
import re
from pydub import AudioSegment
import math
from datetime import datetime

from storyGenerator import geminiStoryGenerator
from audioGenerator import generateVoice
from audioGeneratorHindi import generateVoiceHindi
from imageGenerator import GenerateImage
from videoEffect import createCombineImages
# from combineImages import createCombineImages
from combineAudio import combineAudioFiles
from createVideo import createVideoMviepy
from writeToDoc import writeContentToDoc
from generateSRT import generateSRTFromAudio
from addSubtitle import burn_subtitles_ffmpeg, burn_ass_subtitles
from createThumbnil import create_thumbnail_with_text
from generateASS import generateASSWithKaraoke
from addSubtitle import burn_ass_subtitles

import argparse

start_time = datetime.now()
print(f"Script started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Default values
# geminiKey = ''
# outputPath = 'E:/Youtube/Stories'

# Parse command line arguments
parser = argparse.ArgumentParser(description='Story Generator')
parser.add_argument('--api-key', help='API Key for Gemini')
parser.add_argument('--output-path', help='Output path for generated files')
parser.add_argument('--language', help='Story language')
parser.add_argument('--type', help='Story type')
parser.add_argument('--duration', help='Story duration')
parser.add_argument('--model', help='AI model')
parser.add_argument('--description', help='Story description')
parser.add_argument('--prompt', help='Story prompt')

args = parser.parse_args()

print("Command line arguments:", args)

ImageDurationInVideo=7

totalImageDurationApply = 0 # Default total image duration in seconds
additionalImagePath = None  # Path to additional image if needed

# Override defaults with command line arguments if provided
if args.api_key:
    geminiKey = args.api_key
if args.output_path:
    outputPath = args.output_path

storyType = args.type if args.type else 'short'
language = args.language if args.language else 'English'
if language.lower() == 'english':
    audioVoice = "am_echo"
elif language.lower() == 'hindi':
    audioVoice = "hm_omega"
aiModel = args.model if args.model else 'gemini-2.0-flash'
description = args.description if args.description else ''
prompt = args.prompt if args.prompt else ''

def readPromptFile(filePath):
    with open(filePath, 'r', encoding="utf-8") as file:
        content = file.read()
    return content

def generateTableOfContents(apiKey, language, storyType, model):
    tableIndexPromptFilePath = "../Input/Prompts/short/tableOfIndex.txt"
    promptContent = readPromptFile(tableIndexPromptFilePath)

    chapterDescriptionPromptFile = "../Input/Prompts/short/chapterDescription.txt"
    chapterDescriptionContent = readPromptFile(chapterDescriptionPromptFile)

    storyNameFile = "../Input/storyName.txt"
    storyNameExists = readPromptFile(storyNameFile)

    formatted_content = eval(f"f'''{promptContent}\n{chapterDescriptionContent}'''")

    tableOfContents = geminiStoryGenerator(
        apiKey  = apiKey,
        prompt  = formatted_content,
        geminiModel  = model
    )
    return(tableOfContents)

def generateStory(storyPrompt, apiKey, model):
    storyOutput = geminiStoryGenerator(
        apiKey  = apiKey,
        prompt  = storyPrompt,
        geminiModel  = model
    )
    return(storyOutput)

def generateImagePrompt():
    imagePrompt = geminiStoryGenerator(
        apiKey  = geminiKey,
        prompt  = 'Write a story about Gemini',
        geminiModel  = 'gemini-2.0-flash-thinking-exp'
    )
    return(imagePrompt)

def getImageList(folderPath):
    import os
    imageList = [os.path.join(folderPath, file)
                 for file in os.listdir(folderPath)
                 if file.lower().endswith('.png')]
    return imageList

tableOfIndex = generateTableOfContents(geminiKey, language, storyType, aiModel)

if tableOfIndex:
    json_string = tableOfIndex.replace("```json", "").replace("```", "").strip()

    try:
        chapter_dict = json.loads(json_string)                
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

    storyNameFile = "../Input/storyName.txt"
    storyNameExists = readPromptFile(storyNameFile)

    generate_index = chapter_dict

    story_name = generate_index.get('novel_name', 'Untitled Novel')
    print(f"Story name: {story_name}")

    if story_name in storyNameExists:
        story_name = story_name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    finalPath = f"{outputPath}/{language}/{storyType}/{story_name}/"

    writeContentToDoc(f"{finalPath}/Docs/story.docx", story_name)
    # writeContentToDoc(f"{finalPath}/Docs/story.docx", generate_index)

    # Generate description for the story
    descriptionPromptFile = "../Input/Prompts/short/descriptionPrompt.txt"
    descriptionPromptContent = readPromptFile(descriptionPromptFile)
    formattedDescriptionContent = eval(f"f'''{descriptionPromptContent}'''")
    storyDescription = generateStory(formattedDescriptionContent, geminiKey, aiModel)
    if storyDescription:
        writeContentToDoc(f"{finalPath}/Docs/storyDescription.docx", storyDescription)

    with open('../Input/storyName.txt', "a", encoding='utf-8') as file:
        file.write(story_name + "\n") 

    # if language.lower() == 'english':
    #     generatedTitleVoice = generateVoice(story_name, f"{finalPath}/Audio/", f"chapter_0", audioVoice)
    # if language.lower() == 'hindi':
    #     generatedVoice = generateVoiceHindi(story_name, f"{finalPath}/Audio/", f"chapter_0", audioVoice)

    # firstImagePrompt = generateStory(f"generate realestic image prompts for story name {story_name}", geminiKey, aiModel)
    # titleImageGen = GenerateImage(f"{firstImagePrompt}", f"{finalPath}/Images/", f"chapter_0_0")
    # generateThumbnail = create_thumbnail_with_text(
    #     image_path=f"{finalPath}/Images/chapter_0_0.png",
    #     output_path=f"{finalPath}/Images/chapter_0_0.png",
    #     title_text=f"{story_name}",
    #     subtitle_text=None,
    #     font_path_bold="arialbd.ttf",        # Bold font for title
    #     font_path_regular="arial.ttf",        # Regular font for subtitle
    #     vAlign="center",
    #     yOffset=0,
    #     fill=(255, 255, 255),
    #     outlineColor=None,
    #     outlineWidth=2
    # )
    # finalPath = f"{outputPath}/{story_name}/{language}/{storyType}/"

    # imageList = []
    ImagesOnVideoDefined = False
    if generate_index:
        storyPromptContent = ""
        # Process each chapter
        for key, value in generate_index.items():
            if key != 'novel_name':  # Skip the novel name entry
                if isinstance(value, dict) and 'title' in value:
                    storyPromptFile = "../Input/Prompts/short/storyPrompt.txt"
                    storyPromptContent = readPromptFile(storyPromptFile)
                    formattedContent = eval(f"f'''{storyPromptContent}'''")
                    storyPrompt = formattedContent
                    print(f"Generating story for chapter {key}...")
                    generatedStory = generateStory(storyPrompt, geminiKey, aiModel)
                    if generatedStory:
                        # Generate voice for the story
                        writeContentToDoc(f"{finalPath}/Docs/story.docx", generatedStory)
                        if language.lower() == 'english':
                            generatedVoice = generateVoice(generatedStory, f"{finalPath}/Audio/", f"chapter_{key}", audioVoice)
                        if language.lower() == 'hindi':
                            generatedVoice = generateVoiceHindi(generatedStory, f"{finalPath}/Audio/", f"chapter_{key}", audioVoice)

                        audio = AudioSegment.from_file(generatedVoice)  # or .wav, .ogg, etc.
                        duration_seconds = len(audio) / 1000  # pydub returns length in milliseconds
                        print(f"Duration: {duration_seconds} seconds for chapter {key}")

                        # Dynamically calculate image duration
                        imageNumber = math.ceil(duration_seconds / ImageDurationInVideo)  # Assuming 5 seconds per image
                        image_duration = duration_seconds / imageNumber
                        print(f"Number of images to generate: {imageNumber} for chapter {key}")
                        print(f"Calculated image duration: {image_duration} seconds")

                        # Generate image prompt
                        imagePromptFile = "../Input/Prompts/short/ImagePromtp.txt"
                        imagePromptContent = readPromptFile(imagePromptFile)
                        formattedImagePromptContent = eval(f"f'''{imagePromptContent}'''")
                        imagePrompts = generateStory(formattedImagePromptContent, geminiKey, aiModel)
                        imagePrompts = re.sub(r'\n+', '\n', imagePrompts.strip())  # Remove extra newlines
                        print(f"Number of image prompts: {len(imagePrompts)} for chapter {key}")
                        writeContentToDoc(f"{finalPath}/Docs/prompts.docx", imagePrompts)
                        if totalImageDurationApply > 0:
                            ImagesOnVideoDefined = True
                            print(f"Images on video defined for chapter {key}")
                            if key == '1':
                                numberOfImagesToGenerate = math.ceil(totalImageDurationApply / ImageDurationInVideo)
                                count = 0
                                if imagePrompts:
                                    for number, line in enumerate(imagePrompts.split('\n')):
                                        if line.strip():
                                            count += 1
                                            if count > numberOfImagesToGenerate:
                                                break
                                            imageGen = GenerateImage(line.strip(), f"{finalPath}/Images/", f"chapter_{key}_{number}")
                        else:
                            print(f"Total image duration is 0")
                            if imagePrompts:
                                for number, line in enumerate(imagePrompts.split('\n')):
                                    if line.strip():
                                        imageGen = GenerateImage(line.strip(), f"{finalPath}/Images/", f"chapter_{key}_{number}")

    # Generate video from images
    imageList = getImageList(f"{finalPath}/Images/")
    combineAudioFiles(f"{finalPath}/Audio/", f"{finalPath}/Audio/combined/combined_audio.mp3")
    total_audio_duration = AudioSegment.from_file(f"{finalPath}/Audio/combined/combined_audio.mp3").duration_seconds
    # createCombineImages(imageList, f"{finalPath}/Videos/chapter_video.mp4", ImageDurationInVideo, total_audio_duration, ImagesOnVideoDefined, additionalImagePath, transition_duration=1)

    createCombineImages(
            image_paths=imageList,
            output_path=f"{finalPath}/Videos/chapter_video.mp4",
            image_duration=ImageDurationInVideo,
            audio_duration=total_audio_duration,
            ImagesOnVideoDefined=ImagesOnVideoDefined,
            additionalImagePath=additionalImagePath,
            transition_duration=1,
            fps=30
        )

    createVideoMviepy(f"{finalPath}/Videos/chapter_video.mp4", f"{finalPath}/Audio/combined/combined_audio.mp3", f"{finalPath}/Videos/final_video.mp4")

    # Generate karaoke-style ASS subtitle file
    generateASSWithKaraoke(
        f"{finalPath}/Audio/combined/combined_audio.mp3",
        f"subtitles.ass"
    )

    # Burn .ass subtitles into the final video
    burn_ass_subtitles(
        f"{finalPath}/Videos/final_video.mp4",
        f"subtitles.ass",
        f"{finalPath}/Videos/final_video_with_subtitles.mp4"
    )

    # Thumbnail Image
    thumbnailImageGen = GenerateImage(f"Create a realistic thumbnail image for the story name '{story_name}'", f"{finalPath}/Images/", f"thumbnail")
    generateThumbnail = create_thumbnail_with_text(
        image_path=f"{finalPath}/Images/thumbnail.png",
        output_path=f"{finalPath}/Images/final_thumbnail.png",
        title_text=f"{story_name}",
        subtitle_text="A Supernatural Story",
        font_path_bold="arialbd.ttf",        # Bold font for title
        font_path_regular="arial.ttf"        # Regular font for subtitle
    )

# Record end time
end_time = datetime.now()
print(f"Script ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Calculate and print duration
duration = end_time - start_time
print(f"Total duration: {duration}")