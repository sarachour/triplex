#!/usr/bin/python

import string
import argparse
import random
import re
import load as Loader 
import unicodedata
from nltk.util import ngrams
import nltk
from textstat.textstat import textstat
from collections import Counter

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import * 
import sklearn


parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data_partial(args.directory,20)

print('The nltk version is {}.'.format(nltk.__version__))
print('The scikit-learn version is {}.'.format(sklearn.__version__))

def fic2text(ident):
   textsegs = Loader.get_field(data['fics'],ident,'fic') 
   rtags = Loader.get_field(data['base'],ident,'tags')
   rtext = ""
   tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+[*\w]+')
   punc = "[\.,?!]"
   tngms = []
   num_grams = 3

   for line in textsegs:
      line = line.replace(u'\xa0',' ')
      line = line.encode('ascii', 'ignore').decode('ascii').lower()
      frags = re.compile(punc).split(line)
      for frag in frags:
         toks = tokenizer.tokenize(frag)
         ngms = list(ngrams(toks,num_grams,pad_right=False,pad_left=False))
         tngms += ngms 

   #starting = model("t")
   #content = model.generate(10,starting)
   #print(" ".join(content))

   #tokens = nltk.word_tokenize(rtext)
   return tngms

print("==== Loaded. Getting Data.... =====")
ids = Loader.get_primaries(data['fics']);
vdata = []

for i in ids:
   vdata += fic2text(i)

vstat = Counter(vdata)
for k in vstat:
   print(k,vstat[k])
