from lib.imageLib.imageGenerator import GenerateImage
from lib.thumbnilLib.thumbnilText import createThumbnailWithText
import logging
import sys, os

logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

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