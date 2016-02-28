#!/usr/bin/python

import ujson
import hmm_model as markov

fh = open( "model.bin", "rb" )
smodel = ujson.loads(fh.read())

model = {}
for k in smodel:
   q = {}
   for i in smodel[k]:
      q[eval(i)] = smodel[k][i]

   model[int(k)] = q

print(model)
NUM_GRAMS = 4
LENGTH = 10
print("===== Generate HMMs ===")

for i in range(0,50):
   print(markov.generate_from(model,"<start>",LENGTH, NUM_GRAMS)) # 2 is the ply, 10 is the length

