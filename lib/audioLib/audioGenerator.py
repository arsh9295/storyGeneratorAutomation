import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import globalVariables as gv

def audioGenerator(inputText, outputpat, outputfileName, voiceName=None, 
                   model_name=None, speed=None, pad_between_segments=None, 
                   remove_silence=None, minimum_silence=None, custom_voicepack=None, audioUrl=None, language=None, slow=None, tld=None, exist_ok=True, audioModel=None):
    # Initialize parameters with defaults or from global variables
    voiceName = voiceName if voiceName is not None else getattr(gv, 'audioVoice', "am_echo")
    model_name = model_name if model_name is not None else getattr(gv, 'audioSubModel', "kokoro-v0_19.pth")
    speed = speed if speed is not None else getattr(gv, 'speed', 0.85)
    pad_between_segments = pad_between_segments if pad_between_segments is not None else getattr(gv, 'pad_between_segments', 0.3)
    remove_silence = remove_silence if remove_silence is not None else getattr(gv, 'remove_silence', False)
    minimum_silence = minimum_silence if minimum_silence is not None else getattr(gv, 'minimum_silence', 0.05)
    custom_voicepack = custom_voicepack if custom_voicepack is not None else getattr(gv, 'custom_voicepack', None)
    audioUrl = audioUrl if audioUrl is not None else getattr(gv, 'audioUrl', None)
    language = language if language is not None else getattr(gv, 'storyLanguage', "en")
    slow = slow if slow is not None else getattr(gv, 'slow', False)
    tld = tld if tld is not None else getattr(gv, 'tld', 'co.in')
    audioModel = audioModel if audioModel is not None else getattr(gv, 'audioModel', "kokoro09")

    language = 'hi' if language.lower() == 'hindi' else 'en' if language.lower() == 'english' else language

#########################################################

    # Ensure output path exists
    if not os.path.exists(outputpat):
        os.makedirs(outputpat, exist_ok=exist_ok)
    
    # Generate audio file
    if audioModel.lower() == "kokoro09":
        from lib.audioLib.kokoro09Audio import generateVoice
        audio_file = generateVoice(
            inputText,
            storyPath=outputpat,
            fileName=outputfileName,
            voiceName=voiceName,
            # model_name=model_name,
            # speed=speed,
            # pad_between_segments=pad_between_segments,
            # remove_silence=remove_silence,
            # minimum_silence=minimum_silence,
            # custom_voicepack=custom_voicepack,
            # audioUrl=audioUrl
        )
    elif audioModel.lower() == "kokoro10":
        from lib.audioLib.kokoro10Audio import generateVoice
        audio_file = generateVoice(
            inputText,
            output_path=outputpat,
            output_file_name=outputfileName,
            voice_name=voiceName,
            model_name=model_name,
            speed=speed,
            pad_between_segments=pad_between_segments,
            remove_silence=remove_silence,
            minimum_silence=minimum_silence,
            custom_voicepack=custom_voicepack,
            audioUrl=audioUrl
        )
    elif audioModel.lower() == "gtts":
        from lib.audioLib.gttsAudio import text_to_speech
        audio_file = text_to_speech(
            inputText, 
            filepath=outputpat, 
            language=language, 
            filename=f"{outputfileName}.wav", 
            slow=slow, 
            tld=tld
        )
    elif audioModel.lower() == "kokorofastapi":
        from lib.audioLib.kokorofastapi import synthesize
        audio_file = synthesize(
            inputText, 
            voice=voiceName,
            model=model_name,
            speed=speed,
            OutputPath=outputpat,
            output_file_name=outputfileName,
        )
    else:
        raise ValueError(f"Unsupported audio model: {audioModel}")