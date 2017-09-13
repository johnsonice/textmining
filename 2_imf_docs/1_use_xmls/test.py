
import pickle 
import os 
import re
import csv


#%%     
class rep(object):
    def __init__(self,rep_dict):
        self.rep_dict = dict((re.escape(k), v) for k, v in rep_dict.items())
        self.pattern = re.compile("|".join(rep_dict.keys()))
    
    def replace(self,text):
        result = self.pattern.sub(lambda m: self.rep_dict[re.escape(m.group(0))], text)
        return result

def read_pattern(file,rep):
    """
    file: csv file with keyword list
    rep: a class object
    """
    with open(file,'r') as f:
        reader = csv.reader(f)
        mylist = list(reader)
    
    key_list = [l[0].lower() for l in mylist if ' ' in l[0]]
    #key_list = ['liquidity risk']
    print(key_list)
    rep_dict = dict([(s,s.replace(' ','_')) for s in key_list])
    pattern = rep(rep_dict)
    return pattern,key_list

def clean_up_setances(docs,pattern):
    """
    passin a list of documents 
    """
    replace_num = re.compile(r'\(.*?\)')
    docs = [replace_num.sub('',p) for doc in docs for p in doc]
    docs = [pattern.replace(doc.lower()) for doc in docs]
    return docs 




#%%
if __name__ =='__main__':
    
    pattern,keys = read_pattern('keywords.csv',rep)
    
    text = """
    credit risks are liquidity risk liquidity risk types are identified by moderate debt levels, but with short-term debt in 

    """
    
    text = '---'.join(keys)
    
    x = pattern.replace(text)
    print(x)
#%%
file = 'keywords.csv'
with open(file,'r') as f:
    reader = csv.reader(f)
    mylist = list(reader)

key_list = [l[0].lower() for l in mylist if ' ' in l[0]]
#key_list = ['liquidity risk']
print(key_list)