from combineImages import createCombineImages
from combineAudio import combineAudioFiles
from createVideo import createVideoMviepy
from addSubtitle import burn_subtitles_ffmpeg
from imageGenerator import GenerateImage
from generateSRT import generateSRTFromAudio
# from videoEffect import createRandomKenBurnsVideo

def getImageList(folderPath):
    import os
    imageList = [os.path.join(folderPath, file)
                 for file in os.listdir(folderPath)
                 if file.lower().endswith('.jpeg')]
    return imageList

ImageDurationInVideo=6
finalPath = f"E:/Youtube/Stories/English/Funny Anthropomorphic Fruits/Pulp & Prejudice/"
# Generate video from images
imageList = getImageList(f"{finalPath}/Images/")
createCombineImages(imageList, f"{finalPath}/Videos/chapter_video.mp4", ImageDurationInVideo, transition_duration=1)
# createCombineImages(imageList, f"{finalPath}/Videos/chapter_video.mp4", image_duration=6, transition_duration=1)
combineAudioFiles(f"{finalPath}/Audio/", f"{finalPath}/Audio/combined/combined_audio.mp3")
createVideoMviepy(f"{finalPath}/Videos/chapter_video.mp4", f"{finalPath}/Audio/combined/combined_audio.mp3", f"{finalPath}/Videos/final_video.mp4")
generateSRTFromAudio(f"{finalPath}/Audio/combined/combined_audio.mp3", "subtitles.srt")
# generateSRTFromAudio(f"{finalPath}/Audio/combined/combined_audio.mp3", f"{finalPath}/Videos/subtitles.srt")
burn_subtitles_ffmpeg(
    f"{finalPath}/Videos/final_video.mp4",
    f"subtitles.srt",
    # f"{finalPath}/Videos/subtitles.srt",
    f"{finalPath}/Videos/final_video_with_subtitles.mp4"
)


# createRandomKenBurnsVideo(imageList)