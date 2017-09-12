# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:37:47 2017

@author: chuang
"""

import pickle 
import os 
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Phrases
from gensim.models.phrases import Phraser
#from functools import partial
from multiprocessing import Pool

#%%     
def clean_up_setances(docs):
    """
    passin a list of documents 
    """
    replace_num = re.compile(r'\(.*?\)')
    docs = [replace_num.sub('',p) for doc in docs for p in doc]
    docs = [doc.lower() for doc in docs]
    return docs 

def tokenize(para):
    """
    para: one paragraph.
    this function will tokenize a paragraph by sentances and by token
    """
    sentances = [word_tokenize(s) for s in sent_tokenize(para)]    
    return sentances 

def bigram_transform(s):
    sentance = bigram_transformer[s]
    return sentance 


#%%
if __name__ =='__main__':
    
    test = False
    pl_folder = 'pickle'
    out_path = 'total_results.p'
    files =  os.listdir(pl_folder)
    paras = list()
    
    ## read all into one list 
    for f in files:
        print(f)
        data_path = os.path.join(pl_folder,f)
        docs = pickle.load(open(data_path, "rb"))
        paras.extend(clean_up_setances(docs))

    ## multi process it    
    ## see if we want to run a test first
    if test == True: 
        paras = paras[:100]
        num_cores = 2
    else:
        num_cores = os.cpu_count()
    ## initial workers 
    print('numer of cores:', num_cores)
    p = Pool(num_cores)
    
    #############################
    ## multi process tokenizing##
    #############################
    print('Multi processing tokenizing')
    print('............\n')
    process_mp = p.map(tokenize,paras)
    p.close()
    p.join()
    
    sentances = [s for p in process_mp for s in p]
    pickle.dump(sentances,open('tokenized_sentances.p', "wb"))
    
    ########################
    ### bigram and trigram##
    ########################
    print('Transform sentances to trigrams .........\n')
    bi_phrases = Phrases(sentances, min_count=5, threshold=30)
    bigram_transformer = Phraser(bi_phrases)
    sentances = list(bigram_transformer[sentances]) 

    tri_phrases = Phrases(sentances, min_count=5, threshold=30)
    trigram_transformer = Phraser(tri_phrases)
    sentances = list(trigram_transformer[sentances])
    
    ## if you want to check pharses list
    pharses_list = list(tri_phrases.vocab.keys())
    
    print('Dump to Pickle')
    pickle.dump(sentances,open(out_path, "wb"))


    print('finish')



