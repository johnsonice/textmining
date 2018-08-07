# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 10:36:58 2018

@author: chuang
"""

## calculate tfidf for IMFC 

import pickle 
from tf_idf_model import bow_extractor,display_features,build_df,build_idf,build_idf_diag_matrix
from tf_idf_model import calculate_tfidf
import scipy.sparse as sp
import numpy as np
import pandas as pd
import copy
from math import log
#%%
data_path = 'data/processed_docs.p'
names,docs = pickle.load(open( data_path, "rb" ))
#%%

bow_transformer,features = bow_extractor(docs)
shape = features.shape
vocabs = bow_transformer.get_feature_names()
tf = features.todense()

#%%
## calculate idf weights with out target document that is currently being evaluated
idf_list = list()
for i in range(shape[0]):
    tf_i = copy.deepcopy(tf)
    tf_i = np.delete(tf_i,i,axis=0)
    df = build_df(tf_i)
    idf = build_idf(docs,df,smooth=0.1)
    idf_list.append(idf)
    
idf_mat = np.stack(idf_list,axis=0)  ## stack all idf into matrix
tf_idf = np.multiply(tf,idf_mat)     ## lement wise multiplication
norms = np.linalg.norm(tf_idf,axis=1) ## get norm along the second axis
tf_idf_norm = tf_idf/norms[:,None]            ## normalized 

#%%
#normal tfidf
sd_tfidf = calculate_tfidf(docs,smooth=0.1)

#%%
# export 
df_tfidf = pd.DataFrame(tf_idf,columns=vocabs,index=names).T
df_tfidf_norm = pd.DataFrame(tf_idf_norm,columns=vocabs,index=names).T
sd_tfidf = pd.DataFrame(sd_tfidf,columns=vocabs,index=names).T
#%%
writer = pd.ExcelWriter('results/results.xlsx', engine='xlsxwriter')
df_tfidf.to_excel(writer,sheet_name='tfidf_rolling')
df_tfidf_norm.to_excel(writer,sheet_name='tfidf_rolling_norm')
sd_tfidf.to_excel(writer,sheet_name='tfidf')
writer.save()

### old way
#def old_way():
#    tf = pd.DataFrame(features.toarray(),columns=vocabs)
#    N = len(tf) + 1
#    df = copy.deepcopy(tf)
#    df[df != 0] = 1
#    df = df.agg('sum') + 1         ## calculate document frequency 
#    df.replace(0,1,inplace=True)
#    idf = df.apply(lambda x:1+log(N/x))
#    ## tfidf 
#    tf_idf = tf*idf
#    
#    return tf_idf

