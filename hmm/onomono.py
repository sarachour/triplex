import re

onomonopia = []

def add_sfx(regex,name):
   e = {
      "regex":re.compile(regex+"$"),
      "term":name
   }
   onomonopia.append(e)

def recog_sfx(word):
   lw = word.lower()
   for sfx in onomonopia:
      if sfx["regex"].match(lw):
         return True,sfx["term"]

   return False,lw
   
add_sfx("h[ha]+?","haha")
add_sfx("a[ha]+","ahaha")
add_sfx("fu+ck","fuck")
add_sfx("shi+t","shit")
add_sfx("mm+","mmm")
add_sfx("ss*h+","shh")
add_sfx("aw+","aww")
add_sfx("soo+","soo")
add_sfx("aa+h","aah")
add_sfx("hn+","hnn")
add_sfx("ow+","oww")
add_sfx("(ow)+","owow")
add_sfx("o+","oo")
add_sfx("haa+","haa")
add_sfx("(bu?z+)+","buzz")
add_sfx("(ew+)+","eww")
add_sfx("y+e+s+","yes")
add_sfx("ho+nk","honk")
add_sfx("boo+p","boop")