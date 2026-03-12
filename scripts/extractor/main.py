import json
import os
from pathlib import Path
from src.ocr.ocr_reader import extract_text
from src.utils.image_preprocess import preprocess_image
from src.utils.text_cleaner import clean_text
from src.parser.brochure_parser import parse_brochure
from src.parser.json_builder import build_json
from src.utils.logger import get_logger

logger = get_logger()

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FOLDER = SCRIPT_DIR / "input"
PROJECT_ROOT = SCRIPT_DIR.parent.parent
OUTPUT_FOLDER = PROJECT_ROOT / "output" / "videos"

def process_brochure(image_path):
    logger.info(f"🚀 Processing brochure: {image_path.name}")
    try:
        processed_image = preprocess_image(image_path)
        raw_text = extract_text(processed_image)
        cleaned_text = clean_text(raw_text)
        parsed_data = parse_brochure(cleaned_text)
        json_data = build_json(parsed_data)

        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        # Use image stem (e.g., brochure1) for the JSON name
        output_file = OUTPUT_FOLDER / f"{image_path.stem}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

        logger.info(f"✅ Metadata created: {output_file.name}")
    except Exception as e:
        logger.error(f"❌ Error in {image_path.name}: {e}")

def main():
    INPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    images = [img for img in INPUT_FOLDER.glob("*.*") if img.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    if not images:
        print(f"⚠️ No brochures found in {INPUT_FOLDER}")
        return
    for image in images:
        process_brochure(image)

if __name__ == "__main__":
    main()