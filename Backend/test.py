from combineImages import createCombineImages
from combineAudio import combineAudioFiles
from createVideo import createVideoMviepy

finalPath = 'E:\Youtube\Stories\Whispers of the Forgotten Grimoire\English\supernatural'
# imageList = [
#     f"{finalPath}/Images/chapter_1_0.png",
#     f"{finalPath}/Images/chapter_1_2.png",
#     f"{finalPath}/Images/chapter_1_4.png",
#     f"{finalPath}/Images/chapter_1_6.png",
#     f"{finalPath}/Images/chapter_1_8.png"
# ]

import os

folder_path = f'{finalPath}/Images/'
imageList = [os.path.join(folder_path, file)
             for file in os.listdir(folder_path)
             if file.lower().endswith('.png')]

print(imageList)


# createCombineImages(imageList, f"{finalPath}/Videos/chapter_video.mp4", image_duration=4, transition_duration=1)
# combineAudioFiles(f"{finalPath}/Audio/", f"{finalPath}/Audio/combined/combined_audio.mp3")
createVideoMviepy(f"{finalPath}/Videos/chapter_video.mp4", f"{finalPath}/Audio/combined/combined_audio.mp3", f"{finalPath}/Videos/final_video.mp4")