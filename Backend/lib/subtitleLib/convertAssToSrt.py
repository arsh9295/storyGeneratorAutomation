# this script is to convert generated ass to srt. We can generate image based on srt text and also can put time stump matching to srt time stump to video

import re

def convertAssToSrtManual(input_ass, output_srt):
    with open(input_ass, 'r', encoding='utf-8') as fin, \
         open(output_srt, 'w', encoding='utf-8') as fout:

        in_events = False
        index = 1

        for line in fin:
            if line.strip().startswith("[Events]"):
                in_events = True
                continue

            if in_events and line.strip().startswith("Dialogue:"):
                parts = line.split(",", 9)  # ASS has 9 commas before the text
                if len(parts) < 10:
                    continue
                start, end, text = parts[1].strip(), parts[2].strip(), parts[9].strip()

                # Convert timestamps
                def parse_time(ts):
                    h, m, s_cs = ts.split(":")
                    s, cs = s_cs.split(".")
                    ms = int(cs) * 10
                    return f"{int(h):02}:{int(m):02}:{int(s):02},{ms:03}"

                start_srt, end_srt = parse_time(start), parse_time(end)

                # Remove all inline override tags {…}
                clean_text = re.sub(r"\{.*?\}", "", text)

                # Write to SRT
                fout.write(f"{index}\n")
                fout.write(f"{start_srt} --> {end_srt}\n")
                fout.write(clean_text + "\n\n")
                index += 1

    print(f"✅ Done! Clean .srt written to: {output_srt}")

# if __name__ == "__main__":
#     convert_ass_to_srt_manual("input.ass", "output_clean.srt")
