# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 10:08:14 2018

@author: chuang
"""

### tf-idf customized implementation 

from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import pandas as pd
import scipy.sparse as sp
import numpy as np

#%%
###
def dummy_func(doc):
    return doc


def display_features(features,feature_names):
    df = pd.DataFrame(data=features,columns=feature_names)
    print(df.head(10))
    
def bow_extractor(corpus,ngram_range=(1,1)):
    
    """
    corpus: should be a document list, when all documents has been tokenized
    """
    bow_transformer = CountVectorizer(
                        analyzer='word',   ## this can actually be any kind of function to preprocess your text
                        tokenizer=dummy_func,
                        preprocessor=dummy_func,
                        token_pattern=None,
                        min_df=1,  ## frequency is at least 1 in overall document
                        ngram_range=ngram_range) ## if it is (1,3) it will consider bi and tri gram as well
    
    features = bow_transformer.fit_transform(corpus) ## does the bow process
    
    return bow_transformer,features

## comput document frequency 
def build_df(bow_features):
    df = np.diff(sp.csc_matrix(bow_features,copy=True).indptr)
    #df += 1  ## to smoothen idf latter to avoid 0s 
    return df 

def build_df_dum(bow_features,vocabs=None):
    """
    use basic pandas rather then sparse matrix
    """
    df = pd.DataFrame(bow_features,columns=vocabs)
    df[df != 0] = 1
    df = df.agg('sum') + 1  ## to smoothen 
    return df.values

## compute inverse document frequency 

def build_idf(corpus,df):
    total_docs = len(corpus)
    #idf = 1 + np.log(total_docs/df)   ## be very careful with this formula, especially when your sample is small
    idf = np.log2(total_docs/df)     
    return idf 

## compute idf diagonal matrix 
def build_idf_diag_matrix(idf):
    n = len(idf)
    idf_diag = sp.spdiags(idf,diags=0,m=n,n=n)
    idf_diag = idf_diag.todense()
    return idf_diag

def calculate_tfidf(corpus,norm=False):
    bow_transformer,features = bow_extractor(corpus)
    shape = features.shape
    tf = features.todense()
    df = build_df(features)
    idf = build_idf(corpus,df)
    idf_matrix = np.repeat(idf,shape[0],axis=0).reshape(shape[1],shape[0]).T
    tfidf = np.multiply(tf,idf_matrix)
    
    if norm:
        norms = np.linalg.norm(tfidf,axis=1) ## get norm along the second axis
        tfidf = tfidf/norms[:,None] 
    
    return tfidf
