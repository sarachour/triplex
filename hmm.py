#!/usr/bin/python

import string
import argparse
import random
import unidecode
import re
import load as Loader 
import unicodedata
import hmm
from nltk.util import ngrams
import nltk
from textstat.textstat import textstat
from collections import Counter
import enchant
from enchant.checker import SpellChecker
from sets import Set
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import * 
import sklearn
import nltk.tag

NUM_GRAMS = 3
NUM_FICS = 50

parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data_partial(args.directory,NUM_FICS)

dictionary = enchant.Dict("en_US")
dictionary_br = enchant.Dict('en_GB')
spellcheck = SpellChecker('en_US')

print('The nltk version is {}.'.format(nltk.__version__))
print('The scikit-learn version is {}.'.format(sklearn.__version__))

nonalpha = re.compile('[^a-zA-Z]')
cleanline = re.compile('[\"\\\\,]')
whitespace= nltk.tokenize.RegexpTokenizer(r'\w+[*\w]+')
periods = re.compile("[\.?!]+[\s]*")
punc = re.compile("[,?!]")

fix = {
   "im":"i'm",
   "didn":"didn't",
   "doesn":"doesn't",
   "don'":"don't",
   "couldn":"couldn't",
   "hadn":"hadn't",
   "hasn":"hasn't",
   "isn":"isn't",
   "wasn":"wasn't",
   "weren":"weren't",
   "ve":"I've",
   "mustn":"mustn't",
   "wouldn":"wouldn't",
   "aren":"aren't",
   "shouldn":"shouldn't",
   "ain":"ain't"
}

slang = [
   "clit",
   "wanker",
   "cuppa",
   "twat",
   "arse",
   "wank",
   "ihome",
   "timeline",
   "barista",
   "arabica",
   "unfazed",
   "thrusted",
   "countertop",
   "stubbled",
   "tsk",
   "tsked",
   "combust",
   "arsehole",
   "jeggings",
   "blog",
   "playlist",
   "emoticon",
   "youngling",
   "younglings",
   "dwarflings",
   "dwarven",
   "showerhead",
   "hobbits",
   "orcs",
   "halflings",
   "mithril",
   "halfling",
   "dwarfling",
   "warg",
   "greybeards",
   "oliphant",
   "dwarfling"
]

for slangw in slang:
   dictionary.add(slangw)
   spellcheck.add(slangw)

def normalize(x):
   return nonalpha.sub("",x)

# templatize non-proper nouns
def split_punc(line):
   line = unidecode.unidecode(line)
   line = cleanline.sub('',line)
   pers = periods.split(line)
   allfrags = []
   for p in pers:
      if len(p) == 0:
         continue;

      firstword = p.split(' ')[0]
      if firstword == "":
         continue;

      if((dictionary.check(firstword) or dictionary_br.check(firstword)) and (not (firstword in state["templs"]))):
         p = p[0].lower()+p[1:]
      
      frags = punc.split(p)
      allfrags += frags
      
   return allfrags

def split_whitespace(x):
   toks = whitespace.tokenize(x)
   return toks 

state = {
   "templs":{
      "Harry":"@0",
      "Jim":"@1"
   },
   "freqs":{},
   "cnt":2
}
def reset_state():
   state["templs"] = {}
   state["cnt"] = 0

def repl_proper_noun(x):
   if x.lower() in fix:
      x = fix[x.lower()]

   

   if dictionary.check(x) or dictionary_br.check(x):
      return x
   else:
      if len(x) > 1 and x[0].isupper() and x[1].islower():
         if x in state["templs"]:
            return state["templs"][x]
         else:
            print("RESERVED",x)
            handle = "@"+str(state["cnt"])
            state["templs"][x] = handle
            state["cnt"]+=1
            return handle

      spellcheck.set_text(x)
      for error in spellcheck:
         for suggestion in error.suggest():
            if normalize(error.word) == normalize(suggestion):
               error.replace(suggestion)
               break

      y = spellcheck.get_text()
      if x == y:
         #print("new word",x)
         dictionary.add(x)
         return x
      else:
         #print("fixed",x,y)
         return y

def repl_proper_noun_ws(x):
   y = repl_proper_noun(x)
   ys = split_whitespace(y)
   if len(ys) == 1:
      return [ys[0].lower()]
   else:
      ys = map(lambda q: repl_proper_noun(q).lower(),ys)
      return ys

def clean_line(line):
      line = line.replace(u'\xa0',' ')
      #line = line.encode('ascii', 'ignore').decode('ascii')
      return line 

def clean_tokens(toks):
   ntoks = []
   for tok in toks:
      res = repl_proper_noun_ws(tok)
      ntoks += res
   return ntoks 

def fic2text(ident):
   textsegs = Loader.get_field(data['fics'],ident,'fic') 
   rtags = Loader.get_field(data['base'],ident,'tags')
   rtext = ""
   tngms = []
   ttoks = Set([])

   for line in textsegs:
      line = clean_line(line)
      frags = split_punc(line)
      for frag in frags:
         toks = split_whitespace(frag)
         toks = clean_tokens(toks)
         ttoks.update(toks)

         ngms = list(ngrams(toks,NUM_GRAMS,pad_right=False,pad_left=False))
         tngms += ngms


   #starting = model("t")
   #content = model.generate(10,starting)
   #print(" ".join(content))

   #tokens = nltk.word_tokenize(rtext)
   return ttoks,tngms

print("==== Loaded. Getting Data.... =====")
ids = Loader.get_primaries(data['fics']);
vdata = []
vwords = Set([])

for i in ids:
   print(">> ",i)
   qwords,qdata = fic2text(i)
   vdata += qdata 
   vwords.update(qwords)

print("===== Finished Processing Ngrams ===")
vstat = Counter(vdata)
for k in vstat:
   print(k,vstat[k])

nwords = len(vwords)
print("number of words:",nwords)

HiddenMarkovModelTagger(nwords,)
