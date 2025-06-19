import subprocess

def burn_subtitles_ffmpeg(video_path, srt_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={srt_path}:force_style='FontName=Ubuntu,FontSize=23,PrimaryColour=&H00FF00&,OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=1,Alignment=8,MarginV=40'",
        '-c:a', 'copy',
        output_path
    ]

    subprocess.run(command, check=True)


# import subprocess

# def burn_subtitles_ffmpeg(video_path, srt_path, output_path):
#     command = [
#         'ffmpeg',
#         '-i', video_path,
#         '-vf', f"subtitles={srt_path}:force_style='FontName=Ubuntu, FontSize=23, PrimaryColour=&H00FF00&, OutlineColour=&H000000&, BorderStyle=1, Outline=2, Shadow=1, Alignment=2, MarginV=40'",
#         '-c:a', 'copy',
#         output_path
#     ]

#     subprocess.run(command, check=True)



# import subprocess
from pathlib import Path

def burn_ass_subtitles(video_path, subtitle_path, output_path):
    # Convert paths to POSIX format (with forward slashes)
    video_path = Path(video_path).as_posix()
    subtitle_path = Path(subtitle_path).as_posix()
    output_path = Path(output_path).as_posix()

    # Enclose subtitle path in single quotes to avoid parsing errors
    subtitle_filter = f"ass='{subtitle_path}'"

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", subtitle_filter,
        "-c:a", "copy",
        output_path
    ]

    print("▶️ Running FFmpeg command:")
    print(" ".join(command))

    subprocess.run(command, check=True)    