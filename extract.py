
# import local helper function in ./tools/helper
import tools.helper.parser as parser
import tools.helper.analyze as analyze

file_path,output_path,paper_type,dilate_kernel,top,buttom = parser.argumentParser()


if (file_path[-3:]=="pdf"):
    analyze.analyzePdf(file_path,output_path,paper_type,tuple(dilate_kernel),top,buttom)
else:
    analyze.analyzePicture(file_path,output_path,paper_type,tuple(dilate_kernel),top,buttom)
    