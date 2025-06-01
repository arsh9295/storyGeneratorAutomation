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
        # # Freeze the last frame of the video and extend it
        # freeze_duration = audio_duration - video_duration
        # last_frame = video_clip.to_ImageClip(t=video_duration - 0.04)  # Last frame
        # last_frame = last_frame.with_duration(freeze_duration)

        # print(f"Freezing last frame for {freeze_duration} seconds.")
        # # Concatenate original video with frozen last frame
        # final_video = concatenate_videoclips([video_clip, last_frame])

        # Freeze the last frame
        last_frame = video_clip.get_frame(video_duration - 0.04)  # Get last video frame as image (numpy array)
        # freeze_duration = audio_duration - video_duration

        # # Create an ImageClip from the last frame
        # freeze_clip = ImageClip(last_frame).with_duration(freeze_duration)
        # freeze_clip = freeze_clip.with_fps(video_clip.fps)
        # freeze_clip = freeze_clip.resized(video_clip.size)

        # Create an ImageClip from the last frame
        freeze_clip = ImageClip(last_frame)
        freeze_clip = freeze_clip.with_duration(audio_duration - video_duration)
        freeze_clip = freeze_clip.with_fps(video_clip.fps)
        freeze_clip = freeze_clip.resized(video_clip.size)

        # Concatenate the original video with the freeze frame clip
        final_video = concatenate_videoclips([video_clip, freeze_clip], method="compose")        
    else:
        print("Video is longer than or equal to audio. Trimming video to match audio.")
        # Trim video if it's longer than audio
        final_video = video_clip.subclip(0, audio_duration)

    # Set the audio of the video clip
    final_video = final_video.with_audio(audio_clip)

    # Optional: set duration to match the shorter one (if they differ)
    final_duration = min(video_clip.duration, audio_clip.duration)
    final_video = final_video.subclipped(0, final_duration)

    # Write the result to a file
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
