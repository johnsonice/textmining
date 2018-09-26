# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:01:17 2018

@author: chuang
"""

import re
#from contractions import CONTRACTION_MAP
import en_core_web_md
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import os


#%%
###Latent Semantic Indexing

## topic modeling 
total_topics = 15
lsi = models.LsiModel(corpus_tfidf,
                      id2word=dictionary,
                      num_topics= total_topics)

## now you can see topic by index, words and weights 
print(lsi.show_topic(1))


## a better way to print 
def print_topics_gensim(topic_model, total_topics=1,
                        weight_threshold=0.0001,
                        display_weights=False,
                        num_terms=None):
    
    for index in range(total_topics):
        topic = topic_model.show_topic(index,topn=num_terms)
        topic = [(word, round(wt,4)) 
                 for word, wt in topic 
                 if abs(wt) >= weight_threshold]
        if display_weights:
            print('Topic #'+str(index+1)+' with weights')
            print (topic[:num_terms] if num_terms else topic)
        else:
            print ('Topic #'+str(index+1)+' without weights')
            tw = [term for term, wt in topic]
            print (tw[:num_terms] if num_terms else tw)
        print

print_topics_gensim(topic_model=lsi,
                    total_topics=total_topics,
                    num_terms=5,
                    display_weights=True)
