import requests
import base64
import os
from urllib.parse import urlparse
import shutil
import os
import logging

logger = logging.getLogger(__name__)


FOOOCUS_HOST = os.getenv("FOOOCUS_HOST", "story1-fooocus")
FOOOCUS_PORT = int(os.getenv("FOOOCUS_PORT", "8888"))
KOKORO_HOST = os.getenv("KOKORO_HOST", "story1-kokoro")
KOKORO_PORT = int(os.getenv("KOKORO_PORT", "8880"))

# Fooocus API URL
API_URL = f"http://{FOOOCUS_HOST}:{FOOOCUS_PORT}/v1/generation/text-to-image"  # NOT /generate

def generateImageFromText(prompt, negative_prompt="", seed=-1, sampler="DPM++ 2M Karras", performance_selection="Speed", aspect_ratios_selection="1080*1920", guidance_scale= 7.5, model="juggernautXL_version6Rundiffusion.safetensors", imageExtension="png"):
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
		"save_extension": "jpeg"
	}

	# print("🚀 Sending request to Fooocus API...")

	# Send request
	result = requests.post(API_URL, json=payload)
	result.raise_for_status()            # always a good idea

	data = result.json()
	if not isinstance(data, list) or not data:
		raise ValueError("Unexpected API response: empty or not list")

	first = data[0]
	img_url = first.get("url")
	img_url = img_url.replace("127.0.0.1", FOOOCUS_HOST)
	if not img_url:
		raise ValueError("No 'url' field in API response")

	# Download image from the URL
	img_resp = requests.get(img_url)
	img_resp.raise_for_status()
	img_bytes = img_resp.content

	# print(data)
	# b64 = data[0]  # base64 string
	# img_bytes = base64.b64decode(b64)
	return img_bytes
	# return result.json()

def moveGeneratedImageToDestination(source, destination):
	# Define source and destination paths
	source = source
	destination = destination

	# Ensure destination directory exists
	os.makedirs(os.path.dirname(destination), exist_ok=True)

	# Move the file
	# shutil.move(source, destination)

	with open(destination, "wb") as f:
		f.write(source)



def GenerateImageFooocus(prompt, outputPath, outputFile, fooocusPath, negative_prompt="", seed=-1, sampler="DPM++ 2M Karras", performance_selection="Speed", aspect_ratios_selection="1080*1920", guidance_scale= 7.5, model="juggernautXL_version6Rundiffusion.safetensors", imageExtension="png"):
	generateImage = generateImageFromText(prompt, negative_prompt, seed, sampler, performance_selection, aspect_ratios_selection, guidance_scale, model)

	if generateImage:
		# imageUrl = generateImage[0]['url']
		# imagePath = urlparse(imageUrl)
		# path = imagePath.path.lstrip('/')  # Remove leading '/'
		# moveGeneratedImageToDestination(f"/app/outputs/{path}", f"{outputPath}/{outputFile}.png")
		moveGeneratedImageToDestination(generateImage, f"{outputPath}/{outputFile}.png")
		logger.info(f"Image '{outputFile}.png' generated.")
