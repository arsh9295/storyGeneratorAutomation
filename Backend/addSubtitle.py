import subprocess

def burn_subtitles_ffmpeg(video_path, srt_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FF00&'",
        '-c:a', 'copy',
        output_path
    ]

    subprocess.run(command, check=True)