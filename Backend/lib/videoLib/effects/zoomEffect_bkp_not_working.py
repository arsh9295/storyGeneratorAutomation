import os, random, sys
import numpy as np
from moviepy import ImageClip, VideoClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut
# from moviepy.video.fx import crop as crop_fx
# from moviepy.video.fx import crop

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import globalVariables as gv

def make_zoom_clip(path, duration, fps, trans_dur=1, zoom_strength=0.1, ZoomDirection=None):

    ZoomDirection = ZoomDirection if ZoomDirection is not None else getattr(gv, 'ZoomDirection', "Random")

    if ZoomDirection == "Random":
        # direction = random.choice(['center', 'left', 'right', 'top', 'bottom',
        #                            'top-left', 'top-right', 'bottom-left', 'bottom-right'])
        direction = random.choice(['center', 'left', 'right', 'top', 'bottom'])        
    else:
        direction = ZoomDirection    

    img = ImageClip(path).with_duration(duration)
    w, h = img.size

    # Precompute the direction vector
    dir_map = {
        'center': (0, 0),
        'left': (-1, 0),
        'right': (1, 0),
        'top': (0, -1),
        'bottom': (0, 1),
        'top-left': (-1, -1),
        'top-right': (1, -1),
        'bottom-left': (-1, 1),
        'bottom-right': (1, 1),
    }

    dx_mult, dy_mult = dir_map.get(direction, (0, 0))

    def make_frame(t):
        progress = t / duration
        factor = 1.0 + zoom_strength * progress
        zoomed = img.resized(factor)
        zw, zh = zoomed.size

        # Interpolate crop center from image center to target direction
        cx_start, cy_start = zw / 2, zh / 2
        cx_end = cx_start + dx_mult * (zw - w) / 2
        cy_end = cy_start + dy_mult * (zh - h) / 2
        cx = cx_start + (cx_end - cx_start) * progress
        cy = cy_start + (cy_end - cy_start) * progress

        # Calculate crop rectangle
        x1 = cx - w / 2
        y1 = cy - h / 2
        x2 = x1 + w
        y2 = y1 + h

        # Ensure crop rectangle is within bounds
        x1 = max(0, min(x1, zw - w))
        y1 = max(0, min(y1, zh - h))
        x2 = x1 + w
        y2 = y1 + h

        frame = img.cropped(zoomed, x1=x1, y1=y1, x2=x2, y2=y2).get_frame(t)
        return frame

    clip = VideoClip(make_frame, duration=duration).with_fps(fps)
    return clip.with_effects([FadeIn(trans_dur), FadeOut(trans_dur)])
