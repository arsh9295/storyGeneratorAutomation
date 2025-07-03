from transformers import AutoModel
import numpy as np
import soundfile as sf

# Load INF5 from Hugging Face
repo_id = "ai4bharat/IndicF5"
model = AutoModel.from_pretrained(repo_id, trust_remote_code=True)

# Generate speech
audio = model(
    "नमस्ते! संगीत की तरह जीवन भी खूबसूरत होता है, बस इसे सही ताल में जीना आना चाहिए.",
    ref_audio_path="C:/Users/User/Downloads/ElevenLabs_Text_to_Speech_audio.mp3",
    ref_text="प्राचीन भूमि एल्डोरिया में, जहाँ आकाश चमकते थे और जंगल हवा को राज़ फुसफुसाते थे, वहाँ ज़ेफिरोस नाम का एक ड्रैगन रहता था। वह “सब कुछ जला दो” वाला नहीं था... बल्कि वह कोमल, बुद्धिमान था, जिसकी आँखें पुराने सितारों जैसी थीं। जब वह गुजरता था तो पक्षी भी चुप हो जाते थे।"
)

# Normalize and save output
if audio.dtype == np.int16:
    audio = audio.astype(np.float32) / 32768.0
sf.write("samples/namaste.wav", np.array(audio, dtype=np.float32), samplerate=24000)