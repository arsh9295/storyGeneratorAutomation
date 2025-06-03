import whisper


def generateSRTFromAudio(audioFileClip, outputSRTPath):
    model = whisper.load_model("medium")  # "base" or "small", "medium", "large" for higher accuracy
    result = model.transcribe(audioFileClip,)
    # Save as .srt
    with open(outputSRTPath, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], start=1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            def format_time(t):
                hrs, rem = divmod(int(t), 3600)
                mins, secs = divmod(rem, 60)
                millis = int((t - int(t)) * 1000)
                return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

            f.write(f"{i}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")
