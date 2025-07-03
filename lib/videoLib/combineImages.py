import os, random, sys
import numpy as np
from moviepy import ImageClip, VideoClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut
from datetime import datetime
import logging
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from moviepy.audio.fx import AudioLoop, MultiplyVolume

from lib.videoLib.effects.zoomEffect import make_zoom_clip
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import globalVariables as gv

def combineImages(image_paths, output_path, audio_duration, imageDurationEachImage=None,
                        imageDuration=None,
                        slidDurationInImage=None, additionalImagePath=None,
                        transitionDuration=None, fps=None, videoCode=None, videoPreset=None, finalVideoSize=None, imageCombineMethod=None, videoThreds=None, zoomStrength=None, music_path=None, audio_path=None, musicLoudness=None):

    master_start_time = datetime.now()

    imageDuration = imageDuration if imageDuration is not None else getattr(gv, 'perImageDuration', 7)
    slidDurationInImage = slidDurationInImage if slidDurationInImage is not None else getattr(gv, 'slidDurationInImage', 0)
    additionalImagePath = additionalImagePath if additionalImagePath is not None else getattr(gv, 'additionalImagePath', None)
    imageCombineMethod = imageCombineMethod if imageCombineMethod is not None else getattr(gv, 'imageCombineMethod', 'chain')
    transitionDuration = transitionDuration if transitionDuration is not None else getattr(gv, 'transitionDuration', 1)
    videoCode = videoCode if videoCode is not None else getattr(gv, 'videoCode', 'libx264')
    videoPreset = videoPreset if videoPreset is not None else getattr(gv, 'videoPreset', 'ultrafast')
    videoThreds = videoThreds if videoThreds is not None else getattr(gv, 'videoThreds', 16)
    zoomStrength = zoomStrength if zoomStrength is not None else getattr(gv, 'zoomStrength', 0.1)
    fps = fps if fps is not None else getattr(gv, 'fps', 24)
    finalVideoSize = finalVideoSize if finalVideoSize is not None else getattr(gv, 'finalVideoSize', None)
    musicLoudness = musicLoudness if musicLoudness is not None else getattr(gv, 'musicLoudness', "10%")

    ImagesOnVideoDefined = True if slidDurationInImage > 0 else False

    audio_clip = AudioFileClip(audio_path)


    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    n = len(image_paths)
    if not ImagesOnVideoDefined:
        imageDuration = (audio_duration + (n - 1) * transitionDuration) / n

    clips = []
    clip_generation_start_time = datetime.now()
    for p in image_paths:
        if imageDurationEachImage:
            part = (os.path.splitext(os.path.basename(p))[0]).split('_')
            keyNumber = int(part[2]) if len(part) >= 3 else 0
            imageDuration = imageDurationEachImage[keyNumber] if keyNumber != 0 else imageDuration

        # clips.append(make_zoom_clip(p, imageDuration, fps, transitionDuration, zoomStrength))
        clip = make_zoom_clip(p, imageDuration, fps, transitionDuration, zoomStrength)
        if finalVideoSize:
            clip = clip.resized(new_size=finalVideoSize)
            # clips.append(clip)
        clips.append(clip)

    clip_generation_end_time = datetime.now()

    if additionalImagePath:
        additional_clip = ImageClip(additionalImagePath).with_duration(imageDuration).with_position('center').with_effects([vfx.CrossFadeIn(transitionDuration)]).with_effects([vfx.CrossFadeOut(transitionDuration)])
        if finalVideoSize:
            additional_clip = additional_clip.resized(new_size=finalVideoSize)
        additional_clip = additional_clip.with_effects([vfx.CrossFadeIn(transitionDuration), vfx.CrossFadeOut(transitionDuration)])
        clips.append(additional_clip)    

    final = concatenate_videoclips(clips, method=imageCombineMethod, padding=-transitionDuration)

    # Freeze last frame if audio is longer than video
    video_duration = final.duration
    if audio_duration > video_duration:
        logging.info("Audio is longer than video. Freezing the last frame of the video.")
        freeze = final.to_ImageClip(t=video_duration - 1, duration=audio_duration - video_duration)
        freeze = freeze.with_fps(fps).resized(final.size)
        final = concatenate_videoclips([final, freeze], method=imageCombineMethod)

    # Add audio/music
    if music_path:
        music = AudioFileClip(music_path)
        music_looped_quiet = music.with_effects([
            AudioLoop(duration=final.duration),
            MultiplyVolume(float(musicLoudness.strip('%')) / 100)
        ])
        combined_audio = CompositeAudioClip([audio_clip, music_looped_quiet])
        final = final.with_audio(combined_audio)
    else:
        final = final.with_audio(audio_clip)

    if finalVideoSize:
        final = final.resized(new_size=finalVideoSize)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)


    print(f"Parameters are: {fps} --> {videoCode} --> {videoPreset} --> {videoThreds}")
    video_generation_start_time = datetime.now()
    final.write_videofile(output_path,
                          fps=fps,
                          codec=videoCode,
                          preset=videoPreset,
                          threads=videoThreds,
                          logger=None, # You can also set logger=None to see all messages
                          ffmpeg_params=[
                              '-loglevel', 'verbose',
                              '-c:v', 'h264_nvenc',
                              '-preset', 'p1',          # GPU preset (p1 fastest, p7 best quality)
                              '-b:v', '5M',             # video bitrate
                              '-maxrate', '5M',
                              '-bufsize', '10M',
                              '-pix_fmt', 'yuv420p'     # pixel format
                          ]
                          )


    video_generation_end_time = datetime.now()

    print(f"Clip append time : {clip_generation_end_time - clip_generation_start_time}")
    print(f"video generation time: {video_generation_end_time - video_generation_start_time}")
    print(f"Master time taken: {video_generation_end_time - master_start_time}")