import sys, os
import logging

logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import globalVariables as gv

from lib.subtitleLib.generateSubtitle import generateASSWithKaraoke
from lib.subtitleLib.addSubtitleToVideo import burnSubtitleToVideo

def videoSubtitle(audioFilePath, outputASSPath, videoFilePath, finalVideoPath):
    generateASSWithKaraoke(audioFilePath, outputASSPath)
    logger.info("SRT generated")
    burnSubtitle = burnSubtitleToVideo(videoFilePath, outputASSPath, finalVideoPath)

    if burnSubtitle:
        logger.info("SRT added to Video")