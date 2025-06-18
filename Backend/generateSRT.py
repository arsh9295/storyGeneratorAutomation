import whisper


# def generateSRTFromAudio(audioFileClip, outputSRTPath):
#     model = whisper.load_model("medium")  # "base" or "small", "medium", "large" for higher accuracy
#     result = model.transcribe(audioFileClip,)
#     # Save as .srt
#     with open(outputSRTPath, "w", encoding="utf-8") as f:
#         for i, segment in enumerate(result["segments"], start=1):
#             start = segment["start"]
#             end = segment["end"]
#             text = segment["text"].strip()

#             def format_time(t):
#                 hrs, rem = divmod(int(t), 3600)
#                 mins, secs = divmod(rem, 60)
#                 millis = int((t - int(t)) * 1000)
#                 return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

#             f.write(f"{i}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")



############l New code ############
import whisper

def format_time(t):
    hrs, rem = divmod(int(t), 3600)
    mins, secs = divmod(rem, 60)
    millis = int((t - int(t)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

def split_segment_text(text, start, end, max_words=7):
    words = text.strip().split()
    total_duration = end - start
    avg_word_duration = total_duration / max(len(words), 1)

    chunks = []
    for i in range(0, len(words), max_words):
        chunk_words = words[i:i+max_words]
        chunk_text = ' '.join(chunk_words)
        chunk_start = start + i * avg_word_duration
        chunk_end = start + min(len(words), i + max_words) * avg_word_duration
        chunks.append((chunk_start, chunk_end, chunk_text))
    return chunks

def generateSRTFromAudio(audioFileClip, outputSRTPath):
    model = whisper.load_model("medium")
    result = model.transcribe(audioFileClip)

    with open(outputSRTPath, "w", encoding="utf-8") as f:
        counter = 1
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            # Split long segments into short subtitle chunks
            subtitle_chunks = split_segment_text(text, start, end, max_words=7)

            for chunk_start, chunk_end, chunk_text in subtitle_chunks:
                f.write(f"{counter}\n")
                f.write(f"{format_time(chunk_start)} --> {format_time(chunk_end)}\n")
                f.write(f"{chunk_text}\n\n")
                counter += 1
