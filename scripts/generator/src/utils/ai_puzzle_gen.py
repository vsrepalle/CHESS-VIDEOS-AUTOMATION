import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
# Initializing with the stable v1 API
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(api_version='v1')
)

def generate_ai_puzzle():
    # Using the latest 2026 workhorse model
    model_id = 'gemini-3.1-flash-lite-preview'
    prompt = "Create a unique chess puzzle. Return ONLY a JSON object with keys: fen, headline, hook_text, details."

    try:
        print(f"[AI] Requesting from {model_id}...")
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )

        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)

        fen_dir = r"C:\VISWA\CHESS_PRO_AUTOMATION\scripts\generator\input\FEN"
        if not os.path.exists(fen_dir): os.makedirs(fen_dir)
        base_name = "ai_puzzle_latest"

        with open(os.path.join(fen_dir, f"{base_name}.txt"), "w") as f: f.write(data['fen'])
        with open(os.path.join(fen_dir, f"{base_name}.json"), "w") as f: json.dump(data, f, indent=4)
        print(f"SUCCESS: Generated {data['headline']}")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    generate_ai_puzzle()
