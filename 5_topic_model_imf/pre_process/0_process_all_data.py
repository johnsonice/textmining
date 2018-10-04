# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 15:17:38 2018

@author: chuang
"""
from  pre_process_report import *
import pickle
from multiprocessing import Pool
import os 
#%%
def process_data(content):
    text_1 = group_common_token(content)
    text_2 = group_synonym_token(text_1)
    text_3 = group_bigram(group_trigram(text_2))
    lemma_sents = normalization(text_3)
    return lemma_sents

#%%
if __name__ == '__main__':
    ## read all data 
    raw_data_path = '../data/article_IV_corpus.txt'
    #workers = 1 
    workers = int(os.cpu_count()/2)  ## if you want to multi process
    save_data = False
    dump_data_path = '../data/lemma_corpus.p'
    
    
    ## read raw file
    with open(raw_data_path,'r',encoding='utf8') as f:
        lines = f.readlines()
        lines = [l.strip(' \n') for l in lines if len(l)>50]
        
    ## normalize and tokenize and lemmantize text
    if workers <2:
        print('Toatl number of paragraphs:{}'.format(len(lines)))
        contents = list()
        for idx,content in enumerate(lines):
            lemma_sents = process_data(content)
            contents.append(lemma_sents)
            if idx%1000 == 0: print('{}/{}'.format(idx,len(lines)))
    else:
        print('Running data process in {} processes'.format(workers))
        print('Total number of paragraph to be processed {}'.format(len(lines)))
        p = Pool(workers)
        contents = p.map(process_data,lines)
        p.close()
        p.join()
        print('Finised total number of elements: {}'.format(len(contents)))
        print(contents[10])
        

    ## save file 
    if save_data:
        with open(dump_data_path,'wb') as f:
            pickle.dump(contents,f)
