import os, random
import numpy as np
from moviepy import ImageClip, VideoClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut

def make_zoom_clip(path, duration, trans_dur=1, zoom_strength=0.1, direction='center'):
    img = ImageClip(path).with_duration(duration)
    w, h = img.size

    def make_frame(t):
        factor = 1 + zoom_strength * (t / duration)
        zoomed = img.resized(factor)
        cx, cy = w * factor / 2, h * factor / 2

        dx = {'left': -w*(factor-1)/2, 'right': w*(factor-1)/2}.get(direction, 0)
        dy = {'top': -h*(factor-1)/2, 'bottom': h*(factor-1)/2}.get(direction, 0)

        frame = zoomed.cropped(
            x_center=cx + dx, y_center=cy + dy,
            width=w, height=h
        ).get_frame(t)
        return frame

    clip = VideoClip(make_frame, duration=duration).with_fps(24)
    return clip.with_effects([FadeIn(trans_dur), FadeOut(trans_dur)])

def createCombineImages(image_paths, output_path,
                        image_duration=None, audio_duration=None,
                        ImagesOnVideoDefined=False,
                        transition_duration=1, fps=24):

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    n = len(image_paths)
    if not ImagesOnVideoDefined:
        image_duration = (audio_duration + (n - 1) * transition_duration) / n

    clips = []
    for p in image_paths:
        direction = random.choice(['center', 'left', 'right', 'top', 'bottom'])
        clips.append(make_zoom_clip(p, image_duration,
                                    transition_duration, 0.1, direction))

    final = concatenate_videoclips(clips, method='compose',
                                   padding=-transition_duration)
    final.write_videofile(output_path,
                          fps=fps, codec='libx264',
                          preset='ultrafast', threads=4)

if __name__ == "__main__":
    images = ["img1.jpg", "img2.jpg", "img3.jpg"]
    createCombineImages(
        image_paths=images,
        output_path="combined.mp4",
        image_duration=None,
        audio_duration=60,
        ImagesOnVideoDefined=False,
        transition_duration=1,
        fps=24
    )
