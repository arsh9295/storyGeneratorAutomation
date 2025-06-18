import os
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, vfx

from videoEffect import create_zoom_clip

def createCombineImages(image_paths, output_path, image_duration, audio_duration, ImagesOnVideoDefined, additionalImagePath, transition_duration=1):
    clips = []
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    num_images = len(image_paths)

    print(f"Images On Video Defined: {ImagesOnVideoDefined}")
    if not ImagesOnVideoDefined:
        image_duration = (audio_duration + (num_images - 1) * transition_duration) / num_images

    print(f"Image Duration: {image_duration} seconds")

    for path in image_paths:
        clip = create_zoom_clip(path, image_duration, transition_duration)
        # clip = ImageClip(path).with_duration(image_duration).resized(lambda t: 1 + 0.02 * t).with_position('center').with_effects([vfx.CrossFadeIn(transition_duration)]).with_effects([vfx.CrossFadeOut(transition_duration)])
        clips.append(clip)
    if additionalImagePath:
        additional_clip = ImageClip(additionalImagePath).with_duration(image_duration).with_position('center').with_effects([vfx.CrossFadeIn(transition_duration)]).with_effects([vfx.CrossFadeOut(transition_duration)])
        clips.append(additional_clip)

    final = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    # final.write_videofile(output_path, fps=24, preset='ultrafast')
    final.write_videofile(
        output_path,
        codec='libx264',  # MoviePy default, use 'libx264' or switch to 'libx264rgb' for lossless
        ffmpeg_params=[
            '-vcodec', 'h264_nvenc',  # This is the key: NVIDIA GPU encoding
            '-preset', 'p1',  # Choose from p1 (fastest) to p7 (best quality)
            '-rc', 'vbr',     # Rate control (cbr or vbr)
            '-cq', '19',      # Constant quality (lower = better)
        ],
        fps=24
    )

# Example usage:
# image_files = ["E:\\Youtube\\Stories\\Whispers of the Veiled Hollow\English\supernatural\Images\chapter_1\0.png', "2.png", "4.png", "6.png", "8.png", "10.png", "12.png", "14.png", "16.png"]
# create_moviepy_video(image_files, "output_transition_video.mp4")
