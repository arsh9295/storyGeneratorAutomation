from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip

def createVideoMviepy(video_path, audio_path, output_path):

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

    # Set the audio of the video clip
    final_video = final_video.with_audio(audio_clip)

    # Write the result to a file
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", preset='ultrafast', threads=16)
