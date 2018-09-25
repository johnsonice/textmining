# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 08:35:31 2018

@author: chuang
"""
import en_core_web_md
nlp = en_core_web_sm.load()
doc = nlp('this is a sentence')