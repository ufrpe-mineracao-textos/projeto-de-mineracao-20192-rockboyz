from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from google.cloud import vision
import re

import numpy as np
from gensim.models.word2vec import Word2Vec
import gensim.downloader as api
from gensim.models import KeyedVectors


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
        "fullText": text,
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
        if opt != "D":
            regex = r'^'+ opt + r'\.(.+)$|^\(' + opt + r'\)([^\(]+)\('
        else:
            regex = r'^'+ opt + r'\.(.+)$|^\(' + opt + r'\)([^\(]+)$'
        search = re.search(regex, text, re.MULTILINE)
        if search:
            result = search.group(1) or search.group(2)
        question["options"].append(result)

    return question

def best_probability(question):
    pretrained = KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300-SLIM.bin.gz', binary=True)
    letters = ['A', 'B', 'C', 'D']
    best_value = 999
    best_alt = ""    
    pairs = [
        (question['text'], question['options'][0]),
        (question['text'], question['options'][1]),
        (question['text'], question['options'][2]),
        (question['text'], question['options'][3]),
    ]
    for k, v in enumerate(pairs):
        w1, w2 = v
        similarity = pretrained.wmdistance(w1, w2)
        if similarity < best_value:
            best_value = similarity
            best_alt = k
    return letters[best_alt]

def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        text = img2txt_cloud(request.FILES['image'].file.getvalue())
        
        question = parse_text(text)
        question['answer'] = best_probability(question)

        print(question)

        ##
        return render(request, 'questions/results.html', {'question': question})

    # if a GET (or any other method) we'll create a blank form
    else:
        context = {'a': 1}
        return render(request, 'questions/index.html', context)

