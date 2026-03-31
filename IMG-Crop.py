import cv2

img = cv2.imread("page2.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

table_rois = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    area = w * h
    # Filter out tiny boxes (like page numbers or logos)
    if area > 253700:   # adjust threshold depending on your image size
        roi = img[y:y+h, x:x+w]
        table_rois.append(roi)
        cv2.imwrite(f"table_{len(table_rois)}.png", roi)



