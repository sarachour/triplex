#!/usr/bin/python

import enchant
from enchant.checker import SpellChecker


dictionary = enchant.DictWithPWL("en_US","slang.txt")
dictionary_br = enchant.Dict('en_GB')
spellcheck = SpellChecker('en_US')


def defined_in_dict(x):
   if dictionary.check(x.lower()) or dictionary_br.check(x.lower()):
      return True
   else: 
      return False