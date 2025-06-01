import os
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, vfx

def createCombineImages(image_paths, output_path, image_duration=5, transition_duration=1):
    clips = []
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for path in image_paths:
        clip = ImageClip(path).with_duration(image_duration).with_position('center').with_effects([vfx.CrossFadeIn(1)]).with_effects([vfx.CrossFadeOut(1)])
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    final.write_videofile(output_path, fps=24)

# Example usage:
# image_files = ["E:\\Youtube\\Stories\\Whispers of the Veiled Hollow\English\supernatural\Images\chapter_1\0.png', "2.png", "4.png", "6.png", "8.png", "10.png", "12.png", "14.png", "16.png"]
# create_moviepy_video(image_files, "output_transition_video.mp4")
