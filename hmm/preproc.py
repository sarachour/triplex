#!/usr/bin/python

import string
import argparse
import random
import unidecode
import re

import load as Loader 
from dictionaries import *
import onomono

from propernoun import *
from onomono import *
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

import ujson

#import hmm_model as markov


#NUM_GRAMS = 5
#MIN_PHRASE = 7
NUM_FICS = 10
OUTFILE="out.txt"

parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data_partial(args.directory,NUM_FICS)



print('The nltk version is {}.'.format(nltk.__version__))
print('The scikit-learn version is {}.'.format(sklearn.__version__))


def clean_line(line):
      cleanline = re.compile('[\\\\]')
      line = unidecode.unidecode(line)
      line = cleanline.sub('',line)
      return line 


def proc_line(line):
   #
   whitespace = re.compile("[\s]+")
   punc_pfx = re.compile("^[^A-Za-z]+")
   punc_sfx = re.compile("[^A-Za-z]+$")
   alpha = re.compile("[A-Za-z]+((-|')[A-Za-z])?[A-Za-z]*")
   hyphen = re.compile("[-]+")
   poss = re.compile("'s")
   tokens = whitespace.split(line)
   nline = ""
   for tok in tokens:
      if len(tok) == 0:
         continue;

      pfx = punc_pfx.search(tok)
      sfx = punc_sfx.search(tok)
      word = alpha.match(tok)
      suff = ""
      pref = ""

      if word == None:
         nline += tok + " "
         continue;

      word = word.group(0)

      if pfx != None:
         pref = pfx.group(0)

      if sfx != None: 
         suff = sfx.group(0)

      if "'s" in word:
         suff = "'s" + suff
         word = poss.split(word)[0]

      success,sfx = recog_sfx(word)

      if success:
         nline += pref+sfx+suff 
         continue;

      if "-" in word:
         if is_proper_noun(word) and is_template(word):
               nname = get_template(word);
               nline += pref+nname+suff+" "
               continue;

         subwords = hyphen.split(word)
         all_words = True 
         for subword in subwords:
            if defined_in_dict(subword) == False:
               all_words = False

         if all_words == True:
            nline += pref + word.lower() + suff + " ";
         else:
            if is_proper_noun(word) and not is_template(word):
               nname = add_template(word)
               nline += pref+nname+suff+" "

            elif is_proper_noun(word) and is_template(word):
               nname = get_template(word);
               nline += pref+nname+suff+" "

            else:
               nline += pref+ word + suff+" "


      else:
         if is_proper_noun(word) and is_template(word):
               nname = get_template(word);
               nline += pref+nname+suff+" "
               continue;

         if defined_in_dict(word):
            nline += tok + " "
         else:
            if is_proper_noun(word) and not is_template(word):
               nname = add_template(word)
               nline += pref+nname+suff+" "

            elif is_proper_noun(word) and is_template(word):
               nname = get_template(word);
               nline += pref+nname+suff+" "

            else:
               print("unknown",pref,word,suff)
               nline += pref+ word + suff+" "

   return nline;

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
      line = proc_line(line)
      rtext += line


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
print("==== Writing to File ======")
dump_template("names.templ")
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
