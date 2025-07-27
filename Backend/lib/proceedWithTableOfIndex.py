import os, sys, json, re, math
from pydub import AudioSegment
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

from lib.chatbotLib.chatBot import chatBotOutput
from lib.utilLib.readFiles import readPromptFile
from lib.utilLib.writeToDoc import writeContentToDoc
from lib.audioLib.audioGenerator import audioGenerator
from lib.imageLib.imageGenerator import GenerateImage
from lib.processImageFromSRT import processSRTFromImage

def generateStoryForChapter(outputFinalPath, generatedIndex):
    for key, value in generatedIndex.items():
        if key != 'novel_name':  # Skip the novel name entry
            if isinstance(value, dict) and 'title' in value:
                storyOutputFile = f"{outputFinalPath}/Docs/story.docx"
                generatedStory = processChapterGenerateStory(storyOutputFile, storyPromptFile=gv.storyPromptFile, storyGenra=gv.storyGenra, storyLanguage=gv.storyLanguage, generatedIndex=generatedIndex, chapterTitle=value['title'], chapterDescription=value['description'], key=key, chatBotKey=gv.chatBotKey, chatBotModel=gv.chatBotModel)
                if generatedStory:
                    # Generate voice for the story
                    audioOutputPath = f"{outputFinalPath}/Audio/"
                    chapetrName = f"chapter_{key}"
                    audioDuration = processAudio(generatedStory, audioOutputPath, chapetrName, key)
                    generatefromsrt = (getattr(gv, 'createImageFromSRT') and (gv.createImageFromSRT)) and (gv.addSubtitle)
                    if audioDuration and not(generatefromsrt):
                        processingImage(audioDuration, outputFinalPath, key, generatedStory)

def processChapterGenerateStory(storyOutputFile, storyPromptFile=gv.storyPromptFile, **kwargs):
    storyGenra = kwargs['storyGenra']
    storyLanguage = kwargs['storyLanguage']
    generatedIndex = kwargs['generatedIndex']
    chapterTitle = kwargs['chapterTitle']
    chapterDescription = kwargs['chapterDescription']
    chatBotKey = kwargs['chatBotKey']
    chatBotModel = kwargs['chatBotModel']

    key = kwargs['key']
    if storyLanguage.lower() == 'english':
        wordCountStatement = f"- Word count should be around {gv.wordsPerChapter}" if gv.wordsPerChapter is not None else ""
        promptInstruction = f'''Create a {storyGenra} story chapter based on the following details:
        - The story is set in an {storyLanguage} speaking country. 
        - Index: {generatedIndex} 
        - Chapter title: {chapterTitle} 
        - Chapter description: {chapterDescription} 
        - Story context: This chapter is part of a larger {storyGenra} novel. 
        - Writing style: Deep, immersive and atmospheric, with vivid descriptions and {storyGenra} elements. 
        - Main elements to include: [Specify if any particular scene, character action or twist is required] 
        - Length: [Full chapter] 
        - The story language will be only in {storyLanguage}, so write in that language. 
        - The story output should have proper punctuation marks. For example, put appropriate commas, full stops, question marks etc. where necessary. Put according to the language chosen. 
        - Do not output chapter number or name or description, just write the story.
        {wordCountStatement}
        - double check if following proper instructions or not, especially regarding word count
        '''
    elif storyLanguage.lower() == 'hindi':
        wordCountStatement = f"- शब्द गणना लगभग {gv.wordsPerChapter} होनी चाहिए" if gv.wordsPerChapter is not None else ""
        promptInstruction=f'''निम्नलिखित विवरणों के आधार पर एक {storyGenra} कहानी अध्याय बनाएँ: 
        - कहानी एक {storyLanguage} भाषी देश में सेट है। 
        - विषय-सूची: {generatedIndex} 
        - अध्याय का शीर्षक: {chapterTitle} 
        - अध्याय का विवरण: {chapterDescription} 
        - कहानी का संदर्भ: यह अध्याय एक बड़े {storyGenra} उपन्यास का हिस्सा है। 
        - लेखन शैली: गहरा, गहन और वातावरण, विशद वर्णन और {storyGenra} तत्वों के साथ। 
        - शामिल करने के लिए मुख्य तत्व: [निर्दिष्ट करें कि क्या कोई विशेष दृश्य, चरित्र क्रिया या मोड़ आवश्यक है] 
        - लंबाई: [पूरा अध्याय] 
        - कहानी की भाषा केवल {storyLanguage} भाषा होगी, इसलिए उसी भाषा में लिखें। 
        - कहानी आउटपुट में उचित विराम चिह्न होने चाहिए। उदाहरण के लिए, जहाँ आवश्यक हो, उचित अल्पविराम, पूर्णविराम, प्रश्न चिह्न आदि लगाएँ। भाषा के अनुसार डालें, किसी भी चुनी गई भाषा के लिए। 
        - अध्याय संख्या या नाम या विवरण आउटपुट न करें, केवल कहानी लिखें।
        {wordCountStatement}
        - उचित निर्देशों का पालन किया जा रहा है या नहीं, इसकी दोबारा जांच करें, खासकर शब्द गणना के संबंध में
        '''
    
    if storyPromptFile is not None or (os.path.exists(storyPromptFile) and os.path.getsize(storyPromptFile) != 0):
        storyPromptContent = readPromptFile(storyPromptFile)
        storyPrompt = f"{promptInstruction}\n{storyPromptContent}"
    else:
        storyPrompt = f"{promptInstruction}"
    logging.info(f"Generating story for chapter {key}...")
    generatedStory = chatBotOutput(chatBotKey, chatBotModel, prompt=storyPrompt, useWeb=gv.useWebSearch)
    if generatedStory:
        writeContentToDoc(storyOutputFile, generatedStory)
        return generatedStory
    else:
        raise ValueError(f"Failed to generate story for chapter {key}. Please check the input parameters or the prompt file.")

