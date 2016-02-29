#!/usr/bin/python

import markovify
import argparse 

parser = argparse.ArgumentParser(description='Train data.')
parser.add_argument('command', metavar='cmd',
                   help='test or train')

args = parser.parse_args()

cmd = args.command 

if cmd == "train":
   # Get raw text as string.
   with open("out.txt") as f:
       text = f.read()

   # Build the model.
   text_model = markovify.Text(text,state_size=3)

   fh = open('model.mkv','wb')
   fh.write(text_model.chain.to_json())
   fh.close()

else:
   fh = open('model.mkv','rb')
   text_model = markovify.Text.from_chain(fh.read())
   fh.close()
   # Print five randomly-generated sentences
   for i in range(20):
       print(text_model.make_sentence())

   print("============")
   # Print five randomly-generated sentences
   for i in range(20):
       print(text_model.make_sentence_with_start("His"))
   print("============")

   # Print three randomly-generated sentences of no more than 140 characters
   for i in range(3):
       print(text_model.make_short_sentence(140))