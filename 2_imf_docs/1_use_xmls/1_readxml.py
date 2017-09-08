# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 09:30:59 2017

@author: chuang
"""
import os 
import glob
from bs4 import BeautifulSoup
import csv
import pickle
import sys
from functools import partial
from multiprocessing import Pool,Lock


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
    #with open(file,'r') as f: ## for testing
    with open(file,'r',encoding='utf8') as f:
        soup = BeautifulSoup(f, 'xml')
        
    soup = clean_fig_table(soup)
    p_list = soup.body.find_all('p')
    
    ## check see if documents are structure in this way 
    if len(p_list) ==0 : 
        return p_list 
    
    p_list =  [ele.get_text().replace('\n',' ') for ele in p_list]
    
    return p_list

def multi_extract(file,print_every,logfile):
    idx,f = file
    if (idx+1) % print_every == 0: print(idx+1)
    try:
        sent = extract_xml_paras(f)
        return sent
    except:
        print('corrupted file: ',idx,f,sys.exc_info()[0])
        with open(logfile,'a') as c:
            writer = csv.writer(c)
            writer.writerow([idx,f])
        return [] ## return empty list if error out 

def init(l):
    global lock
    lock = l
    
#%%
## read xml file 
def extract_all_folder(file_path,out_path):
    files = glob.glob(os.path.join(file_path,'*.xml'))  ## only pick one for test
    logfile = 'logfile.csv'
    print_every = 1000
    n_core = os.cpu_count()-1 
    test = False
    multi= True
    
    ## open up a log file 
    with open(logfile,'w') as c:
        writer = csv.writer(c)
        writer.writerow(['index','file'])
    ## run thrugh all files 
    if test: 
        files = files[:200]
        n_core = 2
        print_every = 50
    print('Number of files it is going to go through: ',len(files))
    
    ## use multi core
    if multi:
        print('using multi core: ', n_core)
        l=Lock()
        p = Pool(initializer=init, initargs=(l,),processes=n_core)
        p_extract_xml = partial(multi_extract,print_every=print_every,logfile=logfile)   
        try:
            print('run multi process')
            results = p.map(p_extract_xml,enumerate(files),chunksize=10)
        except:
            print('Error')
            p.close()
            p.join()
            p = None
            print('Finish')
            pass
        
        p.close()
        p.join()
        p = None
    ## use multi core
    else:
        print('using single core')
        results = list()
        log_list = list()
        for idx,f in enumerate(files):
            if (idx+1) % print_every == 0: print(idx+1)
            try:
                sent = extract_xml_paras(f)
                results.extend(sent)
            except:
                print('corrupted file: ',idx,f,sys.exc_info()[0])
                log_list.append((idx,f))
                with open(logfile,'a') as c:
                    writer = csv.writer(c)
                    writer.writerow([idx,f])
    
    results = [f for f in results if len(f)>0]
    pickle.dump(results,open(out_path, "wb"))
    #total_results = pickle.load(open("sentances.p", "rb"))
    #results = [extract_xml_paras(f) for f in files]

#%%
if __name__ =='__main__':
    data_folder = 'data/'
    des_folder = 'xml/'
    sub_folders = os.listdir(des_folder) 
    folder_path = os.getcwd()
    for f in sub_folders:
        f_path = os.path.join(des_folder,f)
        out_path = os.path.join(folder_path,'pickle','sentances' + f + '.p')
        extract_all_folder(f_path,out_path)