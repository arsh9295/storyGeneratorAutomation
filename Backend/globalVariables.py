import os

currentFile = os.path.abspath(__file__)
parentDir = os.path.dirname(os.path.dirname(currentFile))

# Videos Generator Settings
perImageDuration = 7
slidDurationInImage = 0
additionalImagePath = "" # If Provided, it will add this as last frame
imageCombineMethod = "chain" #possible values chain, compress
transitionDuration = 1
finalVideoSize = None # Can provide resolution of final video, If it not provided it will use image size
wordsPerChapter = None
createImageFromSRT = False

videoCode = "libx264"
videoPreset = "ultrafast"
videoThreds = 16

audioCoded = "aac"

videoEffect = "Zoom" # Possible values None, Zoom
ZoomDirection = "Random" # Possible values Randone, 'center', 'left', 'right', 'top', 'bottom'
zoomStrength = 0.1

addMusic = True
musicLoudness = "10%" # How loudness will be music on video
musicPath = "E:/Youtube/storyMusic/" # can provide path where multiple music file placed, it will pick any one  / you can directly provide music file name with complete path

# Final Vide Settings
videoType = "testPrompt"  # or "longVideos"
storyGenra = "supernatural"  # or "romantic", "horror", etc.
storyLanguage = "english"  # "english" or "hindi"
videoGenerationMode = "FromTableOfIndex" # Possible selection, FromStoryGeneratedFile, FromStoryPrompt, FromTableOfIndex
storyText = "" # This parameter is valid only for videoGenerationMode="FromStoryGeneratedFile". This is optional parameter, you can provide storyFile parameter or this
storyName = "" # This parameter is valid only for videoGenerationMode="FromStoryGeneratedFile". This is optional parameter
storyPrompt = "" # This parameter is valid only for videoGenerationMode="FromStoryPrompt". This is optional parameter

# Path Details
storyFile = "" # This parameter is valid only for videoGenerationMode="FromStoryGeneratedFile". This is optional parameter, you can provide storyPrompt parameter or this
storyNameFile = f"{parentDir}/Input/storyName.txt"

tableOfIndexPromptFile = f"{parentDir}/Input/Prompts/{videoType}/tableOfIndex.txt"
descriptionPromptFile = f"{parentDir}/Input/Prompts/{videoType}/descriptionPrompt.txt"
storyPromptFile = f"{parentDir}/Input/Prompts/{videoType}/storyPrompt.txt"
imagePromptFile = f"{parentDir}/Input/Prompts/{videoType}/ImagePromtp.txt"

storyFilePath = f"{parentDir}/Input/Prompts/{videoType}/story.docx" # Valid file extension, txt and docx

outputPath = f"E:/Youtube/Channels/Dark Chronicles/long"

# ChatBot Settings
chatBotKey = ""
chatBotModel = "gemini-2.0-flash" #"gemini-2.0-flash" or "gpt-4o" or "gpt-4-turbo" or "gpt-3.5-turbo"
useWebSearch = False  # Set to True if you want to use web search capabilities

# Audio settings
audioModel = "kokoro09" #kokoro09 or kokoro10 or gtts
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
negativePrompts =  "lowres, bad anatomy, bad proportions, poorly drawn face, double face, cloned face, extra eyes, more than two eyes, deformed pupils, mismatched eyes, cross‑eyed, double nose, extra nose, malformed nose, duplicate features, extra limbs, long neck, elongated neck, mutation, mutated, disfigured, deformed, poorly drawn hands, fused fingers, extra fingers, fused hands, ugly, blurry, out of frame, watermark, signature, text, destroid face, bad face, bad hands, deformed, blurry, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands and fingers, poorly drawn hands and fingers, missing fingers, extra digit, fewer digits, cropped, worst quality, nsfw, lowres, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, fused fingers, too many fingers, long neck, cgi, 3d, cartoon, anime, sketch, drawing, painting, illustration, low quality, out of focus, bad lighting, overexposed, underexposed, grainy, pixelated, noisy, artifacts, compression artifacts, watermarks, text, logo, signature, copyright, label, brand, product name"
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
device = "cuda"
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