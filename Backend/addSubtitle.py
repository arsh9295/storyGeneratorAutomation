import subprocess

def burn_subtitles_ffmpeg(video_path, srt_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={srt_path}:force_style='FontName=Ubuntu, FontSize=23, PrimaryColour=&H00FF00&, OutlineColour=&H000000&, BorderStyle=1, Outline=2, Shadow=1, Alignment=2, MarginV=40'",
        '-c:a', 'copy',
        output_path
    ]

    subprocess.run(command, check=True)