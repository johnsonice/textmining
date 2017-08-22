# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 09:30:59 2017

@author: chuang
"""
import os 
import glob
from bs4 import BeautifulSoup


def clean_fig_table(soup):
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

#%%
def extract_xml_with_sections(file):
    with open(file,'r') as f:
        soup = BeautifulSoup(f, 'xml')
        
    soup = clean_fig_table(soup)
        
    document = list()
    sections = soup.body.find_all(['sec'], recursive=False)
    
    print(len(sections))
    ## check see if documents are structure in this way 
    if len(sections) ==0 : 
        return document 

    for sec in sections:
        elements = [ele for ele in sec.children if ele.name is not None ]
        p_list =  [ele.get_text().replace('\n',' ') for ele in elements]
        document.append(p_list)
    
    return document
#%%
def extract_xml_paras(file):
    with open(file,'r') as f:
        soup = BeautifulSoup(f, 'xml')
        
    soup = clean_fig_table(soup)
    p_list = soup.body.find_all('p')
    
    ## check see if documents are structure in this way 
    if len(p_list) ==0 : 
        return p_list 
    
    p_list =  [ele.get_text().replace('\n',' ') for ele in p_list]
    
    return p_list
#%%

## read xml file 
file_path = 'U:/SPRDU/documents/'
files = glob.glob(file_path+'*.xml')  ## only pick one for test
#files = files[1]
results = [extract_xml_paras(f) for f in files]

