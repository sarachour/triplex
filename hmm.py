#!/usr/bin/python

import string
import argparse
import random
import unidecode
import re

import load as Loader 
from dictionaries import *

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


import hmm_model as markov


NUM_GRAMS = 5
NUM_FICS = 50

parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data_partial(args.directory,NUM_FICS)



print('The nltk version is {}.'.format(nltk.__version__))
print('The scikit-learn version is {}.'.format(sklearn.__version__))


state = {
   "templs":{},
   "freqs":{},
   "cnt":0
}

def add_template(x):
   handle = "@"+str(state["cnt"])
   state["templs"][x.lower()] = handle
   state["cnt"]+=1
   return handle

add_template("Harry")
add_template("Jim")
add_template("Ginny")
add_template("Sara")
add_template("Sarah")
add_template("Derek")
add_template("William")
add_template("Gilbert")
add_template("Spike")

def reset_state():
   state["templs"] = {}
   state["cnt"] = 0

def is_punc(x):
   hasnone=re.search('[a-zA-Z]', x) == None
   return hasnone

def is_template(x):
   if x.lower() in state["templs"]:
      return True 
   else:
      return False

def is_proper_noun(x):
   if(len(x) < 2):
      return False

   if x[0].isupper() and x[1].islower():
      return True
   else:
      return False

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


   toks= (["<start>"]+toks+["<end>"]);
   return toks

def split_periods(line):
   #
   periods = re.compile("([\\.]+|\"|\s\'|\'\s)")
   pers = periods.split(line)
   return pers;

def fic2text(ident,master):
   textsegs = Loader.get_field(data['fics'],ident,'fic') 
   rtags = Loader.get_field(data['base'],ident,'tags')
   rtext = ""
   #tngms = []
   ttoks = Set([])
   atoks = []

   for line in textsegs:
      line = clean_line(line)
      frags = split_periods(line)
      for i in range(0,len(frags)):
         if is_punc(frags[i]):
            continue
         #print(frags[i])
         master = markov.train([frags[i]],NUM_GRAMS,split_callback=split_line,master_dict=master)

   return master

   #print("===========")

   #starting = model("t")
   #content = model.generate(10,starting)
   #print(" ".join(content))

   #tokens = nltk.word_tokenize(rtext)
   #return ttoks,tngms

print("==== Loaded. Getting Data.... =====")
ids = Loader.get_primaries(data['fics']);
vdata = []
vwords = Set([])
master = None

i=1;
for ident in ids:
   print(">> process "+str(ident)+" : # "+str(i))
   master=fic2text(ident,master)
   i+=1
   #qwords,qdata = fic2text(i)
   #vdata += qdata 
   #vwords.update(qwords)

import ujson
print("==== Writing to File ======")
fh = open( "model.bin", "wb" )
#pickle.dump(master, fh)
fh.write(ujson.dumps(master))
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
