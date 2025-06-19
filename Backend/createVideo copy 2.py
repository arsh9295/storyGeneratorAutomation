from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from moviepy.audio.fx import AudioLoop, MultiplyVolume

def createVideoMviepy(video_path, audio_path, output_path, music_path):
    video = VideoFileClip(video_path)
    main_audio = AudioFileClip(audio_path)
    music = AudioFileClip(music_path)

    # Adjust video to match main audio duration
    if main_audio.duration > video.duration:
        freeze = video.to_ImageClip(
            t=video.duration - 1,
            duration=main_audio.duration - video.duration
        ).with_fps(video.fps).resized(video.size)
        final_video = concatenate_videoclips([video, freeze], method="compose")
    else:
        final_video = video.subclipped(0, main_audio.duration)

    # Prepare looped and volume-adjusted music in one step
    music_looped_quiet = music.with_effects([
        AudioLoop(duration=final_video.duration),
        MultiplyVolume(0.05)
    ])

    # Trim main audio to match video length
    main_trimmed = main_audio.subclipped(0, final_video.duration)

    # Combine both audio tracks
    combined_audio = CompositeAudioClip([main_trimmed, music_looped_quiet])
    final_video = final_video.with_audio(combined_audio)

    # Export final video
    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=16
    )
