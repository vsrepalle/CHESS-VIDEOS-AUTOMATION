from src.ocr.ocr_reader import extract_text


def test_ocr():

    text = extract_text("input/sample.jpg")

    print(text)