def processAudio(generatedStory, audioOutputPath, chapetrName, key):
    audioGenerator(
        generatedStory, audioOutputPath, chapetrName 
    )

    logging.info(f"Voice {chapetrName}.wav Generated")

    generatedVoice = f"{audioOutputPath}/{chapetrName}.wav"

    audio = AudioSegment.from_file(generatedVoice)  # or .wav, .ogg, etc.
    duration_seconds = len(audio) / 1000  # pydub returns length in milliseconds
    logging.info(f"Duration: {duration_seconds} seconds for chapter {key}")
    return duration_seconds

def processingImage(audioDuration, outputFinalPath, key, generatedStory, perImageDuration=gv.perImageDuration, slidDurationInImage=gv.slidDurationInImage, chatBotKey=gv.chatBotKey, chatBotModel=gv.chatBotModel):

    # Dynamically calculate image duration
    imageNumber = math.ceil(audioDuration / perImageDuration) 
    logging.info(f"Number of images to generate: {imageNumber} for chapter {key}")

    promptInstruction = f'''
        Generate exact {imageNumber} image prompts, in stable diffusion sdxl format, for the below short story. Image prompts must follow the sequence of the story. You must divide the whole story into {imageNumber} equal parts by first calculating the number of characters in this story and then dividing it by {imageNumber}. After that, you will have {imageNumber} chunks of the whole story. Now, you will generate simple text-to-image prompts for those {imageNumber} chunks. Remember these rules while generating the prompts: 
        1. Include a mix of both, comma separated keywords AND natural language to write the prompts. 
        2. The AI image generator I use doesn't have memory/context feature, that is why it cannot refer to, or get information from any previous prompts. Therefore, make sure to mention everything (every description) in each and every prompt, regardless of if you've mentioned it before in some other prompt. You CAN'T use phrases like "his", "her", "same man", "same woman", etc. or any other such referring words. My AI image generator doesn't carry over details from previous prompts. I can't stress this enough. NEVER write things that connect to the previous or the next prompts. Each and every prompt MUST be unique and NOT related to any other prompt. REMEMBER that, you can have a bit of context and use his, her, their, etc. in one particular prompt, but NOT across different prompts. 
        3. Keep the prompts short and minimal, without any fluff, and use simple sentences, not complex ones. 
        4. Always describe the scene as a still frame frozen in time. Never describe a sequence of events. I need an image from the prompt, not a video. Keep that in mind. 
        5. If there's a scene that demands expressions on the characters' face, make it highly exaggerated. Dial the expressions to 11. 
        6. Make sure to describe the characters' appearance, like their hair color, hair style, clothing type and appearance, age, body type, ethnicity (Caucasian), etc. and more such things, please be descriptive, along with the name as mentioned in the exerpt, and also describe the overall scene (environment, lighting, etc. be descriptive here too) in detail. Do this in each and every prompt, regardless of using it in another prompt. I want the same character's (whoever the character or scene may be) description in all of the prompts again and again. For example if a person's hair is curly, mention it in each and every prompt. 
        7. Mention the images to be anime, cartoon, and digital art style, and add the appropriate keywords in the very beginning of the prompts.
        8. Keep the prompts very short.
        NOTE: Please follow each and every rule while generating the prompts.If you forget any of the rules, I will deduct points in your name. Please do not write any description or heading or "Image Prompt" or number in output. I want only prompts seprated by new lines.
        Now, start creating image prompts for the followng short story: {generatedStory} 
    '''
    storyLanguage=gv.storyLanguage
    if storyLanguage.lower() == 'hindi':
        promptInstruction = f'''
        Generate exactly {imageNumber} highly detailed and vivid image prompts based on the story provided below. The prompts must follow the narrative sequence and capture key moments, emotions, and transitions in the story. Each prompt must visually describe a specific scene like a cinematic frame, with strong attention to atmosphere, lighting, and realism.

        All characters, locations, outfits, objects, and environments must reflect Indian cultural, social, and geographical context—such as traditional sarees, kurtas, school uniforms; Indian facial features; rural or urban architecture; natural landscapes; and authentic elements like auto‑rickshaws, scooters, banyan trees, temple motifs, or monsoon skies.

        1. Character introductions:  
        - In the first prompt where each character appears (e.g., “Leena,” “Rahul,” “Inspector Meena”), include age, gender, skin tone, facial structure (eyes, nose, jaw), hairstyle, traditional attire, and expression or posture grounded in Indian style.  
        - In subsequent prompts, refer to the character naturally (e.g., “Leena leans against the temple wall,” “Rahul glances anxiously under his cap”) without re-listing their attributes.

        2. Setting and object consistency:  
        - Introduce each key location or object once with vivid Indian-specific detail (e.g., “a weathered red sandstone courtyard,” “a green auto-rickshaw parked under a neem tree,” “a brass oil lamp flickering in the veranda”).  
        - Later prompts may simply reference these as “the courtyard,” “the rickshaw,” “the lamp,” keeping their visual identity consistent.

        3. Cinematic realism:
        - Use culturally appropriate lighting and atmosphere—e.g., warm sunrise over fields, monsoon rain washing village lanes, dusk streetlights in Mumbai, temple incense smoke.  
        - Highlight textures: peeling plaster, woven textiles, muddy paths, sun-bleached walls.

        4. Formatting rules: 
        - Output exactly {imageNumber} pure prompts, each on a new line, in English.  
        - Do not include titles, numbers, labels, or extra commentary—just the scene descriptions.

        Story: '{generatedStory}'
        '''

    # Generate image prompt
    if (getattr(gv, 'imagePromptFile') and (gv.imagePromptFile != "" or gv.imagePromptFile != None)):
        imagePromptFile = gv.imagePromptFile

        if (os.path.exists(imagePromptFile) and os.path.getsize(imagePromptFile) != 0):
            imagePromptContentfile = readPromptFile(imagePromptFile)
            imagePromptContent = f"{promptInstruction}\n{imagePromptContentfile}"
    else:
        imagePromptContent = f"{promptInstruction}"

    formattedImagePromptContent = f"{imagePromptContent}"

    imagePrompts = chatBotOutput(chatBotKey, chatBotModel, prompt=formattedImagePromptContent, useWeb=False)

    imagePrompts = re.sub(r'\n+', '\n', imagePrompts.strip())  # Remove extra newlines

    writeContentToDoc(f"{outputFinalPath}/Docs/prompts.docx", imagePrompts)

    if slidDurationInImage > 0:
        ImagesOnVideoDefined = True
        logging.info(f"Images on video defined for chapter {key}")
        if key == '1':
            numberOfImagesToGenerate = math.ceil(slidDurationInImage / perImageDuration)
            count = 0
            if imagePrompts:
                for number, line in enumerate(imagePrompts.split('\n')):
                    if line.strip():
                        count += 1
                        if count > numberOfImagesToGenerate:
                            break
                        imageGen = GenerateImage(line.strip(), f"{outputFinalPath}/Images/", f"chapter_{key}_{number}")
    else:
        ImagesOnVideoDefined = False
        logging.info(f"Total image duration is 0")
        if imagePrompts:
            for number, line in enumerate(imagePrompts.split('\n')):
                if line.strip():
                    imageGen = GenerateImage(line.strip(), f"{outputFinalPath}/Images/", f"chapter_{key}_{number}")    

