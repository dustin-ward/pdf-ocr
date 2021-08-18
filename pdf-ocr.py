from PIL import Image
import pytesseract
import sys
import os
import shutil
from pdf2image import convert_from_path

# Cmd line args
file = sys.argv[1]
keywords = sys.argv[2:]

# Check for and create img directory
imgDirectory = os.getcwd() + "/images"
try:
    os.stat(imgDirectory)
except:
    os.mkdir(imgDirectory)   

# Convert PDF pages to JPG images
print("Converting PDF pages to JPG images...")
pages = convert_from_path(file, 500)
for i, page in enumerate(pages):
    page.save("images/page" + str(i) + ".jpg", 'JPEG')

PageScore = {}

# For each page...
for i in range(0, len(pages)):
    print("Scanning page", i+1)

    # Convert JPG to txt
    text = str(((pytesseract.image_to_string(Image.open("images/page" + str(i) + ".jpg")))))
    text = text.replace('-\n', '') 

    # For each keyword...
    for k in keywords:
        idx = 0
        while True:
            idx = text.find(k, idx)
            if idx == -1:
                break
            
            # Add point to page
            if i+1 not in PageScore:
                PageScore[i+1] = 1
            else:
                PageScore[i+1] += 1

            idx += 1

# Print results
for i, s in sorted(PageScore.items(), key=lambda item: item[1]):
    print("Page", i, ":", s, "keyword matches")

# Clean img directory
print("Cleaning Images Directory...")
for filename in os.listdir(imgDirectory):
    file_path = os.path.join(imgDirectory, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

print("Finished!")