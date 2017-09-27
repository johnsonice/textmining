# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 09:47:51 2017

@author: chuang
"""

import zipfile 
import os
import shutil 
import csv

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

#%%
data_folder = 'data/'
des_folder = 'xml/'
output_folder = 'outputs/'
#sub_folders = ['001','002']
sub_folders = os.listdir(data_folder) 
print(sub_folders)

#%%
print('unziping all folders under', data_folder)
deep_unzip(data_folder,remove=True)

for fo in sub_folders:
    print('processing', fo )
    file_folder =os.path.join(data_folder,fo) 
    f_xmls = get_all_files(file_folder,'.xml')
    
    ## move to destination folder 
    xml_folder = os.path.join(des_folder,fo)
    _ = check_dir(xml_folder)
    for f in f_xmls:
        shutil.move(f,os.path.join(xml_folder,os.path.basename(f)))
    

## write out xml names, see if they match up with database
fs = get_all_files(des_folder)
fns = [os.path.splitext(os.path.basename(f))[0] for f in fs]
fns = [f for f in fns if not '_' in f] 

with open(os.path.join(output_folder,'filenames.csv'),'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(fns))




