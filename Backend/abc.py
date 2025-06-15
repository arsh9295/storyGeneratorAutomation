# from audioGenerator import generateVoice

finalPath = f"E:\Youtube\Stories\English\Supernatural\Echoes of the Unseen"

# generatedTitleVoice = generateVoice("Hello world", f"{finalPath}/Audio/", f"chapter_0")


# from gradio_client import Client, handle_file

# client = Client("http://127.0.0.1:9000/")
# result = client.predict(
# 		text="Hello!!",
# 		model_name="kokoro-v0_19.pth",
# 		voice_name="af",
# 		speed=1,
# 		pad_between_segments=0,
# 		remove_silence=False,
# 		minimum_silence=0.05,
# 		custom_voicepack=None,
# 		api_name="/text_to_speech"
# )
# print(result)



from imageGenerator import GenerateImage

titleImageGen = GenerateImage(f"Write quoted text on image hello world", f"{finalPath}/Images/", f"chapter_0_0")