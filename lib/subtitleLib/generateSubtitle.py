import os, sys
from faster_whisper import WhisperModel

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import globalVariables as gv

def format_ass_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{hrs}:{mins:02}:{secs:02}.{cs:02}"

def generateASSWithKaraoke(
    audioFilePath,
    outputASSPath,
    model_name=None,
    device=None,
    compute_type=None,
    font_name=None,
    font_size=None,
    primary_color=None,
    highlight_color=None,
    outline_color=None,
    back_color=None,
    resolution=None,
    style_name=None,
    alignment=None,
    margin=None,
    pop_duration_ms=None,
    zoom_font_size=None
):
    # Set defaults if not provided
    model_name = model_name if model_name is not None else getattr(gv, 'model_name', "base")
    device = device if device is not None else getattr(gv, 'device', "cuda")
    compute_type = compute_type if compute_type is not None else getattr(gv, 'compute_type', "float16")
    font_name = font_name if font_name is not None else getattr(gv, 'font_name', "Arial")
    font_size = font_size if font_size is not None else getattr(gv, 'font_size', 20)
    primary_color = primary_color if primary_color is not None else getattr(gv, 'primary_color', "&H00FFFFFF&")
    highlight_color = highlight_color if highlight_color is not None else getattr(gv, 'highlight_color', "&H00FFFF&")
    outline_color = outline_color if outline_color is not None else getattr(gv, 'outline_color', "&H00000000&")
    back_color = back_color if back_color is not None else getattr(gv, 'back_color', "&H64000000&")
    resolution = resolution if resolution is not None else getattr(gv, 'resolution', (1080, 1920))
    style_name = style_name if style_name is not None else getattr(gv, 'style_name', "WordPop")
    alignment = alignment if alignment is not None else getattr(gv, 'alignment', 5)
    margin = margin if margin is not None else getattr(gv, 'margin', (30, 30, 30))
    pop_duration_ms = pop_duration_ms if pop_duration_ms is not None else getattr(gv, 'pop_duration_ms', 100)
    zoom_font_size = zoom_font_size if zoom_font_size is not None else getattr(gv, 'zoom_font_size', 48)

    print("Creating ass started...")
    # Load Whisper model
    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, _ = model.transcribe(audioFilePath, word_timestamps=True)

    playres_x, playres_y = resolution
    margin_l, margin_r, margin_v = margin

    with open(outputASSPath, "w", encoding="utf-8") as f:
        # Header
        f.write("[Script Info]\n")
        f.write("Title: Word Pop Subtitles\n")
        f.write("ScriptType: v4.00+\n")
        f.write(f"PlayResX: {playres_x}\n")
        f.write(f"PlayResY: {playres_y}\n\n")

        # Styles
        f.write("[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
                "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
                "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write(
            f"Style: {style_name},{font_name},{font_size},{primary_color},{highlight_color},"
            f"{outline_color},{back_color},-1,0,0,0,100,100,0,0,1,3,1,{alignment},"
            f"{margin_l},{margin_r},{margin_v},1\n\n"
        )

        # Events
        f.write("[Events]\n")
        f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

        for seg in segments:
            if not seg.words:
                continue

            start = format_ass_time(seg.start)
            end = format_ass_time(seg.end)
            seg_start = seg.start

            dialogue_line = ""
            for word in seg.words:
                word_start = int((word.start - seg_start) * 1000)
                word_end = int((word.end - seg_start) * 1000)
                clean_word = word.word.strip().replace('{', '').replace('}', '')

                pop_tag = (
                    f"{{\\fs{zoom_font_size}\\1c{primary_color}"
                    f"\\t({word_start},{word_start+pop_duration_ms},\\fs{zoom_font_size}\\1c{highlight_color})"
                    f"\\t({word_end},{word_end+pop_duration_ms},\\fs{zoom_font_size}\\1c{primary_color})}}"
                )
                dialogue_line += f"{pop_tag}{clean_word} "

            f.write(f"Dialogue: 0,{start},{end},{style_name},,0,0,0,,{dialogue_line.strip()}\n")

    print("Creating ass Completed...")
    return "Hello"
        
    # sys.exit(0)