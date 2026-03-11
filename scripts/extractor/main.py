import json
from pathlib import Path

from src.ocr.ocr_reader import extract_text
from src.utils.image_preprocess import preprocess_image
from src.utils.text_cleaner import clean_text
from src.parser.brochure_parser import parse_brochure
from src.parser.json_builder import build_json
from src.utils.logger import get_logger


logger = get_logger()

INPUT_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")


def process_brochure(image_path):

    logger.info(f"Processing brochure: {image_path}")

    processed_image = preprocess_image(image_path)

    raw_text = extract_text(processed_image)

    cleaned_text = clean_text(raw_text)

    parsed_data = parse_brochure(cleaned_text)

    json_data = build_json(parsed_data)

    output_file = OUTPUT_FOLDER / f"{image_path.stem}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

    logger.info(f"JSON saved to {output_file}")


def main():

    OUTPUT_FOLDER.mkdir(exist_ok=True)

    for image in INPUT_FOLDER.glob("*.*"):

        if image.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            process_brochure(image)


if __name__ == "__main__":
    main()