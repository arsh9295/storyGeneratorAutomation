from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from moviepy.audio.fx import AudioLoop, MultiplyVolume

def createVideoMviepy(video_path, audio_path, output_path, music_path=None):
    # Load video and audio
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Calculate how much longer the audio is
    video_duration = video_clip.duration
    audio_duration = audio_clip.duration

    print(f"Video duration: {video_duration} seconds")
    print(f"Audio duration: {audio_duration} seconds")

    if audio_duration > video_duration:
        print("Audio is longer than video. Freezing the last frame of the video.")

        freeze = video_clip.to_ImageClip(t=video_duration - 1, duration=audio_duration - video_duration)
        freeze = freeze.with_fps(video_clip.fps).resized(video_clip.size)
        final_video = concatenate_videoclips([video_clip, freeze], method="compose")

    else:
        print("Video is longer than or equal to audio. Trimming video to match audio.")
        # Trim video if it's longer than audio
        final_video = video_clip.subclipped(0, audio_duration)

    if music_path:
        music = AudioFileClip(music_path)
        # Prepare looped and volume-adjusted music in one step
        music_looped_quiet = music.with_effects([
            AudioLoop(duration=final_video.duration),
            MultiplyVolume(0.10)
        ])
        combined_audio = CompositeAudioClip([audio_clip, music_looped_quiet])
        final_video = final_video.with_audio(combined_audio)
    else:
        # If no music is provided, just use the main audio
        final_video = final_video.with_audio(audio_clip)

    # # Trim main audio to match video length
    # main_trimmed = main_audio.subclipped(0, final_video.duration)

    # Combine both audio tracks
    # combined_audio = CompositeAudioClip([main_trimmed, music_looped_quiet])
    # final_video = final_video.with_audio(combined_audio)

    # final_video = final_video.resize((1280, 720))

    # Export final video
    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=16
    )
