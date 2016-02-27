import nltk 

parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data(args.directory)

# lower case words
words
freq_words = nltk.FreqDist(words)
# feature vector
features = list(freq_words)[:5000]

def doc2feature(doc):
   words = set(json2words(doc))
   features = {}
   for feat in features:
         feature['contains({})'.format(feat)] = (feat in words)
   return features 

def json2data(j):
   text = j.text
   genres = j.tags
   feats = doc2feature(text)






def fic2text(data):
   textsegs = data;
   rtext = ""

   for line in textsegs:
      line = unicodedata.normalize("NFKD", line)
      rtext += line+"\n"

   print(rtext)
   tokens = nltk.word_tokenize(rtext)
   text = nltk.Text(tokens)
   return text

ids =Loader.get_primaries(data["fics"])
fid = random.choice(ids) 

meta = Loader.get_row(data["base"],fid)
story = Loader.get_row(data["fics"],fid)
print(meta)
print("Fiction",meta["title"]);
text = fic2text(story["fic"])
fdist = FreqDist(text)
print(fdist.most_common(100))