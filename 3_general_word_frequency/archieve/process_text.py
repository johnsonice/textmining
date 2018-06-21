# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 16:30:34 2018

@author: CHuang
"""

from docx import Document
import os 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Phrases
from gensim.models.phrases import Phraser

from collections import Counter
#%%

f_path = os.path.join('data','IMFC_Communique_Aor18.docx')
doc = Document(f_path)
#%%
text_list = [p.text for p in doc.paragraphs if len(p.text)>0][3:]
text_list = [p.replace('\xa0',' ') for p in text_list] # some clean up 
text = ' '.join(text_list)
#%%

wordnet_lemmatizer = WordNetLemmatizer()
stopwords = stopwords.words('english')

def  my_tokenizer(s):
    s = s.lower() # downcase
    tokens = nltk.tokenize.word_tokenize(s) # split string into words (tokens)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if t not in stopwords] # remove stopwords
    return tokens

text_tokens = my_tokenizer(text)

#%%

bigram_transformer = Phraser.load(os.path.join('data','bigram_transformer'))
bi_text_tokens = bigram_transformer[text_tokens]
#%%
trigram_transformer = Phraser.load(os.path.join('data','trigram_transformer'))
tri_text_tokens = trigram_transformer[bi_text_tokens]
#%%
counts = Counter(tri_text_tokens)
vocab = sorted(counts, key=counts.get, reverse=True)

#%%
wordcloud = WordCloud().generate(tri_text_tokens)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")












#%%
wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()