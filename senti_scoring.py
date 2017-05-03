# -*- coding: utf-8 -*-
"""
Created on Wed May  3 01:30:17 2017

@author: cydru
"""

import nltk
from nltk import sentiment
import os
import pandas as pd
import numpy as np
import re

Care_Tagset = ['JJ','JJR','JJS','MD','NN','NNS','NNP','NNPS','RB','RBR','RBS',
               'VB','VBD','VBG','VBN','VBP','VBZ']
Harvard_Selected = ['Positiv','Negativ','Pstv','Ngtv','Strong','Weak','Active',
                   'Passive','EMOT','Virtue','Vice','Ovrst','Undrst','Role',
                   'Need','Goal','Try','Means','Persist','Complet','Fail',
                   'Think','Know','Causal','Ought','Perceiv','Compare','EVAL',
                   'Solve','ABS']
LM_Selected = ['Negative','Positive','Uncertainty','Litigious',
               'Constraining','Superfluous','Interesting',	'Modal']
LM_MasterDict = pd.read_excel('LoughranMcDonald_MasterDictionary_2014.xlsx')
HV4_INQ = pd.read_excel('inquireraugmented.xls')
HVred = HV4_INQ.loc[2:,['Entry']].astype(str)
HVred[Harvard_Selected]=pd.notnull(HV4_INQ.loc[2:,Harvard_Selected])
LMred = LM_MasterDict.loc[:,['Word']].astype(str)
LMred[LM_Selected]=np.sign(LM_MasterDict.loc[2:,LM_Selected])
lLM = len(LM_Selected)
ltotal = len(Harvard_Selected + LM_Selected)

HVred['Entry'] = HVred['Entry'].replace(r'#.*','',regex=True)
HVred = HVred.groupby(['Entry'], as_index=False)[Harvard_Selected].mean()

HVdict = HVred['Entry'].tolist()
LMdict = LMred['Word'].tolist()

def read_bulk(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            lines.append(line)
    blob = ' '.join(lines)
    return blob

def get_candidates(blob):
    wnl = nltk.stem.wordnet.WordNetLemmatizer()
    wordlist = []
    prev_not = False
    tokens = nltk.tokenize.word_tokenize(blob)
    token_pospairs = nltk.pos_tag(tokens)
    # negated = sentiment.util.mark_negation(tokens) # not a good function
    for ind, pair in enumerate(token_pospairs):
        if pair[0]=='not':
            prev_not = True
        elif (pair[1]=='.') or (pair[1]==',') or (pair[1]==':'):
            prev_not = False
        elif pair[1] in Care_Tagset:
            stemmed = wnl.lemmatize(pair[0])
            if prev_not:
                stemmed = 'not_' + stemmed
                prev_not = False
            wordlist.append(stemmed.upper())
    return wordlist

def find_scores(docwords):
    cumscore = np.zeros((ltotal,), dtype=float)
    for word in docwords:
        if word in LMdict:
            cumscore[0:lLM] += \
            LMred.query('Word=="%s"' % word).as_matrix(LM_Selected)[0]
        if word in HVdict:
            cumscore[lLM:] += HVred.query(
                    'Entry=="%s"' % word).as_matrix(Harvard_Selected)[0]
    
    return(cumscore)
