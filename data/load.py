import json 
import os 
import sys
from datetime import datetime


def error(msg):
   print("ERROR:"+msg)
   sys.exit(1)

def add_el(data,k,x):
   if(k in data):
      data[k].append(x)
   else:
      error("key "+k+" does not exist.")

def load_file(st,file):
   add = lambda k,x : add_el(st,k,x)

   try:
      fh = open(file,'r')
      data = json.load(fh);
      
      url=data["url"]
      title=data["title"]
      summary=data["summary"]
      ident=data["id"]
      date=datetime.strptime(data["date"],"%Y-%m-%dT%H:%M:%S.%fZ")
      author=data["author"]

      stats=data["stats"]
      hits=int(stats["hits"])
      words=int(stats["words"])
      lang=stats["language"]


      add("id",ident)
      add("title",title)
      add("summary",summary)
      add("date",date)
      add("hits",hits)
      add("words",words)
      add("language",lang)
      add("author",author)
   
   except Exception:
      print("skipping: "+file)

   return data

def mktable(args):
   tbl = {};
   for arg in args:
      tbl[arg] = []

   return tbl

def load_data(rootdir):
   direc = rootdir + "/works"
   meta = mktable([
      "id",
      "url",
      "title",
      "summary",
      "date",
      "hits",
      "words",
      "language",
      "author"
   ])
   for filename in os.listdir(direc):
      path = direc + "/" + filename 
      print(path)
      load_file(meta,path)