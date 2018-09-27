
# coding: utf-8

# Follow this blog post
# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/

# In[1]:


from gensim import corpora, models 
from scripts.normalization import normalize_corpus
import numpy as np
from docx import Document
import sys
import os
import gensim
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import pickle
import nltk
from collections import Counter
#import pyLDAvis
#import pyLDAvis.gensim  # don't skip this
import pickle
python_root = './scripts'
sys.path.insert(0, python_root)

import normalization_spacy as util
from contractions import CONTRACTION_MAP


# #### Load data

# In[2]:


doc_dict = pickle.load(open('./data/xml_docs.p', "rb")) 
ids = list(doc_dict.keys())
print('sample document ids: \n',ids[:5],'\n')
test_docs = doc_dict[ids[0]]
print('sample paragraphs: \n',test_docs.paras[0])


# In[3]:


## faltten all paragraphs 
paras = [doc_dict[i].paras for i in ids]
corpus = list()
for ps in paras:
    corpus.extend(ps)

print('Total number of paragraphs in the corpus: {}'.format(len(corpus)))


#trigram_reviews_filepath = 'data/lemma_docs.txt'


# In[4]:


## faltten all paragraphs by document
paras = [doc_dict[i].paras for i in ids]
corpus = [' '.join(p) for p in paras]
print('Total number of documents in the corpus: {}'.format(len(corpus)))

trigram_reviews_filepath = 'data/lemma_docs_by_doc.txt'


# ### Tokenize and lemmatize corpus

# In[5]:


import en_core_web_md
nlp = en_core_web_md.load()


# In[ ]:


## single / multi threaded 
n_core = 16 
load = False 

if load:
    with open(trigram_reviews_filepath, 'r', encoding='utf_8') as f:
        docs_lemma = f.readlines()
        docs_lemma = [d.strip('\n').split() for d in docs_lemma]
else:
    if n_core == 1:
        docs = [nlp(d) for d in corpus]
        docs_lemma = [[token.lemma_ for token in doc if not util.punct_space(token) ] for doc in docs]
    else:
        with open(trigram_reviews_filepath, 'w', encoding='utf_8') as f:
            for doc in nlp.pipe(corpus,batch_size=200,n_threads=n_core):
                docs_lemma = [token.lemma_ for token in doc if not util.punct_space(token)]
                trigram_para = ' '.join(docs_lemma)
                f.write(trigram_para + '\n')

        with open(trigram_reviews_filepath, 'r', encoding='utf_8') as f:
            docs_lemma = f.readlines()
            docs_lemma = [d.strip('\n').split() for d in docs_lemma]


# In[ ]:

print(corpus[3])
print(docs_lemma[3])

# ### Bigram and Trigram transform
# In[ ]:


train_phrase_model = False
bigram_transformer_path = os.path.join('data','bigram_transformer')
trigram_transformer_path = os.path.join('data','trigram_transformer')
common_terms = ['a','an','of',',','i','about','to',"with", "without"]

if train_phrase_model: 
    paras = util.phrase_detect_train(docs_lemma,min_count=10,threshold=15,common_terms=common_terms,phrase_model_save_path='./data/bigram')
    paras = util.phrase_detect_train(paras,min_count=10,threshold=15,common_terms=common_terms,phrase_model_save_path='./data/trigram')
else:
    bigram_transformer = Phraser.load(bigram_transformer_path)
    trigram_transformer = Phraser.load(trigram_transformer_path)
    paras = util.phrase_detect(bigram_transformer,trigram_transformer,docs_lemma) 
    


# - exam phrases

# In[ ]:


trigram = Phraser.load('data/trigram')
trigram_transformer = Phraser.load('data/trigram_transformer')
for phrase, score in trigram.export_phrases(docs_lemma[:2]):
     print(phrase,score)


# In[ ]:


with open('./data/processed_corpus_by_doc.p','wb') as f:
    pickle.dump(paras,f)


# In[ ]:


# with open('./data/processed_corpus.p','rb') as f:
#     cs = pickle.load(f)

