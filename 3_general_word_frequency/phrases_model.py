# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:51:09 2018

@author: chuang
"""
import pickle 
import os 
#import re
#import csv
#from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Phrases
from gensim.models.phrases import Phraser
#from functools import partial
#from multiprocessing import Pool

#%%

########################
### bigram and trigram##
########################
data_path = os.path.join('data','tokenized_sentances.p')
bigram_model_path = os.path.join('data','bigram_model')
trigram_model_path = os.path.join('data','trigram_model')

#%%
## first train a bigram and trigram model on a large dataset and save them
sentances = pickle.load(open(data_path,'rb'))
#%%
print('Training bigram model .........\n')
bi_phrases = Phrases(sentances, min_count=5, threshold=15)
bi_phrases.save(bigram_model_path)
bigram_transformer = Phraser(bi_phrases)
bigram_transformer.save(os.path.join('data','bigram_transformer'))
sentances = list(bigram_transformer[sentances]) 
tri_phrases = Phrases(sentances, min_count=5, threshold=10)
bi_phrases.save(trigram_model_path)
trigram_transformer = Phraser(tri_phrases)
trigram_transformer.save(os.path.join('data','trigram_transformer'))
#sentances = list(trigram_transformer[sentances])

## if you want to check pharses list
pharses_list = list(tri_phrases.vocab.keys())

#print('Dump to Pickle')
#pickle.dump(sentances,open(out_path, "wb"))


print('finish')