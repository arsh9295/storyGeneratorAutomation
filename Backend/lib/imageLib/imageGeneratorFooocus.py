import requests
import base64
import os
from urllib.parse import urlparse
import shutil
import os
import logging

logger = logging.getLogger(__name__)

# Fooocus API URL
API_URL = "http://127.0.0.1:8888/v1/generation/text-to-image"  # NOT /generate

def generateImageFromText(prompt, negative_prompt="", seed=-1, sampler="DPM++ 2M Karras", performance_selection="Speed", aspect_ratios_selection="1080*1920", guidance_scale= 7.5, model="animagineXLV31_v31.safetensors", imageExtension="png"):
	# Simple working payload
	payload = {
		"prompt": prompt,
		"negative_prompt": negative_prompt,
		"seed": seed,
		"sampler": sampler,
		"performance_selection": performance_selection, #performance_selection, must be one of Speed, Quality, Extreme Speed default to Speed
		"aspect_ratios_selection": aspect_ratios_selection,
		"guidance_scale": guidance_scale,
		"model": model,  # adjust to a valid one
		"save_extension": "jpeg",
		"style_selections": ["SAI Comic Book", "Misc Kawaii", "SAI Anime", "Adorable Kawaii"],
		# "style_selections": ["Neoclassicism","SAI Anime", "SAI Comic Book"]
		# "enabled": "true",
		# "model_name": "sd_xl_offset_example-lora_1.0.safetensors",
		# "weight": "0.5"
	}

	# print("🚀 Sending request to Fooocus API...")

	# Send request
	result = requests.post(API_URL, json=payload)
	return result.json()

def moveGeneratedImageToDestination(source, destination):
	# Define source and destination paths
	source = source
	destination = destination

	# Ensure destination directory exists
	os.makedirs(os.path.dirname(destination), exist_ok=True)

	# Move the file
	shutil.move(source, destination)



def GenerateImageFooocus(prompt, outputPath, outputFile, fooocusPath, negative_prompt="", seed=-1, sampler="DPM++ 2M Karras", performance_selection="Speed", aspect_ratios_selection="1080*1920", guidance_scale= 7.5, model="juggernautXL_version6Rundiffusion.safetensors", imageExtension="png"):
	generateImage = generateImageFromText(prompt, negative_prompt, seed, sampler, performance_selection, aspect_ratios_selection, guidance_scale, model)

	if generateImage:
		imageUrl = generateImage[0]['url']
		imagePath = urlparse(imageUrl)
		path = imagePath.path.lstrip('/')  # Remove leading '/'
		moveGeneratedImageToDestination(f"{fooocusPath}/outputs/{path}", f"{outputPath}/{outputFile}.png")
		logger.info(f"Image '{outputFile}.png' generated.")
