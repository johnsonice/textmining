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
bigram_transformer_path = os.path.join('data','bigram_transformer')
trigram_transformer_path = os.path.join('data','trigram')
bigram = Phraser.load(bigram_transformer_path)
trigram = Phraser.load(trigram_transformer_path)

#%%
