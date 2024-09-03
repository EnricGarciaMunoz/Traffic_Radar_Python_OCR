import cv2  # type: ignore
import numpy as np # type: ignore
import pytesseract  # type: ignore

# Specify the path to Tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extract_plate_text(image_path):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        return "Image not found"

    # Convert to hsvc color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get binary-mask
    msk = cv2.inRange(hsv, np.array([0, 0, 175]), np.array([179, 255, 255]))
    krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dlt = cv2.dilate(msk, krn, iterations=1)
    thr = 255 - cv2.bitwise_and(dlt, msk)

    # OCR
    plate_text = pytesseract.image_to_string(thr, config="--psm 10")
    return plate_text.strip()  # Usar strip para limpiar espacios en blanco