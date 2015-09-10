var express = require('express');
var cheerio = require('cheerio');
var request = require('request');
var fs = require('fs');
var app = express();
var router = express.Router();

var Dumper = function(){
   this.write_metadata = function(entry){
      var str = JSON.stringify(entry)+"\n";
      fs.appendFile('data/db.dat', str, function(err){

      })
   }
   this.write_fic = function(id, data){
      fs.writeFile('data/fics/'+id+'.txt', data, function (err) {
        if (err) return console.log(err);
        console.log('   > wrote '+id);
      });
   }
}
var Scraper = function(){


   this.get_results = function(url,cbk){
       
      var results_from_page = function(accessor){
         var $ = accessor;

         var next_page = function(){
            var nextbutton = $("a",$(".next"));
            var nurl = nextbutton.attr("href");
            return nurl;
         }

         var clean = function(str){
            return str.split("\"")[1];
         }
         var get_tag_list = function(sel, rt){
            var tgs = $(sel,$(rt));
            var tglst = $(".tag",tgs);

            var dat = [];
            tglst.each(function(i,v){
               var tg = $(v).text();
               if(tg == "null" || tg == null || tg == undefined){
                  return;
               }
               dat.push(clean(JSON.stringify(tg)))
            });
            return dat;
         }

         var works = [];
         console.log("-> getting works");
         $(".work").each(function(){
            var root = this;
            var entry = {};
            var nm = $("a",$(".header",$(root)));
            entry.name = nm.text();
            entry.url = nm.attr('href');
            entry.id = entry.url.split("/")[entry.url.split("/").length - 1];
            entry.rating = $(".rating", $(root)).html();
            entry.warnings = get_tag_list(".warnings",root);
            entry.relationships = get_tag_list(".relationships",root);
            entry.characters = get_tag_list(".characters",root);
            entry.freeforms = get_tag_list(".freeforms",root);
            entry.fandoms = get_tag_list(".fandoms",root);
            works.push(entry);
         });
         console.log("-> getting next page");
         var nurl = next_page();
         cbk(works,nurl);
      }
      
      if(url == undefined){
         return;
      }
      var that = this;
      request(url, function(err,resp,body){
         if(err){
            console.log("failed to retrieve page");
            return;
         }
         that.search_page = cheerio.load(body);
         results_from_page(that.search_page);

      })
   }

   this.get_fic = function(partial, cbk){
      var fic_from_page = function(acc){
          var $ = acc;
          var data = $(".userstuff");
          var text = "";
          data.each(function(i,e){
            var str = $(e).text();
            text += str;
          })
          cbk(text);
      }
      var url = "http://www.archiveofourown.org"+partial+"?view_adult=true&view_full_work=true";
      var that = this;
      request(url, function(err,resp,body){
         if(err){
            console.log("failed to retrieve page");
            return;
         }
         that.search_page = cheerio.load(body);
         fic_from_page(that.search_page);
      });
   }
}


var scraper = new Scraper();
var dumper = new Dumper();
FIC_DELAY = 500;
router.route('/scrape')
   .get(function(req,res){
      console.log("# get scraping")
   })
   .post(function(req,res){
      console.log("# post scraping");
      if(req.query.url){
         var url = req.query.url;
         var npages = req.query.npages;
         if(url == undefined || npages == undefined){
            res.end("failed: need url and npages entry.")
         }
         console.log("get url", url,"/npages",npages)

         var max_idx = parseInt(npages);
         var scrape_page = function(idx, url){
            if(idx >= max_idx) return;
            console.log(":: entries / ",url)
            scraper.get_results(url, function(works, nurl){
               //write to file
               var nworks = works.length;

               works.forEach(function(e,i){
                  dumper.write_metadata(e);
                  
                  var ficurl = e.url;
                  var ficid = e.id;

                  setTimeout(function(){
                     scraper.get_fic(ficurl, function(data){
                        dumper.write_fic(ficid, data);
                        if(i == nworks-1){
                           scrape_page(idx+1, "http://www.archiveofourown.org"+nurl);
                        }
                     });
                  }, i*FIC_DELAY)
                  
               })
            });
         }



         scrape_page(0,url);
      }
   })


app.listen('8081')
console.log('Magic happens on port 8081')

app.use("/api", router)
exports = module.exports = app;


