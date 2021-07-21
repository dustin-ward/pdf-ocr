from PIL import Image
import pytesseract
import sys
import os
from pdf2image import convert_from_path

file = "document.pdf"
pages = convert_from_path(file, 500)

for i, page in enumerate(pages):
    page.save("images/page" + str(i) + ".jpg", 'JPEG')

output_file = "document_text.txt"
f = open(output_file, "a")

for i in range(0, len(pages)):
    text = str(((pytesseract.image_to_string(Image.open("images/page" + str(i) + ".jpg")))))
    text = text.replace('-\n', '') 
    f.write(text)

f.close()