# pacman -S tesseract
# pacman -S tesseract-data-eng
# pip install Pillow
# pip install pytesseract

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import glob
import json
import re

def img2txt(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

images = glob.glob("./images/*.png")
images.sort()

dump_data = []

for i, image in enumerate(images):
    text = img2txt(image)
    print(text)
    print("===========")
    question = {
        "text": "",
        "options": [],
        "result": 0
    }

    # Search text
    regex_text = r'(?s)\A\d+\.\s+(.+?)(?=\n\()'
    match = re.search(regex_text, text)
    print(match)
    if match:
        question["text"] = match.group(1)
    else:
        question["text"] = None

    # Search alternatives
    optionsKey = ["A", "B", "C", "D"]
    for opt in optionsKey:
        result = ''
        regex = r'^'+ opt + r'\.(.+)$|^\(' + opt + r'\)(.+)$'
        search = re.search(regex, text, re.MULTILINE)
        if search:
            result = search.group(1) or search.group(2)
        question["options"].append(result)

    dump_data.append(question)
print(dump_data)
with open('questions.json', 'w') as outfile:
    json.dump(dump_data, outfile, indent=4)
