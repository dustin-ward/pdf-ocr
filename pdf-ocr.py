from PIL import Image
import pytesseract
import sys
import os
from pdf2image import convert_from_path

file = sys.argv[1]
keyword = sys.argv[3]
pages = convert_from_path(file, 500)

for i, page in enumerate(pages):
    page.save("images/page" + str(i) + ".jpg", 'JPEG')

output_file = sys.argv[2]
f = open(output_file, "a")

print("Instances of key:", keyword)
for i in range(0, len(pages)):
    text = str(((pytesseract.image_to_string(Image.open("images/page" + str(i) + ".jpg")))))
    text = text.replace('-\n', '') 

    idx = 0
    while True:
        idx = text.find(keyword, idx)
        if idx == -1:
            break
        
        print("PAGE:", i+1, str(round(idx/len(text)*100, 2)), "%")

        idx += 1

    f.write(text)

f.close()