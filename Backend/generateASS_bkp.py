from faster_whisper import WhisperModel

def format_ass_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{hrs}:{mins:02}:{secs:02}.{cs:02}"

def generateASSWithKaraoke(audioFileClip, outputASSPath):
    model = WhisperModel("base", device="cuda", compute_type="float16")  # Change to "int8" or "float32" if needed
    segments, _ = model.transcribe(audioFileClip, word_timestamps=True)

    with open(outputASSPath, "w", encoding="utf-8") as f:
        # Write ASS header
        f.write("[Script Info]\n")
        f.write("Title: Whisper Karaoke\n")
        f.write("ScriptType: v4.00+\n")
        f.write("PlayResX: 1280\n")
        f.write("PlayResY: 720\n\n")

        f.write("[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
                "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
                "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: Karaoke,Arial,50,&H00FFFFFF,&H00FFFF00,&H00000000,&H64000000,"
                "0,0,0,0,100,100,0,0,1,2,1,2,30,30,30,1\n\n")

        f.write("[Events]\n")
        f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

        for seg in segments:
            if not seg.words:
                continue

            start = format_ass_time(seg.start)
            end = format_ass_time(seg.end)

            dialogue_line = ""
            for word in seg.words:
                dur_cs = int((word.end - word.start) * 100)  # in centiseconds
                clean_word = word.word.strip().replace('{', '').replace('}', '')
                dialogue_line += f"{{\\kf{dur_cs}}}{clean_word} "

            f.write(f"Dialogue: 0,{start},{end},Karaoke,,0,0,0,,{dialogue_line.strip()}\n")
