import os, sys
import random
from pydub import AudioSegment
import logging

logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

from lib.utilLib.getAllFilesInProvidedPath import getAllFilesInProvidedPath
from lib.videoLib.combineImages import combineImages
from lib.videoLib.createVideo import createVideoMviepy


def generateVideoWithImages(finalPath, imageDurationEachImage):
    imageList = getAllFilesInProvidedPath(f"{finalPath}/Images/")
    totalAudioDuration = AudioSegment.from_file(f"{finalPath}/Audio/combined/combined_audio.mp3").duration_seconds
    createCombineImages = combineImages(imageList, f"{finalPath}/Videos/chapter_video.mp4", totalAudioDuration, imageDurationEachImage)
    if gv.addMusic:
        musicFileName = gv.musicPath if os.path.isfile(gv.musicPath) else random.choice(getAllFilesInProvidedPath(gv.musicPath))
        musicFileName = musicFileName if os.path.isfile(musicFileName) else None
        if musicFileName is None:
            logger.warning("Provided music path is not valid... Continuing without music")

    createVideoMviepy(f"{finalPath}/Videos/chapter_video.mp4", f"{finalPath}/Audio/combined/combined_audio.mp3", f"{finalPath}/Videos/final_video.mp4", musicFileName)