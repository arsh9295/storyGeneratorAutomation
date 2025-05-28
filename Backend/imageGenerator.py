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
		"negative_prompt": "",
		"seed": -1,
		"sampler": "DPM++ 2M Karras",
		"steps": 30,
		"width": 1280,
		"height": 720,
		"guidance_scale": 7.5,
		"model": "juggernautXL_version6Rundiffusion.safetensors"  # adjust to a valid one
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
