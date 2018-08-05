# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 13:03:40 2018

@author: chuang
"""
import pickle
import os
import util 
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
    
    key_list= [l[0] for l in my_list]
    rep_dict = dict([(s,s.replace(' ','_')) for s in key_list])
    pattern = rep(rep_dict)
    return pattern
    
def  my_tokenizer(s):
    s = s.lower() # downcase
    tokens= _baisc_tokenizer(s)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords
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
    docs = [' '.join(my_tokenizer(d)) for d in docs]
    docs = [pattern.replace(doc.lower()) for doc in docs]
    return docs 

def read_doc(f_path):
    doc = Document(f_path)
    text_list = [p.text for p in doc.paragraphs if len(p.text)>0][3:]
    text_list = [p.replace('\xa0',' ') for p in text_list] # some clean up 
    text = ' '.join(text_list)
    return text
#%%
## start process text 
wordnet_lemmatizer = WordNetLemmatizer()
stopwords = stopwords.words('english')
#%%
file_path = os.path.join('data','xml_docs.p')
process_keys('key_words.csv','key_words_update.csv')
#%%
pattern = read_pattern('key_words.csv')
#%%
file = pickle.load(open(file_path,'rb'))
f_ids = list(file.keys())[:100]
docs = [file[f].paras for f in f_ids]
docs = [' '.join(d) for d in docs] ## join all paragraphs
#%%
## process the actual document we want to process 
f_path = os.path.join('data','IMFC_Communique_Aor18.docx')
text = read_doc(f_path)
docs.append(text)
#%%
## replace phrases
docs = [pattern.replace(doc.lower()) for doc in docs]
pattern = read_pattern('key_words_update.csv')
docs = clean_up_setances(docs,pattern)
docs = [my_tokenizer(d) for d in docs]
bigram_transformer = Phraser.load(os.path.join('data','bigram_transformer'))
trigram_transformer = Phraser.load(os.path.join('data','trigram_transformer'))
docs = [phrase_detect(bigram_transformer,trigram_transformer,d) for d in docs]
#%%
bow_transformer = CountVectorizer(
                        analyzer='word',   ## this can actually be any kind of function to preprocess your text
                        tokenizer=dummy_func,
                        preprocessor=dummy_func,
                        token_pattern=None)  

docs_bow = bow_transformer.fit_transform(docs)
print('Shape of Sparse Matrix: ',docs_bow.shape)
#%%
vocabs = bow_transformer.get_feature_names()
#%%
tf = pd.DataFrame(docs_bow.toarray(),columns=vocabs)
keep_vocab = list(set(docs[-1]))
tf = tf[keep_vocab]
#%%
import copy
from math import log
#%%
N = len(tf)
df = copy.deepcopy(tf)
df[df != 0] = 1
df = df.agg('sum')          ## calculate document frequency 
df.replace(0,1,inplace=True)
idf = df.apply(lambda x:log(N/x))
#%%
## tfidf 
tf_idf = tf*idf

#%%
doc_tf = tf.loc[100].sort_values(ascending=False)
doc_tf.name = 'tf'
doc_tf_idf = tf_idf.loc[100].sort_values(ascending=False)
doc_tf_idf.name = 'tf_idf'
doc_df = pd.concat([doc_tf,doc_tf_idf],axis=1)
#%%
doc_df.to_csv('results.csv')

