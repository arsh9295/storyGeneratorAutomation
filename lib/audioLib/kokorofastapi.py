import requests
# from openai import OpenAI
import os

FOOOCUS_HOST = os.getenv("FOOOCUS_HOST", "story1-fooocus")
FOOOCUS_PORT = int(os.getenv("FOOOCUS_PORT", "8888"))
KOKORO_HOST = os.getenv("KOKORO_HOST", "localhost")
# KOKORO_HOST = os.getenv("KOKORO_HOST", "story1-kokoro")
KOKORO_PORT = int(os.getenv("KOKORO_PORT", "9000"))
# KOKORO_PORT = int(os.getenv("KOKORO_PORT", "8880"))
API_URL = f"http://{KOKORO_HOST}:{KOKORO_PORT}/v1/audio/speech"

def synthesize(text: str, voice: str = "af_sky+af_bella", model: str = "kokoro", format: str = "wav", OutputPath="hello output.mp3", speed: float = .85, output_file_name=None) -> bytes:
    # client = OpenAI(base_url=f"http://{KOKORO_HOST}:{KOKORO_PORT}/v1/audio/speech", api_key="not-needed")
    payload = {
        "model": "kokoro",
        "voice": "af_bella",
        "input": text,
        "response_format": format,
        "speed": 1
    }
    # payload = {
    #     "model": model,
    #     "voice": voice,
    #     "input": text,
    #     "response_format": "wav",
    #     "speed": speed
    # }
    print(f"Payload is: {payload}")
    resp = requests.post(API_URL, json=payload)
    print("STATUS:", resp.status_code)
    print("HEADERS:", resp.headers)

    try:
        resp.raise_for_status()
    except requests.HTTPError:
        print("Server response:", resp.text)
        raise

    print(f"Content length: {len(resp.content)} bytes")
    save_audio(resp.content, f"{OutputPath}/{output_file_name}.{format}")
    return resp.content

def save_audio(data: bytes, filename: str):
    # audioFileName = os.path.basename(filename)
    print(filename)
    with open("/app/configs/filenameoutput.txt", "w") as f:
        f.write(filename)
    with open(f"{filename}", "wb") as f:
        f.write(data)
    print(f"Audio saved to {filename}")

# if __name__ == "__main__":
#     text = "Hello, this is a test from Kokoro TTS!"
#     audio = synthesize(text=text, voice="af_sarah", format="mp3")
#     save_audio(audio, "output.mp3")
