# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 09:05:47 2017

@author: chuang
"""
import gensim
import os 
from gensim.models.word2vec import Word2Vec


#%%
data_path = os.path.join('trained','imf.w2v')
imf_w2v = Word2Vec.load(data_path)
model = imf_w2v.wv
vocabs = model.vocab.keys()

#%%
