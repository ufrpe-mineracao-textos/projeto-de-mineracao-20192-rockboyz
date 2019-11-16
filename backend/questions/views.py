from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from google.cloud import vision
import re

def img2txt_cloud(content):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    return response.full_text_annotation.text

def parse_text(text):
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

    return question

def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        text = img2txt_cloud(request.FILES['image'].file.getvalue())
        
        print(parse_text(text))
        ##
        return render(request, 'questions/index.html', {})

    # if a GET (or any other method) we'll create a blank form
    else:
        context = {'a': 1}
        return render(request, 'questions/index.html', context)

