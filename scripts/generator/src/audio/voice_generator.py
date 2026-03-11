import os
from gtts import gTTS


def build_script(data):

    script = ""

    for key, value in data.items():
        if isinstance(value, str):
            script += value.strip() + ". "

    return script.strip()


def generate_voice(data, output_dir):

    print("Generating voice...", flush=True)

    script = build_script(data)

    if not script:
        raise Exception("No text available to generate voice")

    audio_path = os.path.join(output_dir, "voice.mp3")

    tts = gTTS(text=script, lang="en")

    tts.save(audio_path)

    print(f"Voice saved to: {audio_path}", flush=True)

    return audio_path