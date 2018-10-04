from xml_report_process import *
from xml_server_connect import Connect_SQL_Server
from collections import defaultdict
import pandas as pd
import re
import os
import ftfy
import nltk
import string
import unicodedata

INPUT_PATH = './input'
GROUP_COUNTRY_FILE = 'grouped_country_update.csv'
GROUP_PHRASE_FILE = 'grouped_phrases.csv'
BIGRAM_FILE = 'bigram_phrases.txt'
TRIGRAM_FILE = 'trigram_phrases.txt'

BIGRAM_DICTIONARY = []
with open(os.path.join(INPUT_PATH, BIGRAM_FILE)) as F:
    for L in F.readlines():
        BIGRAM_DICTIONARY.append(L.strip())

TRIGRAM_DICTIONARY = []
with open(os.path.join(INPUT_PATH, TRIGRAM_FILE)) as F:
    for L in F.readlines():
        TRIGRAM_DICTIONARY.append(L.strip())

PUNCT = set(string.punctuation)
PUNCT |= set('—’—‰‱‘‛“”„‟')

STOPWORDS = set(nltk.corpus.stopwords.words('english'))
STOPWORDS |= set(['i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv','xvi','xvii','xviii','xix','xx', 'annex', 'e.g.',\
                  'staff', 'authority', 'bps', 'pb','percent', 'percents', 'percentage_points', 'percentage_point', 'box', 'figure', 'agree', 'view','however','time', 'note','central_bank_name', \
                  'country_name', 'currency_name', 'imf', 'a.','b.', 'c.', 'd.', 'e.', 'f.', 'g.', 'b','c', 'f','’','u','could','would','may','also', 'title', 'since', "'s"])

def build_group_common_patterns():
    grouped_country = pd.read_csv(os.path.join(INPUT_PATH, GROUP_COUNTRY_FILE))
    grouped_country_patterns = dict()
    for i in list(grouped_country):
        temp_pattern = grouped_country[i].dropna().tolist()
        for n, j in enumerate(temp_pattern):
            j_sub = r'(?<=!^)|(?<=\W)' + j.strip() + r'(?=$|\W)'
            temp_pattern[n] = j_sub
        all_pattern = re.compile('|'.join(temp_pattern), re.IGNORECASE)
        grouped_country_patterns[i] = all_pattern
    return grouped_country_patterns

GROUPED_COUNTRY_PATTERNS = build_group_common_patterns()

def build_group_synonym_patterns():
    grouped_phrases = pd.read_csv(os.path.join(INPUT_PATH, GROUP_PHRASE_FILE))
    grouped_synonym_patterns = dict()
    for i in list(grouped_phrases):
        temp_pattern = grouped_phrases[i].dropna().tolist()
        for n, j in enumerate(temp_pattern):
            j_sub = r'(?<=!^)|(?<=\W)' + j.strip() + r'(?=$|\W)'
            temp_pattern[n] = j_sub
        all_pattern = re.compile('|'.join(temp_pattern), re.IGNORECASE)
        grouped_synonym_patterns[i] = all_pattern
    return grouped_synonym_patterns

GROUPED_SYNONYM_PATTERNS = build_group_synonym_patterns()

def group_common_token(text, grouped_country_patterns=GROUPED_COUNTRY_PATTERNS):
    grouped_country = pd.read_csv(os.path.join(INPUT_PATH, GROUP_COUNTRY_FILE))
    for i in list(grouped_country):
        all_pattern = grouped_country_patterns[i]
        re_text = re.sub(all_pattern, i, text)
        text = re_text
    return text

def group_synonym_token(text, grouped_synonym_patterns=GROUPED_SYNONYM_PATTERNS):
    grouped_phrases = pd.read_csv(os.path.join(INPUT_PATH, GROUP_PHRASE_FILE))
    for i in list(grouped_phrases):
        all_pattern = grouped_synonym_patterns[i]
        re_text = re.sub(all_pattern, i, text)
        text = re_text
    return text

def group_bigram(text):
    for phrases in BIGRAM_DICTIONARY:
        words = phrases.split('_')
        pattern = re.compile(r'%s' % "\s+".join(words), re.IGNORECASE)
        replacement =r'%s' % "_".join(words) 
        text = pattern.sub(replacement, text)
    return text

def group_trigram(text):
    for phrases in TRIGRAM_DICTIONARY:
        words = phrases.split('_')
        pattern = re.compile(r'%s' % "\s+".join(words), re.IGNORECASE)
        replacement =r'%s' % "_".join(words) 
        text = pattern.sub(replacement, text)
    return text

def normalization(text):
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer().lemmatize

    lemma_content_list = list()
    sents = nltk.tokenize.sent_tokenize(text.lower())
    lemma_sents = list()
    for sentence in sents:
        tags = nltk.pos_tag(nltk.word_tokenize(\
                            re.sub('—|/',' — ',ftfy.fix_text(sentence))), \
                            tagset='universal')
        lemma_sent = list()
        for tag in tags:
            if tag[0] in STOPWORDS:
                continue
            if tag[1] == '.' or tag[0] in PUNCT:
                continue
            #end-2017
            if tag[1] == 'NUM' or re.match('\d{2,4}', tag[0]) is not None or\
                any([unicodedata.name(c).startswith('VULGAR FRACTION') for c in tag[0]]):
                continue
#            if tag[1] == '.' or tag[0] in PUNCT:
#                continue
            if '_' in tag[0]:
                word_list = tag[0].split('_')
                word_list = [lemmatizer(w, 'n') for w in word_list]
                lemma_sent.append('_'.join(word_list))
            elif tag[1] == 'VERB':
                lemma_sent.append(lemmatizer(tag[0],'v'))
            elif tag[1] == 'ADJ':
                lemma_sent.append(lemmatizer(tag[0],'a'))
            elif tag[1] == 'ADV':
                lemma_sent.append(lemmatizer(tag[0],'r'))
            else:
                lemma_sent.append(lemmatizer(tag[0],'n'))
        if len(lemma_sent)>0:
            lemma_sents.append(lemma_sent)
    return lemma_sents

if __name__ == '__main__':
    query = '''select d.*, p.Country, p.Title
                from [IMF_EPUBS].[dbo].[DOCUMENT] as d left join 
                  [IMF_EPUBS].[dbo].[PUBLICATION] as p 
                  on d.SeriesNumber=p.SeriesNumber
                where p.Title like '%Peru%Article IV%' 
                      and d.PublisherId like '%A001%' 
                order by SeriesNumber'''
    imfReportServer = Connect_SQL_Server()
    imfReportServer.Execute_Query(query, name='Article IV')
    row = imfReportServer.cursor.fetchone()
    contents = extract_text_from_report(row.Content)
    for content in contents:
        print(content)
        text_1 = group_common_token(content)
        print(text_1)
        text_2 = group_synonym_token(text_1)
        print(text_2)
        text_3 = group_bigram(group_trigram(text_2))
        print(text_3)
        lemma_sents = normalization(text_3)
        print(lemma_sents)
        import pdb;pdb.set_trace()

