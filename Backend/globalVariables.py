import os

currentFile = os.path.abspath(__file__)
parentDir = os.path.dirname(os.path.dirname(currentFile))

# Videos Generator Settings
perImageDuration = 7
slidDurationInImage = 0
additionalImagePath = "" # If Provided, it will add this as last frame
imageCombineMethod = "compose" #possible values chain, compose
transitionDuration = 0.2
finalVideoSize = None # Can provide resolution of final video, If it not provided it will use image size
wordsPerChapter = None
createImageFromSRT = True

videoCode = "libx264"
videoPreset = "ultrafast"
videoThreds = 16

audioCoded = "aac"

videoEffect = "Zoom" # Possible values None, Zoom
ZoomDirection = "Random" # Possible values Randone, 'center', 'left', 'right', 'top', 'bottom'
zoomStrength = 0.1

addMusic = True
musicLoudness = "10%" # How loudness will be music on video
musicPath = "E:/Youtube/storyMusic" # can provide path where multiple music file placed, it will pick any one  / you can directly provide music file name with complete path

# Final Vide Settings
videoType = "testPrompt"  # or "longVideos"
storyGenra = "moral value"  # or "romantic", "horror", etc.
storyLanguage = "hindi"  # "english" or "hindi"
videoGenerationMode = "FromTableOfIndex" # Possible selection, FromStoryGeneratedFile, FromStoryPrompt, FromTableOfIndex
storyText = "" # This parameter is valid only for videoGenerationMode="FromStoryGeneratedFile". This is optional parameter, you can provide storyFile parameter or this
storyName = "" # This parameter is valid only for videoGenerationMode="FromStoryGeneratedFile". This is optional parameter
storyPrompt = "" # This parameter is valid only for videoGenerationMode="FromStoryPrompt". This is optional parameter

# Path Details
storyFile = "" # This parameter is valid only for videoGenerationMode="FromStoryGeneratedFile". This is optional parameter, you can provide storyPrompt parameter or this
storyNameFile = f"{parentDir}/Input/storyName.txt"

# tableOfIndexPromptFile = f"{parentDir}/Input/Prompts/{videoType}/tableOfIndex.txt"
# descriptionPromptFile = f"{parentDir}/Input/Prompts/{videoType}/descriptionPrompt.txt"
# storyPromptFile = f"{parentDir}/Input/Prompts/{videoType}/storyPrompt.txt"
# imagePromptFile = f"{parentDir}/Input/Prompts/{videoType}/ImagePromtp.txt"

tableOfIndexPromptFile = f"C:/Utkarsh/VideoGenerator/Prompts/Agyat Gaathayein/long/tableOfIndex.txt"
descriptionPromptFile = f""
storyPromptFile = f"C:/Utkarsh/VideoGenerator/Prompts/Agyat Gaathayein/long/storyPrompt.txt"
imagePromptFile = f""

storyFilePath = f"{parentDir}/Input/Prompts/{videoType}/story.docx" # Valid file extension, txt and docx

outputPath = f"E:/Youtube/Channels/Agyat Gaathayein/long"

# ChatBot Settings
chatBotKey = ""
chatBotModel = "gemini-2.5-flash-lite-preview-06-17" #"gemini-2.0-flash" or "gemini-2.5-flash-lite-preview-06-17" or "gpt-4o" or "gpt-4-turbo" or "gpt-3.5-turbo"
useWebSearch = False  # Set to True if you want to use web search capabilities

# Audio settings
audioModel = "gtts" #kokoro09 or kokoro10 or gtts
audioVoice = "am_echo"  # or any other voice name
audioSubModel = "kokoro-v0_19.pth"  # or any other model name
speed = 0.85
pad_between_segments = 0.3
remove_silence = False
minimum_silence = 0.05
custom_voicepack = None  # Set to a custom voice pack if needed
audioUrl = None  # Set to a specific audio URL if needed


# Images Settings