def processStoryName(generateIndex, storyNameFile=gv.storyNameFile):
    story_name = generateIndex.get('novel_name', 'Untitled Novel')
    logging.info(f"Story name: {story_name}")

    if gv.storyLanguage.lower() == 'english':
        story_name = re.sub(r'[^A-Za-z0-9 ]', '', story_name)

    storyNameExists = readPromptFile(storyNameFile).replace('\n', '').split(',')
    if story_name in storyNameExists:
        story_name_folder = story_name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        story_name_folder = story_name

    with open(storyNameFile, "a", encoding='utf-8') as file:
        file.write(story_name + "\n")
    return story_name, story_name_folder

def generateDescription(generatedIndex, descriptionOutputFile, descriptionPromptFile=None, chatBotKey=gv.chatBotKey, chatBotModel=gv.chatBotModel):
    # Generate description for the story
    promptInstruction = f"Generate a brief detailed description for the following story: \n {generatedIndex}"
    if (getattr(gv, 'descriptionPromptFile') and (gv.descriptionPromptFile != "" or gv.descriptionPromptFile != None)):
        descriptionPromptFile = gv.descriptionPromptFile
    if (os.path.exists(descriptionPromptFile) and os.path.getsize(descriptionPromptFile) != 0):
        descriptionPromptContent = readPromptFile(descriptionPromptFile)
        formattedDescriptionContent = f"{promptInstruction}/n{descriptionPromptContent}"
    else:
        formattedDescriptionContent = f"{promptInstruction}"
    storyDescription = chatBotOutput(chatBotKey, chatBotModel, prompt=formattedDescriptionContent, useWeb=False)
    storyTitle = chatBotOutput(chatBotKey, chatBotModel, prompt=f"Generate a single, engaging summary for the story below in the form of a suspenseful or thought-provoking question. The question must be under 100 characters and should hint at the core conflict or mystery of the story without giving away the ending. Use a tone that creates curiosity, such as 'What happens when...' or 'Can she escape...?' or 'Will they survive...?'. In {gv.storyLanguage} language \n {storyDescription}", useWeb=False)
    if storyDescription:
        writeContentToDoc(descriptionOutputFile, storyDescription) 
    return storyTitle   

