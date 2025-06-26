import os
import logging

logger = logging.getLogger(__name__)
from lib.utilLib.readFiles import readPromptFile

def chatBotOutput(apiKey, model, PromptFiles=None, prompt=None, useWeb=False, usePromptAndFiles=False):
    mergedContent = ""
    if PromptFiles:
        for PromptFile in PromptFiles:
            if not os.path.exists(PromptFile):
                logger.error(f"Prompt file {PromptFile} does not exist.")
            else:
                promptContent = readPromptFile(PromptFile)
                content = promptContent.strip()  # remove leading/trailing whitespace
                mergedContent += content + "\n"
        filePromptContents = eval(f"f'''{mergedContent}'''")
    if prompt:
        PromptContents = prompt

    if not PromptFiles and not prompt:
        raise ValueError("Either PromptFiles or prompt must be provided.")

    if usePromptAndFiles:
        if not PromptFiles:
            finalPrompt = f"{PromptContents}"
        elif not prompt:
            finalPrompt = f"{filePromptContents}"
        else:
            finalPrompt = f"{filePromptContents}\n{PromptContents}"
    else:
        finalPrompt = PromptContents if prompt else filePromptContents

    if 'gemini' in model.lower():
        from lib.chatbotLib.chatBotModels import geminiStoryGenerator
        generatedOutput = geminiStoryGenerator(apiKey, finalPrompt, model)
    elif 'gpt' in model.lower():
        from lib.chatbotLib.chatBotModels import openAIStoryGenerator
        generatedOutput = openAIStoryGenerator(apiKey, finalPrompt, model, useWeb)
    else:
        raise ValueError("Unsupported model type. Please use 'gemini' or 'gpt'.")
    return(generatedOutput)
