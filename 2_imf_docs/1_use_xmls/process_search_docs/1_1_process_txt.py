# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 17:36:10 2017

@author: chuang
"""

## process PDF txt file from Marc 

import os 
import pickle
#import pandas as pd
os.chdir('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls/process_search_docs')
from util import text_document, read_ids #, find_exact_keywords, get_ids,read_keywords, read_meta

#%%
data_path = 'd:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls/process_search_docs/data/pdfs_text'
txt_ids_path = 'txt_ids.csv'
txts = os.listdir(data_path)

txt_ids = read_ids(txt_ids_path)
txt_ids = [i[0] for i in txt_ids]
## deleted those ones that are too short, usually corrections 
txts = [t for t in txts if t.split('.')[0] in txt_ids]

#%%

dump = True
if dump:
    doc_list = list()
    total_length = len(txts)
    print('converting {} text into paragraph lists ......'.format(total_length))
    for idx,file_name in enumerate(txts):
        txt_path = os.path.join(data_path,file_name)
        try:
            file_id = file_name.split('.')[0]
        except:
            continue
        try:
            doc = text_document(file_id,txt_path)
            #docs_dict[doc.file_id] = doc
            doc_list.append(doc)
        except:
            print(file_name)
            
        if (idx+1)%50 == 0:
            print('{} / {} '.format(idx+1,total_length))
        
    doc_dict = {}
    for doc in doc_list:
        doc_dict[doc.file_id] = doc
        
    process_text = os.path.join('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls','process_search_docs','data','txt_docs.p')
    pickle.dump(doc_dict,open(process_text, "wb"))
    print('Finishing dumping to pickle')
    
#%%
#for x in doc_list:
#    
#    print(x.file_id,len(x.paras))