def generateIndexFunction(storyLanguage=gv.storyLanguage, storyGenra=gv.storyGenra, tableOfIndexPromptFile=gv.tableOfIndexPromptFile, storyNameFile=gv.storyNameFile, chatBotKey=gv.chatBotKey, chatBotModel=gv.chatBotModel, useWebSearch=gv.useWebSearch):
    storyNameExists = readPromptFile(storyNameFile).replace('\n', '').split(',')

    if storyLanguage.lower() == 'hindi':
        promptInstruction = f"यह कहानी {storyLanguage} में है और शैली {storyGenra} है। परिणाम को एक dictionary के रूप में लौटाएँ जहाँ keys अध्याय संख्याएँ (पूर्णांक के रूप में string) हैं, और मान 'title' और 'description' कुंजियों वाले dictionary हैं। आउटपुट को JSON जैसी संरचना के रूप में ठीक से स्वरूपित किया जाना चाहिए। dictionary के पहले तत्व के रूप में उपन्यास का नाम भी बनाएँ जिसमें key 'novel_name' और मान उपन्यास के नाम के रूप में हो। उपन्यास के नाम में कोई विशेष वर्ण नहीं होना चाहिए। उपन्यास का नाम {storyNameExists} में से कोई भी नहीं होना चाहिए \n कहानी के नाम में कोई विशेष वर्ण न डालें \n JSON सामग्री के अलावा कुछ भी अतिरिक्त न लिखें\n JSON संरचना की दोबारा जांच करें और सुनिश्चित करें कि यह वैध है, और दोबारा जांच लें कि आपने सभी निर्देशों का पालन किया है या नहीं"
    elif storyLanguage.lower() == 'english':
        promptInstruction = f"This story is in {storyLanguage} and genra is {storyGenra}. \n Return the result as a dictionary where keys are chapter numbers (as integers as string), and values are dictionaries with 'title' and 'description' keys. The output should be properly formatted as a JSON-like structure. Also, create the novel name as the first element of the dictionary with key 'novel_name' and value as the name of the novel. The novel name should not have any spacial character. The novel name should not be any of {storyNameExists}. \n Do not put any special characters in the story name. \n Do not write anything extra except JSON content \n double check the JSON structure and ensure it is valid, and double check if you follow all instructions"

    tableOfIndexPrompt = f"{readPromptFile(tableOfIndexPromptFile)}\n{promptInstruction}"

    tableOfIndex = chatBotOutput(chatBotKey, chatBotModel, prompt=tableOfIndexPrompt, useWeb=useWebSearch)
    json_string = tableOfIndex.replace("```json", "").replace("```", "").strip()
    json_string = json_string.strip().lstrip('\ufeff')
    try:
        generateIndexOutput = json.loads(json_string)                
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON: {e}")
    return generateIndexOutput if generateIndexOutput else None

