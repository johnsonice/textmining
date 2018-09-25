# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 08:35:31 2018

@author: chuang
"""

import re
#from contractions import CONTRACTION_MAP
import en_core_web_md
from gensim.models import Phrases
from gensim.models.phrases import Phraser

#%%
def expand_contractions(text, contraction_mapping):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def phrase_detect_train(sentances,min_count,threshold,phrase_model_save_path = None):
    """
    input:
        sentances: tokenized sentances 
    """
    print('Transform sentances to trigrams .........\n')
    bi_phrases = Phrases(sentances, min_count=min_count, threshold=threshold)
    bigram_transformer = Phraser(bi_phrases)
    if phrase_model_save_path is not None:
        bi_phrases.save(phrase_model_save_path)
        bigram_transformer.save(phrase_model_save_path+'_transformer')

    sentances = list(bigram_transformer[sentances]) 
    ## if you want to check pharses list
    pharses_list = list(bigram_transformer.phrasegrams)
    print('Phrase model training done.')
    return sentances

def punct_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """
    return token.is_punct or token.is_space

def phrase_detect(bigram_transformer,trigram_transformer,text_tokens):
    """
    function to detect trigrams 
    """
    bi_text_tokens = bigram_transformer[text_tokens]
    tri_text_tokens = trigram_transformer[bi_text_tokens]
    return tri_text_tokens


#%%
if __name__ == "__main__":
    nlp = en_core_web_md.load()
    corpus = ["It's a test sentance, i Don't, i hasn't etc",
            "1. As a small, open, tourism-based economy, St. Lucia is highly vulnerable to exogenous shocks.",
              'Tourism accounts for over three-quarters of exports, and the import content of both consumption and foreign direct investment (FDI) is very high (Figure 1).',
              'The economy has been buffeted by the global economic downturn, which has hobbled the tourism and construction sectors, with potential spillovers to the financial sector.']

    docs = [nlp(d) for d in corpus]
    test_doc = docs[0]
    
    for w in test_doc:
        print(w.orth_,w.is_stop)
    