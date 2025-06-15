import random
from moviepy.editor import *

def random_ken_burns(image_path, duration=4, size=(1280, 720), zoom_range=(1.05, 1.2)):
    img = ImageClip(image_path).resize(height=size[1])  # Maintain aspect ratio
    
    # Random zoom direction: in or out
    zoom_start = random.uniform(*zoom_range)
    zoom_end = random.uniform(*zoom_range)
    if random.choice([True, False]):
        zoom_start, zoom_end = zoom_end, zoom_start  # flip zoom direction

    # Get image dimensions
    w, h = img.size

    # Pan range
    max_x_shift = int((zoom_start - 1) * w)
    max_y_shift = int((zoom_start - 1) * h)
    x_start = random.randint(0, max_x_shift)
    y_start = random.randint(0, max_y_shift)
    x_end = random.randint(0, max_x_shift)
    y_end = random.randint(0, max_y_shift)

    def make_crop(t):
        zoom = zoom_start + (zoom_end - zoom_start) * (t / duration)
        x = x_start + (x_end - x_start) * (t / duration)
        y = y_start + (y_end - y_start) * (t / duration)

        crop_width = int(size[0] / zoom)
        crop_height = int(size[1] / zoom)
        x_center = int(w / 2 - crop_width / 2 + x)
        y_center = int(h / 2 - crop_height / 2 + y)

        return img.crop(x1=x_center, y1=y_center,
                        width=crop_width, height=crop_height).resize(size)

    return VideoClip(make_crop, duration=duration)

def createRandomKenBurnsVideo(image_paths):
    
    clips = [random_ken_burns(img, duration=4) for img in image_paths]
    
    return concatenate_videoclips(clips, method="compose")

# # === USAGE ===
# image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]  # Replace with your paths
# 
# final_video = concatenate_videoclips(clips, method="compose")
# final_video.write_videofile("ken_burns_random.mp4", fps=24)
