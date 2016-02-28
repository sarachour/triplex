#!/usr/bin/python

import enchant
from enchant.checker import SpellChecker

dictionary = enchant.Dict("en_US")
dictionary_br = enchant.Dict('en_GB')
spellcheck = SpellChecker('en_US')

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
   "dwarfling",
   "blowjob",
   "uhh",
   "uh",
   "eh",
   "oh",
   "hii",
   "hi",
   "oof",
   "haha",
   "muuh",
   "ooh",
   "oooh",
   "wassup",
   "wazzup",
   "uhh",
   "uuum",
   "uugh",
   "ugh",
   "uuugh",
   "uunh",
   "unh",
   "uuunh",
   "alrighty",
   "pff",
   "okaay",
   "cuz",
   "mmm",
   "mm",
   "argh",
   "aargh",
   "asshole",
   "sh",
   "shh",
   "shhh",
   "feelin",
   "lookin",
   "righty",
   "ahh",
   "aah",
   "ish",
   "mmhmm",
   "mmmhmm",
   "idk",
   "everything'll",
   "kickass",
   "naw"
]

for slangw in slang:
   dictionary.add(slangw)
   spellcheck.add(slangw)

def defined_in_dict(x):
   if dictionary.check(x.lower()) or dictionary_br.check(x.lower()):
      return True
   else: 
      return False