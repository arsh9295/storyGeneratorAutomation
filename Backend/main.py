import os
import json
import logging

import globalVariables as gv
from lib.generateVideoWithImage import generateVideoWithImages
from lib.processVideoSubtitle import videoSubtitle
from lib.generateThumbnil import createThumbnil
from lib.audioLib.combineAudio import combineAudioFiles
from lib.subtitleLib.generateSubtitle import generateASSWithKaraoke
from lib.subtitleLib.convertAssToSrt import convertAssToSrtManual
from lib.processImageFromSRT import processSRTFromImage
from lib.videoLib.youtubeUpload import initializeUpload
from datetime import datetime

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        #logging.FileHandler("app.log"),    # Log to a file
        logging.StreamHandler()            # Log to console
    ]
)

videoGenerationMode = gv.videoGenerationMode if getattr(gv, 'videoGenerationMode', None) else "FromTableOfIndex"

start_time = datetime.now()

if videoGenerationMode == "FromTableOfIndex":
    tableOfIndexPromptFile= gv.tableOfIndexPromptFile
    if tableOfIndexPromptFile is not None or (os.path.exists(tableOfIndexPromptFile) and os.path.getsize(tableOfIndexPromptFile) != 0):
        logging.info("Found Process with Table of Index..Moving ahead")
        from lib.proceedWithTableOfIndex import proceedWithTableOfIndex
        storyName, storyTitle, finalPath = proceedWithTableOfIndex()
    else:
        raise ValueError(f"Provided table of index prompt file '{tableOfIndexPromptFile}' is not valid or does not exist.")
elif videoGenerationMode == "FromStoryGeneratedFile":
    storyFilePath= gv.storyFilePath
    if storyFilePath is not None or (os.path.exists(storyFilePath) and os.path.getsize(storyFilePath) != 0):
        logging.info("Found Process with Story File..Moving ahead")
        from lib.proceedWithStoryFile import proceedWithStoryFile
        storyName, storyTitle, finalPath = proceedWithStoryFile()
    else:
        raise ValueError(f"Provided table of index prompt file '{storyFilePath}' is not valid or does not exist.")
elif videoGenerationMode == "FromStoryPrompt":
    storyPromptFile= gv.storyPromptFile
    if storyPromptFile is not None or (os.path.exists(storyPromptFile) and os.path.getsize(storyPromptFile) != 0):
        logging.info("Found Process with story prompt file..Moving ahead")
        from lib.proceedWithStoryPrompt import proceedWithStoryPrompt
        storyName, storyTitle, finalPath = proceedWithStoryPrompt()
    else:
        raise ValueError(f"Provided table of index prompt file '{storyPromptFile}' is not valid or does not exist.")
else:
    raise ValueError("Invalid Video Generation Mode: expected a value from FromStoryGeneratedFile, FromStoryPrompt, FromTableOfIndex")

# storyName = "Name is: TheAetheriumEcho"
# storyTitle = "Grief-stricken Elara steals a Lens, facing spirits and the Shade King. A dark pact leads to a choice: protect the Veil or succumb to darkness."
# finalPath = "E:/Youtube/Stories/test/english/supernatural/TheAetheriumEcho/"

logging.info(f"Story Name is: {storyName}")
logging.info(f"Story Title is: {storyTitle}")
logging.info(f"Story Path is: {finalPath}")

# Combine Audio
createCombineAudio = combineAudioFiles(f"{finalPath}/Audio/", f"{finalPath}/Audio/combined/combined_audio.mp3")

if gv.addSubtitle:
    logging.info(f"Generating and adding subtitle")
    storyName = storyName.strip()
    subTitleFileName = storyName.replace(" ","_")
    # Generate SRT
    genneeratesrtout = generateASSWithKaraoke(f"{finalPath}/Audio/combined/combined_audio.mp3", f"{subTitleFileName}_subtitles.ass")
    print(f"Hello: {genneeratesrtout}")

print(f"Hello world ! {genneeratesrtout}")

imageDuration = None

if (gv.addSubtitle) and (gv.createImageFromSRT):
    # Generate Image if from SRT
    convertAssToSrtManual(f"{subTitleFileName}_subtitles.ass", f"{subTitleFileName}_subtitles.srt")
    imageDuration = processSRTFromImage(f"{subTitleFileName}_subtitles.srt", f"{finalPath}", "1")

# Generate Video
generateVideoWithImages(finalPath, imageDuration)

# Generate Subtitle
if gv.addSubtitle:
    logging.info(f"Generating and adding subtitle")
    subTitleFileName = storyName.replace(" ","_")
    videoSubtitle(f"{finalPath}/Audio/combined/combined_audio.mp3", f"{subTitleFileName}_subtitles.ass", f"{finalPath}/Videos/final_video.mp4", f"{finalPath}/Videos/final_video_with_subtitles.mp4")

# Generate Thumbnil
if gv.generateThumbnil:
    logging.info(f"Generating Thumbnil")
    generateThumbnail = createThumbnil( prompt=f"{storyTitle}", imageFileName = "thumbnail", finalImageFileName = "final_thumbnail.png", image_path=f"{finalPath}/Images/", title_text=f"{storyTitle}")

if getattr(gv, 'uploadToYoutube') and gv.uploadToYoutube == True:
    initializeUpload()
# Record end time
end_time = datetime.now()

# Calculate and print duration
duration = end_time - start_time
logging.info(f"Total duration In Video Generation: {duration}")