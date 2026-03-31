import cv2
import pytesseract

# Tell pytesseract where the exe is
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\bakshima\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Load the image
img = cv2.imread("table_1.png")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Optional: threshold to clean background
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Run OCR
text = pytesseract.image_to_string(thresh, lang="eng")

print(text)
