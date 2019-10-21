# pacman -S tesseract
# pacman -S tesseract-data-eng
# pip install Pillow
# pip install pytesseract
# pip install google-cloud-vision
# export GOOGLE_CLOUD_CRENDENTIALS=[path]

try:
    from PIL import Image
except ImportError:
    import Image
    
import pytesseract
import glob
import json
import re
import base64
# from google.cloud import vision

def img2txt_tesseract(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


# def img2txt_cloud(file):
#     """Detects text in the file located in Google Cloud Storage or on the Web.
#     """
#     client = vision.ImageAnnotatorClient()

#     with open(file, 'rb') as image_file:
#         content = image_file.read()

#     image = vision.types.Image(content=content)

#     response = client.text_detection(image=image)
#     texts = response.text_annotations

#     return response.full_text_annotation.text

images = glob.glob("./images/*.png")
images.sort()

dump_data = []

for i, image in enumerate(images):
    text = img2txt_tesseract(image)
    print(text)
    print("===========")
    question = {
        "text": "",
        "options": [],
        "result": 0
    }

    # Search text
    regex_text = r'(?s)\A\d+\.\s+(.+?)(?=\n\()|\A(.+?)(?=\n\()'
    match = re.search(regex_text, text)
    
    if match:
        question["text"] = match.group(1) or match.group(2)
        
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

with open('questions.json', 'w') as outfile:
    json.dump(dump_data, outfile, indent=4)
