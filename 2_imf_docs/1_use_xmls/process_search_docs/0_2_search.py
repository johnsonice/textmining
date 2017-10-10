# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:58:01 2017

@author: chuang
"""
#####################
## search keywords ##
#####################
import os 
os.chdir('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls/process_search_docs')
from util import  find_exact_keywords, read_keywords,construct_rex#, read_meta, get_ids
import pickle 
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
#%%
## improt all staff documents 
doc_dict = pickle.load(open('data/xlm_docs.p', "rb")) 

#%%
key_file = 'search_keywords.csv'
keywords = read_keywords(key_file)
keywords = [k[0].replace('_',' ') for k in keywords]
#keywords = ['risk']
print('Keywords: ', keywords)

total_doc_num = len(doc_dict.items())
df = pd.DataFrame()
rex = construct_rex(keywords)

for idx,(ite) in enumerate(doc_dict.items()):
    #if idx > 500: break
    key,doc = ite
    val = doc.paras   ## read all paragraphs 
    if len(val)==0:
        continue
    for idxp,content in enumerate(val):
        results = find_exact_keywords(content.lower(),keywords,rex)
        if len(results) == 0:
            continue
        results['context'] = content 
        results['doc_id'] = str(key)
        results['para_id'] = str(key) + '_' + str(idxp)
        results['para_word_count'] = len(content.split())
        df = df.append(results, ignore_index=True)
    
    if idx%100 == 0 :
        print('{}/{}'.format(idx,total_doc_num))

#meta = ['doc_id','para_id','context']
#meta.extend(keywords)
#meta = [c for c in meta if c in df.columns ]
#df = df[meta]
#print(df.head())
df.to_csv('data/xml_results.csv',encoding='utf-8')

print('finished')

#%%

stopw = stopwords.words('english')
word_count = []
lemmatizer = WordNetLemmatizer()

## get word count for document 
for idx,(ite) in enumerate(doc_dict.items()):
    #if idx > 500: break
    key,doc = ite
    if len(doc.paras)==0:
        continue
    count = 0 
    for content in doc.paras:
        tokens = word_tokenize(content)
        #tokens = [lemmatizer.lemmatize(t) for t in tokens]
        tokens = [t for t in tokens if t not in stopw]
        count += len(tokens)
    
    if idx%100 == 0 :
        print('{}/{}'.format(idx,len(doc_dict)))
        
    word_count.append((key,count))

    
df_word =pd.DataFrame(word_count,columns=['id','count'])
df_word.to_csv('data/xml_word_count.csv',encoding='utf-8')
print('finished')    
        
        
        
        