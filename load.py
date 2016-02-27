import json 
import os 
import sys
from datetime import datetime
import copy 

glbl = {
   "base": {},
   "tags": {},
   "cats": {},
   "fics": {}
}
def error(msg):
   print("ERROR:"+msg)
   sys.exit(1)

def add_el(d,primary,k,x,force):
   if(not (primary in d["data"])):
      d["data"][primary] = copy.copy(d["default"])

   if(k in d["keys"]):
      d["data"][primary][k] = x
   else:
      error("key "+k+" does not exist.")

def get_row(tbl,i):
   return tbl["data"][i]

def get_field(tbl,i,k):
   return tbl["data"][i][k]

def get_fields(tbl):
   return tbl["keys"]

def get_primaries(tbl):
   return tbl["data"].keys()
   
def load_file(fname):
   
   fh = open(fname,'r')
   data = json.load(fh,encoding="utf-8");


   url=data["url"]
   title=data["title"]

   if("summary" in data):
      summary=data["summary"]
   else:
      summary=""

   ident=data["id"]
   date=datetime.strptime(data["date"],"%Y-%m-%dT%H:%M:%S.%fZ")
   author=data["author"]
   

   addb = lambda k,x : add_el(glbl["base"],ident,k,x,False)
   addt = lambda c,k,x : add_el(glbl["tags"][c],ident,k,x,False)
   addf = lambda k,x : add_el(glbl["fics"],ident,k,x,False) 


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

   addb("title",title)
   addb("summary",summary)
   addb("date",date)
   addb("hits",hits)
   addb("words",words)
   addb("language",lang)
   addb("kudos",kudos)
   addb("author",author)
   addb("bookmarks",bookmarks)
   addb("comments",comments)
   addb('tags',tags)

   addf("id",ident)
   addf("summary",stsummary)
   addf("fic",story)

   commentout = '''
   for cat in tags:
      addt(cat,"id",ident)
      tgs = tags[cat]
      for tag in tgs:
         tname = tag["name"]

         if((tname in glbl["tags"][cat]) == False):
            nprec = len(glbl["tags"][cat]["id"]) - 1 
            glbl["tags"][cat][tname] = [False]*nprec

         addt(cat,tname,True)
   '''




def mktable(args,pid):
   tbl = {};
   tbl["primary"] = pid 
   tbl["default"] = {} 
   tbl["data"] = {}
   tbl["keys"] = args

   for arg in args:
      tbl["default"][arg] = None

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

def load_data_partial(rootdir,n):
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
      "tags",
      "author"
   ],"id")
   glbl["tags"] = {}
   glbl["tags"]["freeforms"] = mktable(["id"],"id")
   glbl["tags"]["relationships"] = mktable(["id"],"id")
   glbl["tags"]["characters"] = mktable(["id"],"id")
   glbl["tags"]["warnings"] = mktable(["id"],"id")
   glbl["fics"] = mktable(["id","fic","summary"],"id")

   i = 0
   
   for filename in os.listdir(direc):
      path = direc + "/" + filename 
      print(path)
      load_file(path)
      i += 1 
      if i >= n:
            return glbl;

   return glbl
