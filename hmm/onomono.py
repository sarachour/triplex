import re

onomonopia = []

def add_sfx(regex,name):
   e = {
      "regex":re.compile(regex),
      "term":name
   }
   onomonopia.append(e)

def recog_sfx(word):
   lw = word.lower()
   for sfx in onomonopia:
      if sfx["regex"].match(lw):
         print("sfx:",lw)
         return sfx["term"]

   return lw
   
add_sfx("(ha)+","haha")
add_sfx("a(ha)+","ahaha")
add_sfx("fu+ck","fuck")
add_sfx("shi+t","shit")
add_sfx("mm+","mmm")
add_sfx("ss*h+","shh")