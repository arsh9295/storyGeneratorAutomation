from pydub import AudioSegment

# from combineImages import createCombineImages
from combineAudio import combineAudioFiles
from createVideo import createVideoMviepy
from addSubtitle import burn_subtitles_ffmpeg
from audioGeneratorHindi import generateVoiceHindi
from createThumbnil import create_thumbnail_with_text
from generateSRT import generateSRTFromAudio
from imageGenerator import GenerateImage
from videoEffect import createCombineImages

# finalPath = f"E:/Youtube/Stories/English/Supernatural/Veil of Whispers/"

# ImageDurationInVideo=5

# totalImageDurationApply = 0 # Default total image duration in seconds
# additionalImagePath = None  # Path to additional image if needed
# ImagesOnVideoDefined = False

# def getImageList(folderPath):
#     import os
#     imageList = [os.path.join(folderPath, file)
#                  for file in os.listdir(folderPath)
#                  if file.lower().endswith('.png')]
#     return imageList

# imageList = getImageList(f"{finalPath}/Images/")

def readPromptFile(filePath):
    with open(filePath, 'r', encoding="utf-8") as file:
        content = file.read()
    return content


storyNameFile = "../Input/storyName.txt"
storyNameExists = readPromptFile(storyNameFile)

string_to_check = "Utkarsh"

if string_to_check in storyNameExists:
    print("Found!")
else:
    print("Not found.")