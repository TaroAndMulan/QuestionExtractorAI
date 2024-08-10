import easyocr
reader = easyocr.Reader(['en'])
result = reader.readtext('./tools/testing/1/question_4.png',detail = 0)
print(result)