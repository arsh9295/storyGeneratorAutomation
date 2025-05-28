import json
import re

from storyGenerator import geminiStoryGenerator
from audioGenerator import generateVoice
from imageGenerator import GenerateImage

geminiKey = 'your-gemini-api-key-here'

def readPromptFile(filePath):
    with open(filePath, 'r', encoding="utf-8") as file:
        content = file.read()
    return content

def generateTableOfContents(apiKey, language, storyType, model):
    tableIndexPromptFilePath = "../Input/Prompts/short/tableOfIndex.txt"
    promptContent = readPromptFile(tableIndexPromptFilePath)

    chapterDescriptionPromptFile = "../Input/Prompts/short/chapterDescription.txt"
    chapterDescriptionContent = readPromptFile(chapterDescriptionPromptFile)

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


# def generateImage():
#     pass

# def generateVoice():
#     pass


storyType = 'supernatural'
language = 'English'
tableOfIndex = generateTableOfContents(geminiKey, 'English', storyType, 'gemini-2.0-flash')

if tableOfIndex:
    json_string = tableOfIndex.replace("```json", "").replace("```", "").strip()

    try:
        chapter_dict = json.loads(json_string)                
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

    generate_index = chapter_dict

    story_name = generate_index.get('novel_name', 'Untitled Novel')
    print(f"Story name: {story_name}")

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
                    generatedStory = generateStory(storyPrompt, geminiKey, 'gemini-2.0-flash')
                    if generatedStory:
                        # Generate voice for the story
                        generatedVoice = generateVoice(generatedStory, story_name, f"chapter_{key}")
                        # Generate image prompt
                        imagePromptFile = "../Input/Prompts/short/ImagePromtp.txt"
                        imagePromptContent = readPromptFile(imagePromptFile)
                        formattedImagePromptContent = eval(f"f'''{imagePromptContent}'''")
                        imagePrompts =  generateStory(formattedImagePromptContent, geminiKey, 'gemini-2.0-flash')
                        # print(f"Generated image prompts for chapter {key}: {imagePrompts}")
                        if imagePrompts:
                            for number, line in enumerate(imagePrompts.split('\n')):
                                if line.strip():
                                    # print(f"{number}, {line.strip()}")
                                    # Generate image from the prompt
                                    GenerateImage(line.strip(), f"../Output/{story_name}/Images/chapter_{key}", f"{number}")