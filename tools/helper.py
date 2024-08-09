import argparse
import os
import sys
import cv2
from imutils import contours
import numpy as np
# read argument
def getFileLocation():
    parser = argparse.ArgumentParser(description="Process a file path and file name.")
    parser.add_argument(
        "file_path", 
        type=str, 
        nargs='?',  # Makes this argument optional
        default="/tools/testing/1",  # Default value
        help="The path to the file"
    )
    parser.add_argument(
        "file_name", 
        type=str, 
        nargs='?',  # Makes this argument optional
        default="sat.png",  # Default value
        help="The name of the file"
    )
    args = parser.parse_args()
    cwd = os.getcwd()
    file_path = os.path.join(cwd,args.file_path, args.file_name)
    dir_path  = os.path.join(cwd,args.file_path)
    if os.path.exists(file_path):
        print(f"The file '{file_path}' exists.")
        return dir_path,file_path
        
    else:
        print(f"The file '{file_path}' does not exist.")
        return None, None
# use relative path    
def getFileLocationRel():
    parser = argparse.ArgumentParser(description="Process a file path and file name.")
    parser.add_argument(
        "file_path", 
        type=str, 
        nargs='?',  # Makes this argument optional
        default="./tools/testing/1",  # Default value
        help="The path to the file"
    )
    args = parser.parse_args()
    #print (args.file_path)
    save_path  = os.path.dirname(args.file_path)
    if os.path.exists(args.file_path):
        print(f"The file '{args.file_path}' exists.")
        return args.file_path, save_path
        
    else:
        return None, None
    
def analyzeImage(image,minArea):
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
    bounding_box = []
    # Get bounding box of each question, crop ROI, and save
    question_number = 0
    for c in cnts:
        # Filter by area to ensure its not noise
        area = cv2.contourArea(c)
        if area > minArea:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0,255,0), 5)
            bounding_box.append(np.array([x,y,w,h]))
    return original,thresh,dilate,image,bounding_box