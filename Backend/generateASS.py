
# FOR EACH WORD POP (Zoom In + YELLOW) EFFECT.

from faster_whisper import WhisperModel

def format_ass_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{hrs}:{mins:02}:{secs:02}.{cs:02}"

def generateASSWithKaraoke(audioFileClip, outputASSPath):
    model = WhisperModel("base", device="cuda", compute_type="float16")
    segments, _ = model.transcribe(audioFileClip, word_timestamps=True)

    with open(outputASSPath, "w", encoding="utf-8") as f:
        # Header
        f.write("[Script Info]\n")
        f.write("Title: Word Pop Subtitles\n")
        f.write("ScriptType: v4.00+\n")
        f.write("PlayResX: 1080\n")
        f.write("PlayResY: 1920\n\n")

        # Styles
        f.write("[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
                "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
                "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: WordPop,Arial,20,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,"
                "-1,0,0,0,100,100,0,0,1,3,1,5,30,30,30,1\n\n")

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
                word_start = int((word.start - seg_start) * 1000)  # ms relative to segment
                word_end = int((word.end - seg_start) * 1000)
                clean_word = word.word.strip().replace('{', '').replace('}', '')

                # Animation timing for each word
                pop_tag = (
                    f"{{\\fs48\\1c&HFFFFFF&"
                    f"\\t({word_start},{word_start+100},\\fs48\\1c&H00FFFF&)"  # pop: 0.1s grow
                    f"\\t({word_end},{word_end+100},\\fs48\\1c&HFFFFFF&)}}"
                )
                dialogue_line += f"{pop_tag}{clean_word} "

            f.write(f"Dialogue: 0,{start},{end},WordPop,,0,0,0,,{dialogue_line.strip()}\n")





# # FOR KARAOKE YELLOW TEXT FILL ANIMATION EFFECT

# from faster_whisper import WhisperModel

# def format_ass_time(seconds):
#     hrs = int(seconds // 3600)
#     mins = int((seconds % 3600) // 60)
#     secs = int(seconds % 60)
#     cs = int((seconds - int(seconds)) * 100)
#     return f"{hrs}:{mins:02}:{secs:02}.{cs:02}"

# def generateASSWithKaraoke(audioFileClip, outputASSPath):
#     model = WhisperModel("base", device="cuda", compute_type="float16")  # Adjust if needed
#     segments, _ = model.transcribe(audioFileClip, word_timestamps=True)

#     with open(outputASSPath, "w", encoding="utf-8") as f:
#         # ASS header
#         f.write("[Script Info]\n")
#         f.write("Title: Whisper Karaoke\n")
#         f.write("ScriptType: v4.00+\n")
#         f.write("PlayResX: 1280\n")
#         f.write("PlayResY: 720\n\n")

#         # Styles
#         f.write("[V4+ Styles]\n")
#         f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
#                 "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
#                 "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")

#         f.write("Style: Karaoke,Arial,52,&H0000FFFF,&H00FFFFFF,&H00000000,&H64000000,"
#                 "-1,0,0,0,100,100,0,0,1,3,1,2,30,30,30,1\n\n")

#         # Events
#         f.write("[Events]\n")
#         f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

#         for seg in segments:
#             if not seg.words:
#                 continue

#             start = format_ass_time(seg.start)
#             end = format_ass_time(seg.end)

#             dialogue_line = ""
#             for word in seg.words:
#                 dur_cs = int((word.end - word.start) * 100)  # duration in centiseconds
#                 clean_word = word.word.strip().replace('{', '').replace('}', '')
#                 dialogue_line += f"{{\\kf{dur_cs}}}{clean_word} "

#             # Add fade-in effect (optional) and write line
#             f.write(f"Dialogue: 0,{start},{end},Karaoke,,0,0,0,,{{\\fad(100,0)}}{dialogue_line.strip()}\n")