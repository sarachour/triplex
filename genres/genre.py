import string
import argparse
import random
import unidecode
import re

import load as Loader 

## determine which genres are most common, least common
NUM_FICS = 50

parser = argparse.ArgumentParser(description='Analyze scraped data.')
parser.add_argument('directory', metavar='dir',
                   help='directory to process')

args = parser.parse_args()
data = Loader.load_data_partial(args.directory,NUM_FICS)



## determine which genres are corralated


## determine the most popular genres