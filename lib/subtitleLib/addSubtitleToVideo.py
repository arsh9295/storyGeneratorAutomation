import subprocess
from pathlib import Path
import sys, os, shutil

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import globalVariables as gv

def burnSubtitleToVideo(
    video_path=None,
    subtitle_path=None,
    output_path=None,
    subtitle_format=None,
    font_name=None,
    font_size=None,
    primary_color=None,
    outline_color=None,
    border_style=None,
    outline=None,
    shadow=None,
    alignment=None,
    margin_v=None,
    audio_codec=None,
    overwrite=None,
    dry_run=None
):
    print("SRT adding to video.. started")
    # Set defaults if not provided
    subtitle_format = subtitle_format if subtitle_format is not None else getattr(gv, 'subtitle_format', "ass")
    font_name = font_name if font_name is not None else getattr(gv, 'font_name', "Ubuntu")
    font_size = font_size if font_size is not None else getattr(gv, 'font_size', 23)
    primary_color = primary_color if primary_color is not None else getattr(gv, 'primary_color', "&H00FF00&")
    outline_color = outline_color if outline_color is not None else getattr(gv, 'outline_color', "&H000000&")
    border_style = border_style if border_style is not None else getattr(gv, 'border_style', 1)
    outline = outline if outline is not None else getattr(gv, 'outline', 2)
    shadow = shadow if shadow is not None else getattr(gv, 'shadow', 1)
    alignment = alignment if alignment is not None else getattr(gv, 'alignment', 8)
    margin_v = margin_v if margin_v is not None else getattr(gv, 'margin_v', 40)
    audio_codec = audio_codec if audio_codec is not None else getattr(gv, 'audio_codec', "copy")
    overwrite = overwrite if overwrite is not None else getattr(gv, 'overwrite', True)
    dry_run = dry_run if dry_run is not None else getattr(gv, 'dry_run', False)


    if not video_path or not subtitle_path or not output_path:
        raise ValueError("video_path, subtitle_path, and output_path must be provided.")

    if not os.path.exists(subtitle_path):
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")

    print(f"Subtitle Path: {subtitle_path}")

    # Convert to POSIX (forward-slash) format
    video_path = Path(video_path).as_posix()
    subtitle_path = Path(subtitle_path).as_posix()
    output_path = Path(output_path).as_posix()

    # Subtitle filter depending on format
    if subtitle_format.lower() == "ass":
        subtitle_filter = f"ass='{subtitle_path}'"
    elif subtitle_format.lower() == "srt":
        subtitle_filter = (
            f"subtitles='{subtitle_path}':force_style="
            f"'FontName={font_name},FontSize={font_size},"
            f"PrimaryColour={primary_color},OutlineColour={outline_color},"
            f"BorderStyle={border_style},Outline={outline},"
            f"Shadow={shadow},Alignment={alignment},MarginV={margin_v}'"
        )
    else:
        raise ValueError("subtitle_format must be 'srt' or 'ass'")

    command = [
        "ffmpeg",
        "-y" if overwrite else "-n",
        "-i", video_path,
        "-vf", subtitle_filter,
        "-c:a", audio_codec,
        output_path
    ]

    # print("▶️ Running FFmpeg command:")
    # print(" ".join(command))

    if not dry_run:
        subprocess.run(command, check=True)

    # Move SRT to respective directory
    # if os.path.exists(video_path):
    #     os.remove(video_path)
    destination_path = os.path.dirname(video_path)
    shutil.move(subtitle_path, destination_path)