# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 08:20:45 2017

@author: chuang
"""


import gensim
from gensim.models.word2vec import Word2Vec
import pickle
import os

#%%
data = 'total_results.p'
total_results = pickle.load(open(data, "rb"))
#total_results = total_results[:10000]
#%%
### initialize model and build vocabulary 
n_dim = 300
window = 5 
downsampling = 0.001
seed = 1 
num_workers = os.cpu_count()-1    ## not sure if this is a good idea
min_count = 40 
imf_w2v = Word2Vec(
    sg=1,
    seed=seed,
    workers=num_workers,
    size=n_dim,
    min_count=min_count,
    window= window,
    sample=downsampling
)
## build the vocabulary
imf_w2v.build_vocab(total_results)

#%%
## train w2v model 
corpus_count = imf_w2v.corpus_count
iteration = 20
if gensim.__version__[0] =='1':
    imf_w2v.train(total_results)
else:
    imf_w2v.train(total_results,total_examples=corpus_count,epochs = iteration)

## save trained word2 to vect model 
if not os.path.exists("trained"):
    os.makedirs("trained")

imf_w2v.save(os.path.join('trained','imf.w2v'))
