from lib.imageLib.imageGenerator import GenerateImage
from lib.thumbnilLib.thumbnilText import createThumbnailWithText
import logging
import sys, os
from PIL import Image

logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

def compress_image(input_path, output_path, quality=30):
    try:
        with Image.open(input_path) as img:
            # Keep original dimensions
            img = img.convert("RGB")  # Ensure compatibility for JPEG format

            # Save with reduced quality
            img.save(output_path, format="JPEG", optimize=True, quality=quality)

            original_size = os.path.getsize(input_path) / 1024
            new_size = os.path.getsize(output_path) / 1024

            print(f"Original Size: {original_size:.2f} KB")
            print(f"Compressed Size: {new_size:.2f} KB")
            print(f"Saved to: {output_path}")

    except Exception as e:
        print(f"Compression failed: {e}")

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        print(f"Width: {width}px, Height: {height}px")
        return width, height

def createThumbnil( 
        prompt,
        imageFileName,
        finalImageFileName,
        image_path,
        title_text
):
    GenerateImage(prompt, f"{image_path}", imageFileName)
    generateThumbnilImage = createThumbnailWithText(f"{image_path}/{imageFileName}.{gv.imageExtension}", f"{image_path}/{finalImageFileName}", title_text)
    if(generateThumbnilImage):
        logger.info(f"Thumbnil Image {finalImageFileName} generated")
    
    w, h = get_image_dimensions(f"{image_path}/{finalImageFileName}")

    if h > w:
        compress_image(f"{image_path}/{finalImageFileName}", f"{image_path}/{finalImageFileName}", quality=25)