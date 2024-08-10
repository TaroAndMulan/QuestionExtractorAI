import cv2
from helper import getFileLocation, getFileLocationRel,analyzeImage
from imutils import contours
import os
import numpy as np
from pdf2image import convert_from_path

# Load image, grayscale, Gaussian blur, Otsu's threshold
file_path,save_dir = getFileLocationRel()
print ("filepath: ",file_path)
images = convert_from_path(file_path)
print ("loaded")

for i,image in enumerate(images):
    print (f"analying page {i+1}")
    image = np.array(image)
    minArea = 0.001*image.shape[0]*image.shape[1]
    original,thresh,dilate,output,bounding_boxes = analyzeImage(image,minArea,(20,10))
    #for i,b in enumerate(bounding_boxes):
    #save_path = os.path.join(save_dir, 'P_{}_q_{}.png'.format(i+1,question_number))
    #cv2.imwrite(save_path_image, question)
    cv2.imwrite(os.path.join(save_dir,'Fp_{}.png'.format(i+1)),output)
    cv2.imwrite(os.path.join(save_dir,'Fdilatep_{}.png'.format(i+1)),dilate)
    cv2.imwrite(os.path.join(save_dir,'Fthresh_{}.png'.format(i+1)),thresh)



