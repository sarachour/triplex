#!/usr/bin/python

import marshal

fh = open( "model.bin", "rb" )
model = marshal.load(fh)

NUM_GRAMS = 2

print("===== Generate HMMs ===")

for i in range(0,50):
   print(markov.generate_from(model, "<start>",20, NUM_GRAMS)) # 2 is the ply, 10 is the length

