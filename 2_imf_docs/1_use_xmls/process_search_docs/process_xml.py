# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:07:11 2017

@author: chuang
"""

### process search documents 

## copy files > than 5 k 
import shutil 
import os 
#import glob
from bs4 import BeautifulSoup
import csv
import pickle
import re
from collections import Counter
import pandas as pd


#%%

def copy_files(data_path,dest_path):
    shutil.copytree(data_path,dest_path)
    print('finished copying')
    
    files = os.listdir(dest_path)
    #files = [os.path.join(dest_path,f) for f in files if os.path.getsize(os.path.join(dest_path,f)) < 3000] ## files < 5k
    files = [os.path.join(dest_path,f) for f in files if '_' not in f]
    _ = [os.remove(f) for f in files]
    print('finish filtering')
    
def find_exact_keywords(content,keyWords):
    content = content.replace('\n', '').replace('\r', '')#.replace('.',' .')
    r_keyWords = [r'\b' + re.escape(k) + r'\b'for k in keyWords]             # tronsform keyWords list to a patten list
    rex = re.compile('|'.join(r_keyWords),flags=re.I)                        # use or to join all of them, ignore casing
    #match = [(m.start(),m.group()) for m in rex.finditer(content)]          # get the position and the word
    match = Counter([m.group() for m in rex.finditer(content)])
    return match

def get_ids(xml):
    """
    input xml full name, return series id and file id 
    """
    series_id,xml_name = xml.split('-')
    file_id,_ = xml_name.split('_') 
    return series_id,file_id

def read_keywords(file):
    """
    file: csv file with keyword list
    rep: a class object
    """
    with open(file,'r') as f:
        reader = csv.reader(f)
        mylist = list(reader)
    
    return mylist
    
#%%
class document(object):
    def __init__(self,series_id,file_id,xml_path):
        #print('initiate doc object')
        self.file_id = file_id
        self.series_id = series_id
        self.xml_path = xml_path
        self.paras = self.load_xml()
    
    def load_xml(self):
        return  self.extract_xml_paras()
    
    def clean_fig_table(self,soup):
        for tag in soup.body.find_all(['fig','table-wrap']):
            tag.decompose()
        ## group list points together in one paragraph
        for li in soup.body.find_all('list'):
            s = [t.get_text() for t in li.find_all('list-item')]
            s = ' '.join(s)
            tag = soup.new_tag('p')
            tag.string = s    
            li.replaceWith(tag)
        
        return soup 
    
    def extract_xml_paras(self):
        with open(self.xml_path,'r',encoding='utf8') as f:
            soup = BeautifulSoup(f, 'xml')
        try:
            soup = self.clean_fig_table(soup)
            p_list = soup.body.find_all('p')
            ## check see if documents are structure in this way 
            if len(p_list) ==0 : 
                print('no paragraph found: {}'.format(self.file_id))
                return p_list 
        except:
            print('file corropted: {}'.format(self.file_id))
            return []
        
        p_list =  [ele.get_text().replace('\n',' ') for ele in p_list]
        
        return p_list


#%%
## copy and clear useless data 
os.chdir('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls/process_search_docs')
data_path = os.path.join('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls','xml','002')
dest_path = os.path.join('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls','process_search_docs','data','002')
copy = False

if copy:
    copy_files(data_path,dest_path)
#%%
xmls = os.listdir(dest_path)
doc_list = list()
total_length = len(xmls) + 1 
print('converting {} xmls into paragraph lists ......'.format(total_length))
for idx,file_name in enumerate(xmls):
    xml_path = os.path.join(dest_path,file_name)
    try:
        series_id,file_id = get_ids(file_name)
    except:
        continue
    doc = document(series_id,file_id,xml_path)
    doc_list.append(doc)
    if (idx+1)%100 == 0:
        print('{} / {} '.format(idx+1,total_length))
        
process_text = os.path.join('d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls','process_search_docs','text.p')
pickle.dump(doc_list,open(process_text, "wb"))
print('done')

#%%
docs = pickle.load(open('text.p', "rb")) 
doc_dict = {}

for doc in docs:
    try:
        if doc.file_id in doc_dict.keys():
            doc_dict[doc.file_id].extend(doc.paras)
        else:
            doc_dict[doc.file_id] = doc.paras
    except:
        print(doc.file_id)

#%%
key_file = '../keywords.csv'
keywords = read_keywords(key_file)
keywords = [k[0] for k in keywords]
print('Keywords: ', keywords)

total_doc_num = len(doc_dict.items())
df = pd.DataFrame()
for idx,(ite) in enumerate(doc_dict.items()):
    #if idx > 500: break
    key,val = ite
    if len(val)==0:
        continue
    for idxp,content in enumerate(val):
        results = find_exact_keywords(content.lower(),keywords)
        if len(results) == 0:
            continue
        results['context'] = content 
        results['doc_id'] ='DOCID'+str(key)
        results['para_id'] = 'PARAID' + str(key) + '_' + str(idxp)
        df = df.append(results, ignore_index=True)
    
    if idx%100 == 0 :
        print('{}/{}'.format(idx,total_doc_num))
        #print(df.tail())

meta = ['doc_id','para_id','context']
meta.extend(keywords)
meta = [c for c in meta if c in df.columns ]
df = df[meta]
#print(df.head())
df.to_csv('final_results.csv',encoding='utf-8')
