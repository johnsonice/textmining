# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:07:11 2017

@author: chuang
"""

import shutil 
import os 
import pickle
#import pandas as pd
os.chdir('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls/process_search_docs')
from util import document, find_exact_keywords, get_ids,read_keywords, read_meta

#%%

def copy_files(data_path,dest_path):
    shutil.copytree(data_path,dest_path)
    print('finished copying')
    
    files = os.listdir(dest_path)
    #files = [os.path.join(dest_path,f) for f in files if os.path.getsize(os.path.join(dest_path,f)) < 3000] ## files < 5k
    files = [os.path.join(dest_path,f) for f in files if '_' not in f]
    _ = [os.remove(f) for f in files]
    print('finish filtering')  

#%%
## copy and clear useless data 

data_path = os.path.join('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls','xml','002')
dest_path = os.path.join('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls','process_search_docs','data','002')
copy = False
dump = True
ids, meta = read_meta('staff_reports_meta.csv')

#%%
## copy xml to data folder 
if copy:
    copy_files(data_path,dest_path)
#%%
## keep only staff reports 
xmls = os.listdir(dest_path)
xmls = [f for f in xmls if get_ids(f)[1] in ids]

#%%
## dump xmls to pickle 

if dump:
    doc_list = list()
    total_length = len(xmls)
    print('converting {} xmls into paragraph lists ......'.format(total_length))
    for idx,file_name in enumerate(xmls):
        xml_path = os.path.join(dest_path,file_name)
        try:
            series_id,file_id = get_ids(file_name)
        except:
            continue
        doc = document(series_id,file_id,xml_path)
        #docs_dict[doc.file_id] = doc
        doc_list.append(doc)
        if (idx+1)%100 == 0:
            print('{} / {} '.format(idx+1,total_length))
    
    doc_dict = {}
    for doc in doc_list:
        try:
            if doc.file_id in doc_dict.keys():
                doc_dict[doc.file_id].paras.extend(doc.paras)
            else:
                doc_dict[doc.file_id] = doc
        except:
            print(doc.file_id)
        
    process_text = os.path.join('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls','process_search_docs','data','xlm_docs.p')
    pickle.dump(doc_dict,open(process_text, "wb"))
    print('Finishing dumping to pickle')

