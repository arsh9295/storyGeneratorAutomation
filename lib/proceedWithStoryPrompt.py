import logging
import os, sys, re
import math
from datetime import datetime
from pydub import AudioSegment

logger = logging.getLogger(__name__)

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

from lib.utilLib.readDocFile import readDocx
from lib.utilLib.readFiles import readPromptFile
from lib.audioLib.audioGenerator import audioGenerator
from lib.chatbotLib.chatBot import chatBotOutput
from lib.proceedWithTableOfIndex import processingImage
from lib.chatbotLib.chatBot import chatBotOutput


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

def getStoryText():
    if (getattr(gv, 'storyText') and gv.storyText != "" or gv.storyText != None):
        story = gv.storyText
    elif(os.path.isfile(gv.storyFile) and os.path.getsize((gv.storyFile))):
        if gv.storyFile.endswith("docx"):
            story = readDocx(gv.storyFile)
            return story
        elif gv.storyFile.endswith("txt"):
            story = readPromptFile(gv.storyFile)
            return story
        else:
            raise ValueError("Supported format of story file are docx and txt")
    else:
        raise ValueError("One parameter either storyText or storyFile is required for videoGenerationMode='FromStoryGeneratedFile'")

def processAudio(generatedStory, audioOutputPath, chapetrName, key):
    audioOutputPath = f"{audioOutputPath}/Audio"
    audioGenerator(
        generatedStory, audioOutputPath, chapetrName 
    )

    logging.info(f"Voice {chapetrName}.wav Generated")

    generatedVoice = f"{audioOutputPath}/{chapetrName}.wav"

    audio = AudioSegment.from_file(generatedVoice)  # or .wav, .ogg, etc.
    duration_seconds = len(audio) / 1000  # pydub returns length in milliseconds
    logging.info(f"Duration: {duration_seconds} seconds for chapter {key}")
    return duration_seconds

def generateStoryName(storyText):
    if (getattr(gv, 'storyName') and (gv.storyName != "" or gv.storyName != None)):
        storyName = gv.storyName
    else:
        alreadyExistingName = readPromptFile(gv.storyNameFile).replace('\n', '').split(',')
        storyName = chatBotOutput(gv.chatBotKey, gv.chatBotModel, prompt=f"Generate a catchy story name for below story in {gv.storyLanguage} language. Do not give multiple options or do not write unnessery text. only generate story name in mention language only not other language should be there. do not put astrik to make it bold. do not add new line, do not add any spaical character in name like ', :, etc \n {storyText} \n Name should not be any of {alreadyExistingName}")

        storyName = re.sub(r'[^A-Za-z0-9 ]', '', storyName)

        if storyName in gv.storyNameFile:
            story_name_folder = storyName + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            story_name_folder = storyName

        with open(gv.storyNameFile, "a", encoding='utf-8') as file:
            file.write(storyName + "\n")    

    storyTitle = chatBotOutput(gv.chatBotKey, gv.chatBotModel,  prompt=f"Generate a single, engaging summary for the story below in the form of a suspenseful or thought-provoking question. The question must be under 100 characters and should hint at the core conflict or mystery of the story without giving away the ending. Use a tone that creates curiosity, such as 'What happens when...' or 'Can she escape...?' or 'Will they survive...?'. In {gv.storyLanguage} language. Do not give multiple options or do not write unnessery text. only generate story name in mention language only not other language should be there. do not put astrik to make it bold. do not add new line \n {storyText}")
    return storyName.strip(), storyTitle.strip(), story_name_folder.strip()


def proceedWithStoryPrompt():
    prompt = gv.storyPrompt if(getattr(gv, 'storyName') and gv.storyPrompt != "" or gv.storyPrompt != None) else None
    PromptFiles = gv.storyPromptFile if (os.path.exists(gv.storyPromptFile) and os.path.getsize(gv.storyPromptFile) != 0) or gv.storyPromptFile is not None else None
    
    if prompt == None and PromptFiles == None:
        raise ValueError("storyPromptFile or storyPrompt Required !")

    print(f"Prompt file is {PromptFiles}")
    print(f"Prompt is {prompt}")

    storyText = chatBotOutput(gv.chatBotKey, gv.chatBotModel, [PromptFiles], prompt)
    if storyText:
        storyName, storyTitle, story_name_folder = generateStoryName(storyText)
        finalOutputPath = f"{gv.outputPath}/{story_name_folder}"
        print(f"final Output Path: {finalOutputPath}")
        generatedAudioDuration = processAudio(storyText, finalOutputPath, storyName, 1)
        generatefromsrt = (getattr(gv, 'createImageFromSRT') and (gv.createImageFromSRT)) and (gv.addSubtitle)
        if not(generatefromsrt):
            processingImage(generatedAudioDuration, finalOutputPath, "1", storyText)
        return storyName, storyTitle, finalOutputPath