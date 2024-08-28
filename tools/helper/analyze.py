import argparse
import os
import sys
import cv2
from imutils import contours
import numpy as np
from pdf2image import convert_from_path
from . import boundingBox as bb
# This file contain logic that extract individual questions from image
# General idea is based on this answer on stackoverflow
# https://stackoverflow.com/questions/71882225/slicing-of-a-scanned-image-based-on-large-white-spaces/71882633#71882633 

def analyzeImage(image,minArea,paper_type,kernel_shape,top,buttom):
    
    # crop image 
    height = image.shape[0]
    image = image[top*height//100:(100-buttom)*height//100,:]
    """
    (default) Paper Type 1 : Question number lead Question content
    For example:  
    Q1  : xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
          (a) ... (b) ... (c)... (d) ...
    Q2  : xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
          (a) ... (b) ... (c)... (d) ...
    Q3  : xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
          (a) ... (b) ... (c)... (d) ...
       
    Paper Type 2 : Split page Like SAT exam
    For example:  
     Q1 : xxxxxxxxxxxxx                      |    Q3: xxxxxxxxxxxxx
           (a) ... (b) ... (c)... (d) ...    |      (a) ... (b) ... (c)... (d) ...
     Q2 : xxxxxxxxxxxxx                      |  Q4: xxxxxxxxxxxxx
            (a) ... (b) ... (c)... (d) ...   |    (a) ... (b) ... (c)... (d) ...
     
    Paper Type 3 : Question number and Question content are aligned
    For example:  
        Q1  : xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        (a) ... (b) ... (c)... (d) ...
        
        Q2  : xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        (a) ... (b) ... (c)... (d) ...
        
        Q3  : xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        (a) ... (b) ... (c)... (d) ...      
         
     
     
    """
    if (paper_type==1):
        original = image.copy()
        original_width = original.shape[1]
        
        # Remove horizontal line    
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (300,5))
        detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(image, [c], -1, (255,255,255), 2)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # Remove small artifacts and noise with morph open
        open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, open_kernel, iterations=1)
        
        # Create rectangular structuring element and dilate
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_shape)
        dilate = cv2.dilate(opening, kernel, iterations=5)

        # Find contours, sort from top to bottom, and extract each question
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        try:
            (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
        except Exception as e:
            return original,thresh,dilate,original,[]
        
        bounding_box = []
        # Get bounding box of each question, crop ROI, and save
        question_number = 0
        for c in cnts:
            # Filter by area to ensure its not noise
            area = cv2.contourArea(c)
            if area > minArea:
                x,y,w,h = cv2.boundingRect(c)
                bounding_box.append(np.array([x,y,w,h]))
        bounding_box = bb.mergeRelatedBoundingBoxes(bounding_box,original_width,0.01)
        for b in bounding_box:
            x,y,w,h = b
            cv2.rectangle(image, (x, y), (x + w, y + h), (0,255,0), 5)
            
    elif (paper_type==3):
        
        original = image.copy()
        original_width = original.shape[1]
        
        # Remove horizontal line    
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (300,1))
        detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(image, [c], -1, (255,255,255), 2)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Remove small artifacts and noise with morph open
        open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, open_kernel, iterations=1)
        
        # Create rectangular structuring element and dilate
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_shape)
        dilate = cv2.dilate(opening, kernel, iterations=5)

        # Find contours, sort from top to bottom, and extract each question
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        try:
            (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
        except Exception as e:
            return original,thresh,dilate,original,[]
        bounding_box = []
        # Get bounding box of each question, crop ROI, and save
        question_number = 0
        for c in cnts:
            # Filter by area to ensure its not noise
            area = cv2.contourArea(c)
            if area > minArea:
                x,y,w,h = cv2.boundingRect(c)
                bounding_box.append(np.array([x,y,w,h]))
        for b in bounding_box:
            x,y,w,h = b
            cv2.rectangle(image, (x, y), (x + w, y + h), (0,255,0), 5) 
                   
    elif (paper_type==2):
        original = image.copy()
        original_width = original.shape[1]
        cut_off = original_width//2
        # Remove horizontal line    
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,1))
        detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(image, [c], -1, (255,255,255), 2)

        # Remove vertical line    
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,10))
        detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(image, [c], -1, (255,255,255), 2)            
            
            
        # split by half
        image_l = image[:,:cut_off]
        original_l = original[:,:cut_off].copy()
        image_r = image[:,cut_off:]
        original_r = original[:,cut_off:].copy()
        gray_l = cv2.cvtColor(image_l, cv2.COLOR_BGR2GRAY)
        blur_l = cv2.GaussianBlur(gray_l, (7,7), 0)
        _,thresh_l = cv2.threshold(blur_l, 250, 255, cv2.THRESH_BINARY_INV)
        gray_r = cv2.cvtColor(image_r, cv2.COLOR_BGR2GRAY)
        blur_r = cv2.GaussianBlur(gray_r, (7,7), 0)
        _,thresh_r = cv2.threshold(blur_r, 250, 255, cv2.THRESH_BINARY_INV)
        
        # Remove small artifacts and noise with morph open
        open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
        opening_l = cv2.morphologyEx(thresh_l, cv2.MORPH_OPEN, open_kernel, iterations=1)
        opening_r = cv2.morphologyEx(thresh_r, cv2.MORPH_OPEN, open_kernel, iterations=1)
        
        # Create rectangular structuring element and dilate
        kernel= cv2.getStructuringElement(cv2.MORPH_RECT, kernel_shape)
        dilate_l = cv2.dilate(opening_l, kernel, iterations=5)
        dilate_r = cv2.dilate(opening_r, kernel, iterations=5)

        # Find contours, sort from top to bottom, and extract each question
        cnts_l= cv2.findContours(dilate_l, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_l = cnts_l[0] if len(cnts_l) == 2 else cnts_l[1]
        try:
            (cnts_l,_) = contours.sort_contours(cnts_l, method="top-to-bottom")
        except Exception as e:
            return original,thresh,dilate,original,[]
        bounding_box_l = []
        cnts_r = cv2.findContours(dilate_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_r = cnts_r[0] if len(cnts_r) == 2 else cnts_r[1]
        try:
            (cnts_r,_) = contours.sort_contours(cnts_r, method="top-to-bottom")
        except Exception as e:
            return original,thresh,dilate,original,[]
        bounding_box_r = []
        # Get bounding box of each question, crop ROI, and save
        question_number = 0
        for c in cnts_l:
            # Filter by area to ensure its not noise
            area = cv2.contourArea(c)
            if area > minArea:
                x,y,w,h = cv2.boundingRect(c)
                bounding_box_l.append(np.array([x,y,w,h]))
        bounding_box_l = bb.mergeRelatedBoundingBoxes(bounding_box_l,cut_off,0.01)
        for b in bounding_box_l:
            x,y,w,h = b
            cv2.rectangle(original_l, (x, y), (x + w, y + h), (0,255,0), 5)
        for c in cnts_r:
            # Filter by area to ensure its not noise
            area = cv2.contourArea(c)
            if area > minArea:
                x,y,w,h = cv2.boundingRect(c)
                bounding_box_r.append(np.array([x,y,w,h]))
        bounding_box_r = bb.mergeRelatedBoundingBoxes(bounding_box_r,cut_off,0.01)
        for b in bounding_box_r:
            x,y,w,h = b
            cv2.rectangle(original_r, (x, y), (x + w, y + h), (0,0,255), 5)
        image = cv2.hconcat([original_l,original_r])
        dilate = cv2.hconcat([dilate_l,dilate_r])
        thresh = cv2.hconcat([thresh_l,thresh_r])
        bounding_box  = bb.combineTwoHalf(bounding_box_l,bounding_box_r,cut_off)
    else:
        print("invalid paper type")
         
    return original,thresh,dilate,image,bounding_box

def analyzePicture(file_path,output_dir,paper_type,kernel_shape,top,buttom):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print (f"analyzing {file_path}")
    image = cv2.imread(file_path)
    minArea = 0.0005*image.shape[0]*image.shape[1]
    original,thresh,dilate,output,bounding_boxes = analyzeImage(image,minArea,paper_type,kernel_shape,top,buttom)
    #for i,b in enumerate(bounding_boxes):
    #save_path = os.path.join(save_dir, 'P_{}_q_{}.png'.format(i+1,question_number))
    #cv2.imwrite(save_path_image, question)
    
    cv2.imwrite(os.path.join(output_dir,'output.png'),output)
    cv2.imwrite(os.path.join(output_dir,'dilate.png'),dilate)
    cv2.imwrite(os.path.join(output_dir,'threshold.png'),thresh)
    print (f"Output file: {file_path}/output")
    
    
def analyzePdf(file_path,output_dir,paper_type,kernel_shape,top,buttom):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    images = convert_from_path(file_path)
    for i,image in enumerate(images):
        print (f"analyzing page {i+1}")
        image = np.array(image)
        minArea = 0.001*image.shape[0]*image.shape[1]
        original,thresh,dilate,output,bounding_boxes = analyzeImage(image,minArea,paper_type,kernel_shape,top,buttom)
        #for i,b in enumerate(bounding_boxes):
        #save_path = os.path.join(save_dir, 'P_{}_q_{}.png'.format(i+1,question_number))
        #cv2.imwrite(save_path_image, question)
        cv2.imwrite(os.path.join(output_dir,'output_P_{}.png'.format(i+1)),output)
        cv2.imwrite(os.path.join(output_dir,'dilate_P_{}.png'.format(i+1)),dilate)
        cv2.imwrite(os.path.join(output_dir,'threshold_{}.png'.format(i+1)),thresh)
    print (f"Output file: {file_path}/output")