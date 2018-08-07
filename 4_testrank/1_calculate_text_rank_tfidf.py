# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 10:00:27 2018

@author: chuang
"""

import pickle
from docx import Document
import os 
from gensim.summarization import keywords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from tf_idf_model import bow_extractor,display_features,build_df,build_idf,build_idf_diag_matrix
from tf_idf_model import calculate_tfidf
import operator
import numpy as np
import copy
from statistics import mean
import pandas as pd

#%%

def get_text_rank(text):
    """
        input is a string document 
        out a list of tuples with words and its rank
    """
    pos_filters = ('NN','NNS','NNP','NNPS','JJ','JJR','JJS')
    ranks = keywords(text,split=True,ratio=1,scores=True,
                 lemmatize=False,
                 pos_filter=pos_filters)
    
    r_list = [(v,d[0]) for v,d in ranks]
    
    return r_list

def calculate_idf_tfidf(docs):
    """
        input is clearned and tokenized document list
    """
    bow_transformer,features = bow_extractor(docs)
    shape = features.shape
    vocabs = bow_transformer.get_feature_names()
    tf = features.todense()
    df = build_df(tf)
    idf = build_idf(docs,df)
    idf_matrix = np.repeat(idf,shape[0],axis=0).reshape(shape[1],shape[0]).T
    tfidf = np.multiply(tf,idf_matrix)
    tfidf = np.asarray(tfidf)
    
    return vocabs,idf,tfidf

def build_tfidf_vocab_map(vocabs,doc_index,tfidf):
    
    """
        input: vacabs dictonray, doc_index in the document name list 
                and tfidf matrix 
    """
    tfidf_doc_i = copy.deepcopy(tfidf[doc_index,:])
    voc2tfidf = {v:i for v,i in zip(vocabs,tfidf_doc_i)}
    
    return voc2tfidf

def build_idf_vocab_map(vocabs,idf):
    
    """
        input: vacabs dictonray,  idf list of idf values
    """
    voc2idf = {v:i for v,i in zip(vocabs,idf)}    
    return voc2idf

def build_pd_df(text_r,voc2idf,voc2tfidf):
    data = []
    for k,v in text_r:
        k = k.split()
        i_idf = [voc2idf.get(i,0.0) for i in k]
        i_idf = mean(i_idf)
        i_tfidf = [voc2tfidf.get(i,0.0) for i in k]
        i_tfidf = mean(i_tfidf)
        data.append((' '.join(k),v,i_idf,i_tfidf))
    
    _df = pd.DataFrame(data, columns=['vocab','text_rank','idf','tfidf'])
    _df['text_rank_idf'] = _df['text_rank']*_df['idf']
    _df['text_rank_tfidf'] = _df['text_rank']*_df['tfidf']
    result = _df.sort_values('text_rank_tfidf',ascending=False)
    return result

#%%

## calculate text rank for each document 
## please the vocabulary for each document will be different because of the automatic key phrase extraction

data_path = 'data/processed_docs.p'
names,docs_list = pickle.load(open( data_path, "rb" ))
docs_list = [' '.join([' '.join(p) for p in doc]) for doc in docs_list]
document_text_rank_list = [get_text_rank(doc) for doc in docs_list]

#%%
## calculate tfidf and idf 
## first load a different dataset, it is pre cleaned 

data_path = '../3_general_word_frequency/data/processed_docs.p'
names,docs = pickle.load(open( data_path, "rb" ))
vocabs,idf,tfidf = calculate_idf_tfidf(docs)

#%%
df_list = list()
voc2idf = build_idf_vocab_map(vocabs,idf)
for idx in range(len(docs)):
    voc2tfidf = build_tfidf_vocab_map(vocabs,idx,tfidf)
    text_df = build_pd_df(document_text_rank_list[idx],voc2idf,voc2tfidf)
    df_list.append(text_df)
    

#%%
index = -1 
test_df = df_list[index]
test_df.head(10)

#%%
column_names = ['text_rank','text_rank_idf','text_rank_tfidf']

writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')
for column_name in column_names:
    result = copy.deepcopy(df_list[0][['vocab',column_name]])
    result.rename(columns={column_name:names[0] +'_'+ column_name}, inplace=True)
    for idx,name in enumerate(names):
        merge_df = copy.deepcopy(df_list[idx][['vocab',column_name]])
        merge_df.rename(columns={column_name:names[idx] +'_'+column_name}, inplace=True)
        result = pd.merge(result,merge_df,on='vocab',how='outer')
    result.to_excel(writer,sheet_name=column_name)
    
writer.save()


    
    