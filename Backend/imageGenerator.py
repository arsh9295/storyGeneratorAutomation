import requests
import base64
import os
from urllib.parse import urlparse
import shutil
import os


# Fooocus API URL
API_URL = "http://127.0.0.1:8888/v1/generation/text-to-image"  # NOT /generate

def generateImageFromText(prompt):
	# Simple working payload
	payload = {
		"prompt": prompt,
		"negative_prompt": "bad hands, deformed, blurry, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands and fingers, poorly drawn hands and fingers, missing fingers, extra digit, fewer digits, cropped, worst quality, nsfw, lowres, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, fused fingers, too many fingers, long neck, cgi, 3d, cartoon, anime, sketch, drawing, painting, illustration, low quality, out of focus, bad lighting, overexposed, underexposed, grainy, pixelated, noisy, artifacts, compression artifacts, watermarks, text, logo, signature, copyright, label, brand, product name",
		"seed": -1,
		"sampler": "DPM++ 2M Karras",
		"performance_selection": "Speed", #performance_selection, must be one of Speed, Quality, Extreme Speed default to Speed
		"aspect_ratios_selection": "1280*720",
		"guidance_scale": 7.5,
		"model": "juggernautXL_version6Rundiffusion.safetensors"  # adjust to a valid one
		# "save_extension": "jpeg"
	}

	print("🚀 Sending request to Fooocus API...")

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

	print(f"Moved file from {source} to {destination}")


def GenerateImage(prompt, outputPath, outputFile):
	generateImage = generateImageFromText(prompt)

	if generateImage:
		imageUrl = generateImage[0]['url']
		imagePath = urlparse(imageUrl)
		path = imagePath.path.lstrip('/')  # Remove leading '/'
		print(path)
		moveGeneratedImageToDestination(f"C:\AI\Fooocus-API\outputs\{path}", f"{outputPath}/{outputFile}.png")
