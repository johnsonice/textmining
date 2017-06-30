
# coding: utf-8

# In[4]:

import nltk
import os 
import glob
import re
import  pickle
from nltk.tokenize import sent_tokenize, word_tokenize
from functools import partial
from multiprocessing import Pool


# In[5]:

def useless_words(delete_words,target):
    for w in delete_words:
        if w in target:
            return False
    return True

def process_documents(fi,delete_words,replace_regex,number_regex):
    index, file = fi 
    with open(file,'r',encoding='utf-8') as f:
        text = f.read()
    text = replace_regex.sub(' ',text)
    text = re.sub(r'\(.*?\d+.*?\)|\s\s\s\s+\d','',text)  # clean up things like '(box 1)' and  '     1'
    sentances = sent_tokenize(text)
    
    clean_sentances= list()
    for line in sentances:
        if useless_words(delete_words,line):
            tokens = word_tokenize(line)
            if len(tokens)>5:
                wl = [len(t) for t in tokens]
                if max(wl)<30:
                    line = number_regex.sub(' ',line)
                    tokens = word_tokenize(line.lower())
                    clean_sentances.append(tokens)
    if index%1000 == 0: print('finished ', index)
    return clean_sentances


# In[6]:

if __name__ =='__main__':
    
    ## run a small sample of test first 
    test = False
    
####################################
## set up some global variables 
####################################

    delete_words = ['____','DOCUMENT OF INTERNATIONAL MONETARY FUND','Download Date']
    replace_regex = re.compile(r'\uf0b7|\x0c')
    number_regex = re.compile(r'\d+?\.\d+|\.\d+|\d+-\d+|\d+/\d+|\d+/|-\d+|\d+|½|¼|¼|⅔|¾/') ## clean up all kinds of numbers
    #test = '123.45 123.25 1234 .245 2015-218  -60 1/asdf 2/asdf  2021/22 ////'
    #replace_regex.findall(test)

    files_path = 'txt_files_finished/'
    files = sorted(glob.glob(files_path+'*.txt'))
    if len(files) == 0:
        raise ValueError('could not find input files')
        
###############################
## run text process in parellel
###############################
    ## multi process it 
    num_cores = os.cpu_count()
    
    ## see if we want to run a test first
    if test == True: 
        files = files[:100]
        num_cores = 2
    else:
        num_cores = os.cpu_count()
    
    #multi process unpacking
    p = Pool(num_cores)
    partial_unpack = partial(process_documents,delete_words=delete_words,replace_regex=replace_regex,number_regex=number_regex)
    process_mp = p.map(partial_unpack,enumerate(files))
    p.close()
    p.join()
    print('finish')



    # In[12]:

    total_results = [l for sublist in process_mp for l in sublist]
    pickle.dump(total_results,open("sentances.p", "wb"))
    #total_results = pickle.load(open("sentances.p", "rb"))




