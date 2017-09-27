# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 18:54:39 2017

@author: jbarkema
"""

import os
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import csv
import pickle

#%%
## define some functions 
def get_ids(xml):
    """
    input xml full name, return series id and file id 
    """
    series_id,xml_name = xml.split('-')
    file_id,_ = xml_name.split('_') 
    return series_id,file_id

def read_ids(file):
    """
    file: csv file with keyword list
    rep: a class object
    """
    with open(file,'r') as f:
        reader = csv.reader(f)
        meta = list(reader)
        ids = [row[3] for row in meta ][1:]
    return ids,meta

class document(object):
    def __init__(self,series_id,file_id,xml_path):
        #print('initiate doc object')
        self.file_id = file_id
        self.series_id = series_id
        self.xml_path = xml_path
        self.text = self.load_xml()
    
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
            text = soup.text
        except:
            print('file corropted: {}'.format(self.file_id))
            return []
    
        return text
#%%
process_xml_data = False

if process_xml_data:
    ## read staff report meta data
    report_list_path = "staff_reports_meta.csv"
    ids,meta = read_ids(report_list_path)
    
    ## read files list to get through 
    folder_path = "d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls/xml/002"
    files = os.listdir(folder_path)
    files = [f for f in files if '_' in f]  ## have to have _ in file name 
    
    ## check if file id in staff_id
    files = [f for f in files if get_ids(f)[1] in ids]
    
    ## read xml texts 
    doc_list = list()
    total_length = len(files) + 1 
    print('converting {} xmls into text ......'.format(total_length))
    for idx,file_name in enumerate(files):
        xml_path = os.path.join(folder_path,file_name)
        try:
            series_id,file_id = get_ids(file_name)
        except:
            continue
        doc = document(series_id,file_id,xml_path)
        doc_list.append(doc)
        if (idx+1)%100 == 0:
            print('{} / {} '.format(idx+1,total_length))
            
    process_text = 'text.p'
    pickle.dump(doc_list,open(process_text, "wb"))
    print('done')


#%%
#######################################
### extract missione chief ############
#######################################

## load data 
docs = pickle.load(open('text.p', "rb")) 

## now extract mission chiefs
reg_test1 = re.compile(r'(staff|missio\w+|program|team)(\,|\s?)?\s?(team|members|missio\w+)?\s?(compris\w+|participat\w+|consist\w+|includ\w+|:) (.*?)(head|chief)', re.IGNORECASE)
reg_test2 = re.compile(r'(staff|missio\w+|program|team)(\,|\s?)?\s?(team|members|representat\w+|missio\w+)?\s?(compris\w+|participat\w+|consist\w+|includ\w+|was|were|are|:) (.*?)(head|chief|\,)', re.IGNORECASE)

chiefs = []
errors = []

for doc in docs:
    try:
        content = doc.text
        content = re.sub(' +', ' ', content)
        content = re.sub('\n', '', content)
        content = re.sub('- ', '', content)
    
        results = reg_test1.findall(doc.text)
        if len(results)>0:
            for mc in results:
                _,_,_,_,result,_ = mc
                if len(result)<120:
                    chiefs.append((doc.file_id,result))
                else: 
                    #chiefs.append(doc.file_id+", "+"Not Found") 
                    pass
        else:
            results = reg_test2.findall(content)
            if len(results)>0:
                for mc in results:
                    _,_,_,_,result,_ = mc
                    if len(result)<120:
                        chiefs.append((doc.file_id,result))
                    else:
                        #chiefs.append(doc.file_id+", "+"Not Found")
                        pass
            else:
                #chiefs.append(doc.file_id+", "+"Not Found") 
                pass
    except:
        errors.append(doc.file_id)
        #print("error :", doc.file_id)
        
        
#export results to excel 
chiefs = pd.DataFrame(chiefs)
writer = pd.ExcelWriter('MCs.xlsx', engine='xlsxwriter')
chiefs.to_excel(writer, sheet_name='Sheet1')
errors = pd.DataFrame(errors)
errors.to_excel(writer, sheet_name='error')
writer.save()


#%%
## test 
folder_path = "d:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls/xml/002"
file_name =  '08467-9781451835809_A002.xml'
xml_path = os.path.join(folder_path,file_name)
series_id,file_id = get_ids(file_name)
doc = document(series_id,file_id,xml_path)
text = doc.text

content = doc.text
content = re.sub(' +', ' ', content)
content = re.sub('\n', '', content)
content = re.sub('- ', '', content)

chiefs = []
errors = []

results = reg_test1.findall(doc.text)
if len(results)>0:
    for mc in results:
        _,_,_,_,result,_ = mc
        if len(result)<120:
            chiefs.append((doc.file_id,result))
else:
    results = reg_test2.findall(content)
    if len(results)>0:
        for mc in results:
            _,_,_,_,result,_ = mc
            if len(result)<120:
                chiefs.append((doc.file_id,result))

print(chiefs)
