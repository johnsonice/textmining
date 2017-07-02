# coding: utf-8
# #### Preprocess IMDB data 

import numpy as np
import glob
import os 
import pickle

def read_text(path):
    files = glob.glob(path+'/*.txt')
    sentances = list()
    for fi in files:
        with open(fi) as f:
            text = f.read()
        sentances.append(text)
    return sentances


def clean_text(corpus):
    punctuation = """.,?!:;(){}[]"""
    corpus = [z.lower().replace('\n','') for z in corpus]
    corpus = [z.replace('<br />', ' ') for z in corpus]
    
    # treat punctuation as individual words 
    for c in punctuation:
        corpus = [z.replace(c, ' %s '%c) for z in corpus]
    corpus = [z.split() for z in corpus]
    return corpus  


def load_review_data(data_path):
    train_pos_path = os.path.join(data_path,'train','pos')
    train_neg_path = os.path.join(data_path,'train','neg')
    train_unsup_path = os.path.join(data_path,'train','unsup')
    
    train_pos_reviews = read_text(train_pos_path)
    train_neg_reviews = read_text(train_neg_path)
    train_unsup_reviews = read_text(train_unsup_path)
    
    x = np.concatenate((train_pos_reviews, train_neg_reviews),axis=0)
    y = np.concatenate((np.ones(len(train_pos_reviews)), np.zeros(len(train_neg_reviews))))
    x= clean_text(x)
    
    return x,y

def save_processed_data(data_path):
    ## check folder exists
    if not os.path.isdir(data_path): 
        raise ValueError("data folder doesn't exist")
    x,y = load_review_data(data_path)
    pickle.dump((x,y),open(os.path.join(data_path,'imdb.p'),'wb'))


def load_processed_data(path):
    x,y = pickle.load(open(path,'rb'))
    return x,y

####################
## main function ###
####################
if __name__ == '__main__':
    data_path = '../../imdb'
    save_processed_data(data_path)





