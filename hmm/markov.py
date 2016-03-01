#!/usr/bin/python

import markovify
import argparse 
import random 

parser = argparse.ArgumentParser(description='Train data.')
parser.add_argument('command', metavar='cmd',
                   help='test or train')

def get_states(mdl,x):
  return filter(x,mdl.chain.model.keys())

def state_to_text((a,b,c)):
  t = a+" "+b+" "+c
  return t 


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
   print("=== Loading =====")
   fh = open('model.mkv','rb')
   text_model = markovify.Text.from_chain(fh.read())
   fh.close()
   
   print("=== Loaded =====")
  

   # Print five randomly-generated sentences
   for i in range(20):
       print(text_model.make_sentence())

   print("============")
   x = "cock"
   sts = get_states(text_model,lambda (w1,w2,w3) : w1 == x or w2 == x or w3 == x)
   ist = state_to_text(random.choice(sts))
   print(ist)
   # Print five randomly-generated sentences
   for i in range(20):
       print(ist+" "+text_model.make_sentence_with_start(ist))
   print("============")

   # Print three randomly-generated sentences of no more than 140 characters
   for i in range(3):
       print(text_model.make_short_sentence(140))