import cv2
from helper import getFileLocation, getFileLocationRel
from imutils import contours
import os
# Load image, grayscale, Gaussian blur, Otsu's threshold
file_path,save_path = getFileLocationRel()
image = cv2.imread(file_path)
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Remove small artifacts and noise with morph open
open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, open_kernel, iterations=1)

# Create rectangular structuring element and dilate
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,18))
dilate = cv2.dilate(opening, kernel, iterations=5)

# Find contours, sort from top to bottom, and extract each question
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

# Get bounding box of each question, crop ROI, and save
question_number = 0
for c in cnts:
    # Filter by area to ensure its not noise
    area = cv2.contourArea(c)
    if area > 4000:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0,255,0), 5)
        question = original[y:y+h, x:x+w]
        save_path = os.path.join(save_path, 'question_{}.png'.format(question_number))
        cv2.imwrite(save_path, question)
        question_number += 1

cv2.imshow('thresh', thresh)
cv2.imshow('dilate', dilate)
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()