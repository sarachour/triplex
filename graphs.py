#!/usr/bin/python

import argparse
import load as Loader 
import analyze as Analyzer


parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data(args.directory)

print("==== Loaded Data =====")
Analyzer.histogram("hits.png", 
   data["base"]["hits"], 25,
   "Histogram of Number of Hits","Number of Hits")

Analyzer.histogram("words.png", 
   data["base"]["words"], 25,
   "Histogram of Number of Words","Number of Words")

Analyzer.scatter("hits-vs-words.png",
   data["base"]["words"],data["base"]["hits"], 
   "Histogram of Hits vs Words","Number of Words", "Number of Hits")

Analyzer.scatter("bookmarks-vs-words.png",
   data["base"]["words"],data["base"]["bookmarks"], 
   "Histogram of Bookmarks vs Words","Number of Words", "Number of Bookmarks")

Analyzer.scatter("kudos-vs-words.png",
   data["base"]["words"],data["base"]["kudos"], 
   "Histogram of Kudos vs Words","Number of Words", "Number of Kudos")

Analyzer.scatter("kudos-vs-words.png",
   data["base"]["words"],data["base"]["comments"], 
   "Histogram of Comments vs Words","Number of Words", "Number of Comments")



