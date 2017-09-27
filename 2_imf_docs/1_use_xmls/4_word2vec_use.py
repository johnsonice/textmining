# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 09:05:47 2017

@author: chuang
"""
#import gensim
import os 
import csv
from gensim.models.word2vec import Word2Vec
#%%
## some helper functions 
def read_keywords(file):
    """
    file: csv file with keyword list
    """
    with open(file,'r') as f:
        reader = csv.reader(f)
        mylist = list(reader)
    
    key_list = [l[0].lower().replace(' ','_') for l in mylist]
    key_list = list(set(key_list))
    return key_list

def get_sim_words(key,topn,w2v):
    """
    key: keyword you want to find similar work for 
    topn: how many word you want to get 
    w2v: gensim w2v model
    """
    w_list = [key]
    try:
        words = model.most_similar(key,topn=topn)
        words = [w[0] for w in words]
        w_list.extend(words)
    except:
        return w_list
    
    return w_list

#%%
## load models 

data_path = os.path.join('trained','imf_132.w2v')
imf_w2v = Word2Vec.load(data_path)
model = imf_w2v.wv
vocabs = model.vocab.keys()

#%%

file = 'keywords.csv'
out_file = 'sim_words.csv'
save = True

key_list = read_keywords(file)
results = [get_sim_words(w,40,model) for w in key_list]

if save:
    with open(out_file,'w',newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)
else:   
    with open(out_file,'r') as f:
        reader = csv.reader(f)
        key_list = list(reader)
        
#print(key_list)