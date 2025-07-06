
import os, random, sys
import numpy as np
from moviepy import ImageClip, VideoClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import globalVariables as gv

def make_zoom_clip(path, duration, fps, trans_dur=1, zoom_strength=0.1, ZoomDirection=None):

    ZoomDirection = ZoomDirection if ZoomDirection is not None else getattr(gv, 'ZoomDirection', "Random")

    if ZoomDirection == "Random":
        direction = random.choice(['center', 'left', 'right', 'top', 'bottom'])
    else:
        direction = ZoomDirection    

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

    clip = VideoClip(make_frame, duration=duration).with_fps(fps)
    return clip.with_effects([FadeIn(trans_dur), FadeOut(trans_dur)])
