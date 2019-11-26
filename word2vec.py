import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models.word2vec import Word2Vec
import gensim.downloader as api
from gensim.models import KeyedVectors

df = pd.read_csv('questions.csv')
df1 = df.astype(object).replace(np.nan, "")
pretrained = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin', binary=True)
letters = ['A', 'B', 'C', 'D', 'E']
acertos = 0
total = len(df1)
for index, row in df1.iterrows():
    best_value = 999
    best_alt = ""    
    pairs = [
        (row['Question'], row['A']),
        (row['Question'], row['B']),
        (row['Question'], row['C']),
        (row['Question'], row['D']),
        (row['Question'], row['E']),
    ]
    for k, v in enumerate(pairs):
        w1, w2 = v
        similarity = pretrained.wmdistance(w1, w2)
        if similarity < best_value:
            best_value = similarity
            best_alt = k
        #print(f"{w1} {w2} {pretrained.wmdistance(w1, w2)}")
    if letters[best_alt] == row['Answer']:
        acertos += 1
    #print(f"Suggestion: {letters[best_alt]} Answer: {row['Answer']}")
print(f"Precisao: {acertos/total} Acertos: {acertos}") 
