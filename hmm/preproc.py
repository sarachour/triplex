#!/usr/bin/python

import string
import argparse
import random
import unidecode
import re

import load as Loader 
from dictionaries import *
import onomono

import unicodedata

from nltk.util import ngrams
import nltk
import nltk.tag

from textstat.textstat import textstat

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import * 
import sklearn

from collections import Counter
from sets import Set


#import hmm_model as markov


#NUM_GRAMS = 5
#MIN_PHRASE = 7
NUM_FICS = 100
OUTFILE="out.txt"

parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data_partial(args.directory,NUM_FICS)



print('The nltk version is {}.'.format(nltk.__version__))
print('The scikit-learn version is {}.'.format(sklearn.__version__))


def is_punc(x):
   hasnone=re.search('[a-zA-Z]', x) == None
   return hasnone


def clean_line(line):
      cleanline = re.compile('[\\\\]')
      line = line.replace("Mr.","Mr").replace("Ms.","Ms").replace("Mrs.","Mrs").replace("Dr.","Dr").replace("Prof.","Prof")
      line = unidecode.unidecode(line)
      line = cleanline.sub('',line)
      return line 


def split_line(line):
   toks = line.split();
   if len(toks) < 1:
      return []

   if is_template(toks[0]):
      toks[0] = "@"
   else:
      toks[0] = toks[0].lower()

   #toks[0] = toks[0].lower();
   for i in range(0,len(toks)):
      if is_proper_noun(toks[i]):
         if is_template(toks[i]):
            toks[i] = "@"
         elif not defined_in_dict(toks[i]):
            add_template(toks[i])
            toks[i] = "@"
      else:
         toks[i] = toks[i].lower()

   if(len(toks) < MIN_PHRASE):
      return [];

   toks= (["<start>"]+toks+["<end>"]);
   return toks

def split_periods(line):
   #
   periods = re.compile("([\\.]+|\"|\s\'|\'\s|^\')")
   pers = periods.split(line)
   return pers;

def fic2text(ident,master):
   textsegs = Loader.get_field(data['fics'],ident,'fic') 
   rtags = Loader.get_field(data['base'],ident,'tags')
   rtext = ""
   #tngms = []
   ttoks = Set([])
   atoks = []

   rtext = ""
   for line in textsegs:
      line = clean_line(line)
      rtext += line


   frags = split_periods(rtext)
   #for i in range(0,len(frags)):
   #   if is_punc(frags[i]):
   #      continue
   #   print(frags[i])
   
   #master = markov.train([rtext],NUM_GRAMS,split_callback=split_line,master_dict=master)

   return rtext


print("==== Loaded. Getting Data.... =====")
ids = Loader.get_primaries(data['fics']);
vdata = []
vwords = Set([])
master = None

i=1;
ofh = open("out.txt","w")
for ident in ids:
   print(">> process "+str(ident)+" : # "+str(i))
   text=fic2text(ident,master)
   ofh.write(text)
   i+=1
   #qwords,qdata = fic2text(i)
   #vdata += qdata 
   #vwords.update(qwords)

ofh.close()
import ujson
print("==== Writing to File ======")
fh = open( "model.bin", "wb" )
#pickle.dump(master, fh)
fh.write(ujson.dumps(master))
fh.close()
#
print("==== Finished ======")

#print("===========")
#print("===== Finished Processing Ngrams ===")
#vstat = Counter(vdata)
#for k in vstat:
#   print(k,vstat[k])

#nwords = len(vwords)
#print("number of words:",nwords)

#HiddenMarkovModelTagger(nwords,)
