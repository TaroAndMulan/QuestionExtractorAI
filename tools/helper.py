import argparse
import os
import sys
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