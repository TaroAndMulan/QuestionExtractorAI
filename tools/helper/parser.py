import argparse
import os
import sys
import cv2
from imutils import contours
import numpy as np
from pdf2image import convert_from_path

# python run.py [file_path]
# return "file_path" from command line argument    
# additionally return "save_path" which is the same directory as the input file 
def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path", 
        type=str, 
        default="./tools/testing/1/sat.png",  # Default value
    )
    # paper type
    parser.add_argument(
        "-type", 
        type=int, 
        nargs='?',  # Makes this argument optional
        default=1  # Default value
    )
    # dilate kernel
    parser.add_argument(
        "-kernel", 
        type=int, 
        nargs='*',  # Makes this argument optional
        default=[15,5]  # Default value
    )
    # header & footer
    parser.add_argument(
        "-top", 
        type=int, 
        nargs='?',  # Makes this argument optional
        default=0  # Default value
    )
    parser.add_argument(
        "-buttom", 
        type=int, 
        nargs='?',  # Makes this argument optional
        default=0  # Default value
    )

    args = parser.parse_args()
    
    file_dir  = os.path.dirname(args.file_path)
    output_dir= os.path.join(file_dir, "output")
    if os.path.exists(args.file_path):
        print(f"The file '{args.file_path}' exists, Analyzing file ....")
        return args.file_path, output_dir, args.type,args.kernel,args.top,args.buttom
    else:
        print(f"The file '{args.file_path}' does not exist, program terminated")
        sys.exit(0)



