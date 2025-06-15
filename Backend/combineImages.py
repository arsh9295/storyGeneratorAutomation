import os
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, vfx

def createCombineImages(image_paths, output_path, image_duration, audio_duration, ImagesOnVideoDefined, transition_duration=1):
    clips = []
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # total_duration = image_duration  # here, this is the TOTAL target length
    num_images = len(image_paths)
    # image_duration = (total_duration + (num_images - 1) * transition_duration) / num_images
    # image_duration = image_duration - (transition_duration / 2)
    print(f"Images On Video Defined: {ImagesOnVideoDefined}")
    if not ImagesOnVideoDefined:
        image_duration = (audio_duration + (num_images - 1) * transition_duration) / num_images

    print(f"Image Duration: {image_duration} seconds")

    for path in image_paths:
        clip = ImageClip(path).with_duration(image_duration).with_position('center').with_effects([vfx.CrossFadeIn(transition_duration)]).with_effects([vfx.CrossFadeOut(transition_duration)])
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    final.write_videofile(output_path, fps=30)

# Example usage:
# image_files = ["E:\\Youtube\\Stories\\Whispers of the Veiled Hollow\English\supernatural\Images\chapter_1\0.png', "2.png", "4.png", "6.png", "8.png", "10.png", "12.png", "14.png", "16.png"]
# create_moviepy_video(image_files, "output_transition_video.mp4")
