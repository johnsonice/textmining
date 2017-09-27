# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 09:47:51 2017

@author: chuang
"""

import zipfile 
import os
import shutil 
import re

#%%

def check(f):
    filename, file_extension = os.path.splitext(f)
    if file_extension == '.zip' or file_extension == '.rar' or file_extension == '.7z':
        return True
    else:
        return False
    
def check_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)        # If not create the directory, inside their home directory
        return True
    
def get_all_files(folder,ext=None):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(folder):
        if ext is None:
            for filename in [f for f in filenames]:
                file_list.append(os.path.join(dirpath, filename))
        else:
            for filename in [f for f in filenames if f.endswith(ext)]:
                file_list.append(os.path.join(dirpath, filename))

    return file_list

def unzip(f_zips,remove=True):
    for f in f_zips:
        zip_ref = zipfile.ZipFile(f,'r')
        dir_name = os.path.dirname(f)
        zip_ref.extractall(dir_name)
        zip_ref.close()
        ## delete the original zip file 
        if remove:
            os.remove(f)

def deep_unzip(folder,remove=True):
    while True:
        f_zips = get_all_files(folder,'.zip')
        if len(f_zips) > 0:
            unzip(f_zips,remove)
        else: break

def find_exact_keywords(content,keyWords):
    content = content.replace('\n', '').replace('\r', '').replace('.',' .')
    r_keyWords = [r'\b' + re.escape(k) + r'\b'for k in keyWords]             # tronsform keyWords list to a patten list
    rex = re.compile('|'.join(r_keyWords),flags=re.I)                        # use or to join all of them, ignore casing
    match = [(m.start(),m.group()) for m in rex.finditer(content)]
    return match