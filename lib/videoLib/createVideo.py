import os, sys
import logging

logger = logging.getLogger(__name__)
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from moviepy.audio.fx import AudioLoop, MultiplyVolume

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import globalVariables as gv

def createVideoMviepy(video_path, audio_path, output_path, music_path=None, finalVideoSize=None, imageCombineMethod=None, videoCode=None, videoPreset=None, videoThreds=None, audioCoded=None, musicLoudness=None):

    finalVideoSize = finalVideoSize if finalVideoSize is not None else getattr(gv, 'finalVideoSize', None)
    imageCombineMethod = imageCombineMethod if imageCombineMethod is not None else getattr(gv, 'imageCombineMethod', 'chain')
    videoCode = videoCode if videoCode is not None else getattr(gv, 'videoCode', 'libx264')
    videoPreset = videoPreset if videoPreset is not None else getattr(gv, 'videoPreset', 'ultrafast')
    videoThreds = videoThreds if videoThreds is not None else getattr(gv, 'videoThreds', 16)
    audioCoded = audioCoded if audioCoded is not None else getattr(gv, 'audioCoded', "acc")
    musicLoudness = musicLoudness if musicLoudness is not None else getattr(gv, 'musicLoudness', "10%")

    # Load video and audio
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Calculate how much longer the audio is
    video_duration = video_clip.duration
    audio_duration = audio_clip.duration

    logger.info(f"Video duration: {video_duration} seconds")
    logger.info(f"Audio duration: {audio_duration} seconds")

    if audio_duration > video_duration:
        logger.info("Audio is longer than video. Freezing the last frame of the video.")

        freeze = video_clip.to_ImageClip(t=video_duration - 1, duration=audio_duration - video_duration)
        freeze = freeze.with_fps(video_clip.fps).resized(video_clip.size)
        final_video = concatenate_videoclips([video_clip, freeze], method=imageCombineMethod)

    else:
        logger.info("Video is longer than or equal to audio. Trimming video to match audio.")
        # Trim video if it's longer than audio
        final_video = video_clip.subclipped(0, audio_duration)

    if music_path:
        logger.info("Found music path, adding music to video")
        music = AudioFileClip(music_path)
        # Prepare looped and volume-adjusted music in one step
        music_looped_quiet = music.with_effects([
            AudioLoop(duration=final_video.duration),
            MultiplyVolume(float(musicLoudness.strip('%')) / 100)
        ])
        combined_audio = CompositeAudioClip([audio_clip, music_looped_quiet])
        final_video = final_video.with_audio(combined_audio)
    else:
        # If no music is provided, just use the main audio
        final_video = final_video.with_audio(audio_clip)

    if(finalVideoSize):
        final_video = final_video.resized(new_size=finalVideoSize)

    # Export final video
    final_video.write_videofile(
        output_path,
        codec=videoCode,
        audio_codec=audioCoded,
        preset=videoPreset,
        threads=videoThreds
    )
