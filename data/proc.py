#!/usr/bin/python

import argparse
import load as Loader 

parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data(args.directory)
print("==== Loaded Data =====")
print(data)



