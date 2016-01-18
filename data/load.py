import json 
import os 
import sys
from datetime import datetime

glbl = {
   "base": {},
   "tags": {},
   "cats": {},
   "fics": {}
}
def error(msg):
   print("ERROR:"+msg)
   sys.exit(1)

def add_el(data,k,x,force):
   if(k in data):
      data[k].append(x)
   elif(force):
      data[k] = []
      data[k].append(x)
   else:
      error("key "+k+" does not exist.")

def load_file(file):
   addb = lambda k,x : add_el(glbl["base"],k,x,False)
   addt = lambda c,k,x : add_el(glbl["tags"][c],k,x,False)
   addf = lambda k,x : add_el(glbl["fics"],k,x,False) 

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
      bookmarks = int(stats["bookmarks"])
      kudos = int(stats["kudos"])
      comments = int(stats["comments"])

      tags=data["tags"]

      story = data["fanfic"]["story"]
      stsummary = data["fanfic"]["summary"]

      addb("id",ident)
      addb("title",title)
      addb("summary",summary)
      addb("date",date)
      addb("hits",hits)
      addb("words",words)
      addb("language",lang)
      addb("author",author)
      addb("bookmarks",bookmarks)
      addb("comments",comments)

      addf("id",ident)
      addf("summary",stsummary)
      addf("fic",story)

      for cat in tags:
         addt(cat,"id",ident)
         tgs = tags[cat]
         for tag in tgs:
            tname = tag["name"]

            if((tname in glbl["tags"][cat]) == False):
               nprec = len(glbl["tags"][cat]["id"]) - 1 
               glbl["tags"][cat][tname] = [False]*nprec

            addt(cat,tname,True)


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
   glbl["base"] = mktable([
      "id",
      "url",
      "title",
      "summary",
      "date",
      "hits",
      "words",
      "language",
      "bookmarks",
      "kudos",
      "comments",
      "author"
   ])
   glbl["tags"] = {}
   glbl["tags"]["freeforms"] = mktable(["id"])
   glbl["tags"]["relationships"] = mktable(["id"])
   glbl["tags"]["characters"] = mktable(["id"])
   glbl["tags"]["warnings"] = mktable(["id"])
   glbl["fics"] = mktable(["id","fic","summary"])
   
   for filename in os.listdir(direc):
      path = direc + "/" + filename 
      print(path)
      load_file(path)

   return glbl
