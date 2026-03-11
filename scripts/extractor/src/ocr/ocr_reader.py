import pytesseract
import cv2


def extract_text(image_path):

    image = cv2.imread(str(image_path))

    text = pytesseract.image_to_string(image)

    return text