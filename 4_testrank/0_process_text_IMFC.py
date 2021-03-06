# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 13:03:40 2018

@author: chuang
"""
import pickle
import os
#import util 
import re
import csv
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from docx import Document
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import pandas as pd
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import copy
from math import log
#%%
def dummy_func(doc):
    return doc

class rep(object):
    def __init__(self,rep_dict):
        self.rep_dict = dict((re.escape(k), v) for k, v in rep_dict.items())
        self.pattern = re.compile("|".join(rep_dict.keys()))
    
    def replace(self,text):
        result = self.pattern.sub(lambda m: self.rep_dict[re.escape(m.group(0))], text)
        return result

def _baisc_tokenizer(para):
    """
    para: one paragraph. can also be the entire document
    this function will tokenize a paragraph by sentances and by token
    """
    words = word_tokenize(para.lower())
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in words]    
    return tokens 

def process_keys(file,outfile):
    with open(file,'r',encoding='utf-8',) as f:
        reader = csv.reader(f)
        mylist = list(reader)
        
    key_list = [s[0].replace('\ufeff','').replace(' ,',',') for s in mylist]
    key_list = [' '.join(_baisc_tokenizer(l)) for l in key_list]
    
        ## export keywords
    with open(outfile,'w',encoding='utf-8') as resultFile:
        wr = csv.writer(resultFile, lineterminator='\n')
        [wr.writerow([k]) for k in key_list]
    print('output updated keyword list: success')

def read_pattern(file):
    """
    file: csv file with keyword list
    rep: a class object
    """
    with open(file,'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        my_list = list(reader)
    
    key_list= [l[0].lower() for l in my_list]
    rep_dict = dict([(s,s.replace(' ','_')) for s in key_list])
    pattern = rep(rep_dict)
    return pattern

def has_number(inputString):  
    """
    check if string contrain numbers 
    """
    return bool(re.search(r'\d', inputString))
    
def my_tokenizer(s):
    s = s.lower() # downcase
    tokens= _baisc_tokenizer(s)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [t for t in tokens if t not in stopword_list] # remove stopwords
    tokens = [t for t in tokens if not has_number(t)]
    return tokens

def phrase_detect(bigram_transformer,trigram_transformer,text_tokens):
    bi_text_tokens = bigram_transformer[text_tokens]
    tri_text_tokens = trigram_transformer[bi_text_tokens]
    return tri_text_tokens

def clean_up_setances(docs,pattern):
    """
    passin a list of documents 
    """
    #replace_num = re.compile(r'\(.*?\)')
    #docs = [replace_num.sub('',doc) for doc in docs]
    #docs = [' '.join(my_tokenizer(d)) for d in docs]
    docs = [' '.join(_baisc_tokenizer(d)) for d in docs]
    docs = [pattern.replace(doc.lower()) for doc in docs]
    return docs 

def read_doc(f_path):
    doc = Document(f_path)
    text_list = [p.text for p in doc.paragraphs if len(p.text)>0]#[3:]
    text_list = [p.replace('\xa0',' ') for p in text_list] # some clean up 
    text_list = [p for p in text_list if len(p.split()) > 15]
    #text = ' '.join(text_list)
    return text_list

def text_for_idf(files_path):
    docs = [read_doc(f) for f in files_path]
    return docs

def get_file_paths(folder_path):
    files = os.listdir(folder_path)
    files = [f for f in files if '.docx' in f]
    files = [f for f in files if not '~' in f]
    files_path = [os.path.join(folder_path,f) for f in files]

    return files,files_path
#%%
data_folder = './data/IMFC Communiques'
file_names,files_path = get_file_paths(data_folder)
docs = text_for_idf(files_path)

#%%
## start process text 
wordnet_lemmatizer = WordNetLemmatizer()
stopword_list = stopwords.words('english')
process_keys('input/key_words.csv','input/key_words_update.csv')
pattern = read_pattern('input/key_words.csv')
docs_list = [[pattern.replace(p.lower()) for p in doc] for doc in docs]
pattern = read_pattern('input/key_words_update.csv')
docs_list = [clean_up_setances(doc,pattern) for doc in docs_list] ## replace phrases
#%%
docs_list = [[word_tokenize(p) for p in doc] for doc in docs_list]
bigram_transformer = Phraser.load(os.path.join('data','bigram_transformer'))
trigram_transformer = Phraser.load(os.path.join('data','trigram_transformer'))
docs_list = [[phrase_detect(bigram_transformer,trigram_transformer,p) for p in doc] for doc in docs_list]

#%%
##export to pickle
pickle.dump((file_names,docs_list), open( "data/processed_docs.p", "wb" ) )


