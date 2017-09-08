# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:37:47 2017

@author: chuang
"""

import pickle 
import os 
import re

#%%     
def clean_up_setances(docs):
    """
    passin a list of documents 
    """
    replace_num = re.compile(r'\(.*?\d+.*?\)')
    docs = [replace_num.sub('',p) for doc in docs for p in doc]
    return docs 

#%%
if __name__ =='__main__':
    pl_folder = 'pickle'
    out_path = 'total_results.p'
    files =  os.listdir(pl_folder)
    paras = list()
    
    for f in files:
        print(f)
        data_path = os.path.join(pl_folder,f)
        docs = pickle.load(open(data_path, "rb"))
        paras.extend(clean_up_setances(docs))
        
    pickle.dump(paras,open(out_path, "wb"))


