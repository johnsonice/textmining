# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:47:20 2017

@author: chuang
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 18:54:39 2017

@author: jbarkema
"""

#import PyPDF2
import os
import re
import glob
import pandas as pd
import numpy as np
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io

#%%
def convert(case,fname, pages=None):
    """
    case = ['txt','html']
    fname = file path 
    
    """
    if not pages:
        pagenums = set();
    else:
        pagenums = set(pages);      
    codec = 'utf-8'
    caching = True
    #laparams = LAParams()
    laparams = None
    #password = ''
    #maxpages = 0
    manager = PDFResourceManager(caching=caching) 
    if case == 'txt' :
        output = io.StringIO()
        converter = TextConverter(manager, output, codec=codec, laparams=laparams)     
    if case == 'HTML' :
        output = io.BytesIO()
        converter = HTMLConverter(manager, output, codec=codec, laparams=laparams)
        
    interpreter = PDFPageInterpreter(manager, converter)   
    infile = open(fname, 'rb')

    for index,page in enumerate(PDFPage.get_pages(infile, pagenums,caching=caching, check_extractable=True)):
        interpreter.process_page(page)

    convertedPDF = output.getvalue()


    infile.close();
    converter.close();
    output.close()
    
    return convertedPDF

#%%
#file_path = 'Q:/DATA/AI/JelleBarkema/DP Mission Chief Project/Documents'
folder = 'd:/usr-profiles/chuang/Desktop/Dev/textmining/2_imf_docs/1_use_xmls/data/pdfs'
dest_folder = 'data/txt'
file_names = os.listdir(folder)
error = list()

for idx,f in enumerate(file_names):
    if idx ==0: print('start processing files, total: {}'.format(len(file_names)))
    if (idx+1) % 10 ==0 : print('processing {}'.format(idx+1))
    f_name = os.path.splitext(os.path.basename(f))[0] + '.txt'
    file_path = os.path.join(folder,f)
    file_dest = os.path.join(dest_folder,f_name)
    
    try:
        content = convert('txt',file_path)
        with open(file_dest,'w') as out_file:
            out_file.write(content)
    except:
        print('error: ',f)
        error.append(f)
        

with open('log.txt','w') as out_file:
    for e in error:
       out_file.write(e)

print('finished')




#%%
#test_file = os.path.join(folder,file_names[0])
#content = convert('txt',test_file)