def proceedWithTableOfIndex(storyLanguage=gv.storyLanguage, storyGenra=gv.storyGenra, tableOfIndexPromptFile=gv.tableOfIndexPromptFile, storyNameFile=gv.storyNameFile, outputPath=gv.outputPath, descriptionPromptFile=gv.descriptionPromptFile):
    generateIndex = generateIndexFunction(storyLanguage, storyGenra, tableOfIndexPromptFile, storyNameFile)

    if generateIndex:
        
        story_name, story_name_folder = processStoryName(generateIndex, storyNameFile)

        finalPath = f"{outputPath}/{storyLanguage}/{storyGenra}/{story_name_folder}/"
        os.makedirs(finalPath, exist_ok=True)
        writeContentToDoc(f"{finalPath}/Docs/story.docx", story_name)
        
        if (os.path.exists(descriptionPromptFile) and os.path.getsize(descriptionPromptFile) != 0) or descriptionPromptFile is not None:
            # Generate description for the story
            descriptionOutputFile=f"{finalPath}/Docs/storyDescription.docx"
            storyTitle = generateDescription(generateIndex, descriptionOutputFile, descriptionPromptFile)

        # Process each chapter
        storyOutputFile = f"{finalPath}/Docs/story.docx"
        generateStoryForChapter(finalPath, generateIndex)
        return story_name, storyTitle, finalPath
    else:
        raise ValueError("Index generation failed or is empty.")
