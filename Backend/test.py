from combineImages import createCombineImages
from combineAudio import combineAudioFiles
from createVideo import createVideoMviepy
from addSubtitle import burn_subtitles_ffmpeg


# def getImageList(folderPath):
#     import os
#     imageList = [os.path.join(folderPath, file)
#                  for file in os.listdir(folderPath)
#                  if file.lower().endswith('.png')]
#     return imageList


finalPath = f"E:\Youtube\Stories/English/Supernatural/Echoes of the Unseen/"
# Generate video from images
# imageList = getImageList(f"{finalPath}/Images/")
# createCombineImages(imageList, f"{finalPath}/Videos/chapter_video.mp4", image_duration=6, transition_duration=1)
# combineAudioFiles(f"{finalPath}/Audio/", f"{finalPath}/Audio/combined/combined_audio.mp3")
# createVideoMviepy(f"{finalPath}/Videos/chapter_video.mp4", f"{finalPath}/Audio/combined/combined_audio.mp3", f"{finalPath}/Videos/final_video.mp4")
# generate_srt_from_audio(f"{finalPath}/Audio/combined/combined_audio.mp3", f"{finalPath}/Videos/subtitles.srt", chunk_length=5)
# burn_srt_to_video(f"{finalPath}/Videos/final_video.mp4", "output.srt", f"{finalPath}/Videos/final_video_with_subtitles.mp4")
burn_subtitles_ffmpeg(
    f"{finalPath}/Videos/final_video.mp4",
    f"subtitles.srt",
    f"{finalPath}/Videos/final_video_with_subtitles.mp4"
)