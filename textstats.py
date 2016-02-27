#!/usr/bin/python

import string
import argparse
import random
import re
import load as Loader 
import unicodedata
import nltk
from textstat.textstat import textstat

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import * 


parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data_partial(args.directory,10)

#nltk.download()
def fic2text(ident):
   textsegs = Loader.get_field(data['fics'],ident,'fic') 
   rtags = Loader.get_field(data['base'],ident,'tags')
   rtext = ""

   for line in textsegs:
      line = line.replace(u'\xa0',' ')
      s = re.sub('([.,!?()])', r' \1 ', line)
      s = re.sub('\s{2,}', ' ', line)
      line = line.encode('ascii', 'ignore').decode('ascii')
      rtext += line+" "

   tags = []
   for genre in rtags:
      for el in rtags[genre]:
         tname = el["name"]
         tags.append(tname)

   reading_ease =  textstat.flesch_reading_ease(rtext)
   reading_level = textstat.flesch_kincaid_grade(rtext)
   print(ident,reading_ease,reading_level)
   #tokens = nltk.word_tokenize(rtext)
   return tags,rtext

print("==== Loaded. Getting Data.... =====")
ids = Loader.get_primaries(data['fics']);
vdata = []
vtags = []
for i in ids:
   tags,arr = fic2text(i)
   vdata.append(arr)
   vtags.append(tags)

print("==== TFIDF Vectorize.... =====")
tf_vectorize = TfidfVectorizer(use_idf=True)
tfidf = tf_vectorize.fit_transform(vdata)
idf = tf_vectorize.idf_

# these are the words that we use for classification
vects = dict(zip(tf_vectorize.get_feature_names(),idf))

print("==== Predict Topics.... =====")
ctags = MultiLabelBinarizer().fit_transform(vtags)
clf = MultinomialNB().fit(tfidf, twenty_train.target)
