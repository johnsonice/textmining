# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:27:40 2018

@author: chuang
"""

from gensim.summarization import keywords
import pickle
from docx import Document
import os 
## read this to get more sense of it
##http://bdewilde.github.io/blog/2014/09/23/intro-to-automatic-keyphrase-extraction/

#%%

text='''Challenges in natural language processing frequently involve \
speech recognition, natural language understanding, natural language \
generation (frequently from formal, machine-readable logical forms), \
connecting language and machine perception, dialog systems, or some \
combination thereof.'''

text2 = "This paragraoh is mainly about IMF and it's loan programs. Ok, this is the second sentance. This paragraoh is mainly about IMF and it's loan programs.\
This paragraoh is mainly about IMF and it's loan programs. Ok, this is the second sentance. This paragraoh is mainly about IMF and it's loan programs. \This paragraoh is mainly about IMF and it's loan programs."
keywords(text2,split=True,ratio=1,scores=True,lemmatize=True)
#%%
def get_file_paths(folder_path):
    files = os.listdir(folder_path)
    files = [f for f in files if '.docx' in f]
    files = [f for f in files if not '~' in f]
    files_path = [os.path.join(folder_path,f) for f in files]

    return files,files_path

def read_doc(f_path):
    doc = Document(f_path)
    text_list = [p.text for p in doc.paragraphs if len(p.text)>0]#[3:]
    text_list = [p.replace('\xa0',' ') for p in text_list] # some clean up 
    text_list = [p for p in text_list if len(p.split()) > 15]
    text = ' '.join(text_list)
    return text

#%%

data_folder = '../data/IMFC Communiques'
file_names,files_path = get_file_paths(data_folder)
docs = [read_doc(f) for f in files_path]

#%%
docs[0]
#%%

keywords(docs[-2],split=True,ratio=0.5,scores=True,lemmatize=True)