apiUrl = "http://127.0.0.1:8888/v1/generation/text-to-image"
# negativePrompts = "lowres, worst quality, low quality, blurry, pixelated, jpeg artifacts, grainy, text, logo, watermark, signature, username, cropped, out of frame, error, bad composition, bad lighting, underexposed, overexposed, unnatural shadows, cgi, 3d, cartoon, anime, painting, sketch, drawing, illustration, plastic doll, deviant art, surreal, abstract, distorted, mutated, mutated limbs, malformed limbs, malformed body, bad anatomy, bad proportions, disfigured, deformed, contorted, gross proportions, ugly body, extra limbs, extra arms, extra legs, extra fingers, fused fingers, fused hands, missing limbs, missing fingers, missing arms, missing legs, long neck, long body, cloned face, double face, two faces, poorly drawn face, bad face, deformed pupils, cross‑eyed, huge eyes, oversized eyes, mismatched eyes, poorly drawn eyes, messy hair, bad ears, malformed ears, poorly drawn hands, bad hands, malformed hands, webbed fingers, claw-like fingers, extra digits, too many fingers, floating limbs, disconnected limbs, dismembered, amputee, ugly fingers, broken bones, body horror, morbid, mutilated"
negativePrompts = '''
(low quality:1.3), (worst quality:1.3), (blurry:1.2), (jpeg artifacts:1.2), (watermark:1.2), (text:1.2), (signature:1.2), (logo:1.2), (cropped:1.1), (out of frame:1.1), (bad composition:1.1),
(bad anatomy:1.3), (bad proportions:1.3), (deformed:1.3), (disfigured:1.3), (contorted:1.2), (gross proportions:1.2),
(extra limbs:1.5), (extra arms:1.5), (extra legs:1.5), (extra fingers:1.5), (mutated limbs:1.5), (mutated hands:1.5), (fused fingers:1.5), (missing limbs:1.5),
(cloned face:1.5), (double face:1.5), (two faces:1.5), (poorly drawn face:1.4), (bad face:1.4),
(poorly drawn hands:1.4), (bad hands:1.4), (malformed hands:1.4), (fused hands:1.4),
(long neck:1.3), (long body:1.3)
'''
seed = -1
sampler = "DPM++ 2M Karras"
performance_selection = "Speed" #performance_selection, must be one of Speed, Quality, Extreme Speed default to Speed
aspect_ratios_selection = "1920*1080" #"1920*1080" or "1080*1920"
guidance_scale = 7.5
subModel = "juggernautXL_version6Rundiffusion.safetensors"  # adjust to a valid one
imageModel = "fooocus"
imageExtension = "png"
fooocusPath = "C:/AI/Fooocus-API/"


# Subtitle Variables 
addSubtitle = True
model_name = "base"
device = "cuda" # "cpu" or "cuda"
compute_type = "float16"
highlight_color = "&H00FFFF&"     # cyan
back_color = "&H64000000&"
# resolution = (1920, 1080) #(1080, 1920)
resolution = tuple(map(int, aspect_ratios_selection.split('*'))) #(1080, 1920)
style_name = "WordPop"
margin = (30, 30, 30)
pop_duration_ms =  100
zoom_font_size = 48
subtitle_format="ass"  # or "srt"
font_name="Ubuntu"
font_size=23
primary_color="&H00FF00&"
outline_color="&H000000&"
border_style=1
outline=2
shadow=1
alignment=2
margin_v=40
audio_codec="copy"
overwrite=True
dry_run=False

# Thumbnil Variables
generateThumbnil= True
font_path_bold="C:/Utkarsh/VideoGenerator/Channels/Agyat Gaathayein/shorts/Backend/lib/thumbnilLib/fonts/arialbd.ttf"
font_path_regular="C:/Utkarsh/VideoGenerator/Channels/Agyat Gaathayein/shorts/Backend/lib/thumbnilLib/fonts/arial.ttf"
title_font_size=72
subtitle_font_size=44

title_v_align = "bottom"
title_y_offset = 200
title_fill = (152, 251, 74)
title_outline_color = (0, 0, 0)
title_outline_width = 3

subtitle_text = None
subtitle_v_align = "bottom"
subtitle_y_offset = 150
subtitle_fill = (255, 255, 255)
subtitle_outline_color = (0, 0, 0)
subtitle_outline_width = 2

# Youtube Settings
uploadToYoutube = False
youtubeAuthConfigFile = ""