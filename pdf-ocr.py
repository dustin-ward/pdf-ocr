from PIL import Image
import pytesseract
import sys
import os
import shutil
from pdf2image import convert_from_path

# Cmd line args
file = sys.argv[1]
output_file = sys.argv[2]
keywords = sys.argv[3:]

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

# Gather keywords
print("Gathering Keywords...")
instances = {}
for k in keywords:
    instances[k] = []

# For each page...
f = open(output_file, "a")
for i in range(0, len(pages)):
    print("Checking page", i+1, "for...")

    # Convert JPG to txt
    text = str(((pytesseract.image_to_string(Image.open("images/page" + str(i) + ".jpg")))))
    text = text.replace('-\n', '') 

    # For each keyword...
    for k in keywords:
        print(k)
        idx = 0
        while True:
            idx = text.find(k, idx)
            if idx == -1:
                break
            
            # Add page # and position to dictionary
            instances[k].append((i+1, round(idx/len(text)*100, 2)))

            idx += 1

    print("Writing Text To File...")
    f.write(text)

# Print results
for k, l in instances.items():
    print("INSTANCES OF KEYWORD", k, ":")
    if len(l):
        for i in l:
            print("PAGE:", i[0], i[1], "%")
    else:
        print("None")

f.close()

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