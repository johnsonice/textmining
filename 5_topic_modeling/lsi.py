#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 21:42:14 2018

@author: chengyu
"""

### topic modeling 1 latent semantic indexing 

from gensim import corpora, models 
from scripts.normalization import normalize_corpus
import numpy as np
from docx import Document
import sys
#%%
def read_txt(file_path):
    with open(file_path,'r') as f:
        corpus = f.readlines()
    
    corpus = [c.strip('\n') for c in corpus]
    corpus = [c for c in corpus if len(c)> 10]
    return corpus

#%%

##read data
file_path = 'input/doc_1.txt'
corpus = read_txt(file_path)
## preprocess text
norm_tokenized_corpus = normalize_corpus(corpus,tokenize=True)

#%%
# build dictionary
dictionary = corpora.Dictionary(norm_tokenized_corpus)
# convert document into bow
corpus_bow = [dictionary.doc2bow(text) for text in norm_tokenized_corpus]
## comput tfidf feature vectors
tfidf = models.TfidfModel(corpus_bow)
corpus_tfidf = tfidf[corpus_bow]

#%%

## topic modeling 

total_topics = 7
lsi = models.LsiModel(corpus_tfidf,
                      id2word=dictionary,
                      num_topics= total_topics)

#%%

for index, topic in lsi.print_topics(total_topics):
    print('Topic #{}'.format(index+1))
    print(topic)
    print()
          



