var delay = function(amt,cbk){
   console.log("setting timeout with delay:",amt)
   setTimeout(function(){
      cbk()
   },amt);
}

var Scraper = function(url,n){
   this.init = function(url,n){
      this.root = url;
      this.dummy = $("<div/>")
      this.npages = n;
      this.base_url = "http://www.archiveofourown.com";
      this.request_delay = 100;
      this.obs = new Observer();
   }
   this.event = function(){
      return this.obs;
   }

   this.get_page = function(url,proc,args){
      var that = this;
      console.log("request:", url)
      $.ajax({
         type: "POST",
         url: "/api/get?url="+encodeURIComponent(url),
         success:function(data){
            data = JSON.parse(data);
            if(data.error){
               console.log("ERROR",data.error)
            }
            else{
               that.data = data
               that.dom = jQuery.parseHTML(that.data.body);
               proc(that.dom,args);
            }
         }
      })
   }
   this.get_works = function(D){
      var that = this;
      var get_work_data = function(w){
         var data = {};
         //console.log(w);
         that.work = w;
         //get title
         data.title = $("a",$(".heading",w)).eq(0).html();
         //get url
         var url = $("a",$(".heading",w)).eq(0).attr("href")
         data.id = parseInt(url.split("/")[2]) 
         data.url = that.base_url+url
         //get author
         data.author = $("a",$(".heading",w)).eq(1).html()
         data.author_url = $("a",$(".heading",w)).eq(1).attr("href")
         //get date created 
         data.date = new Date(Date.parse($(".datetime",w).html()))
         data.fanfic = {
            body: null
         }
         //get fandoms
         //get warnings
         //get tags
         
         //get summary
         data.summary = $("p", $(".userstuff.summary",w)).html();

         //get stats
         var stats = {};
         var elem = $(".stats",w);
         stats.language = $("dd.language",elem).html();
         stats.words = parseInt($("dd.words",elem).html());
         stats.hits = parseInt($("dd.hits",elem).html());
         var chaps =  $("dd.chapters",elem).html(); 
         stats.chapters = {
            released: parseInt(chaps.split("/")[0]),
            total: parseInt(chaps.split("/")[1])
         }
         var tags = {}

         $("li",$(".tags",w)).each(function(i,t){
            var cls = $(t).attr("class")
            var vl = $(".tag",t).html();
            var url = $(".tag",t).attr("href");
            if(! (cls in tags)){
               tags[cls] = []
            }
            tags[cls].push({name:vl,url:url});
         })
         data.stats = stats;
         data.tags = tags;

         return data;
      }
      var works = {}
      $(".work",D).each(function(i,e){
         var d = get_work_data(e);         
         works[d.id] = d;
      })
      return works;
   }
   this.scrape_works = function(){
      var that = this 
      var state = {
         index: 0,
         n: 0
      }
      var complete = function(){
         console.log("==== Completed Crawl =====")
         that.obs.trigger("completed");
         that.save();
      }
      var scrape_body = function(body,args){
         console.log(">> Retreiving Fanfic ",args.id)
         state.index += 1;
         var summary = ""
         $(".userstuff.summary",body).each(function(i,e){
            summary += $(e).html();
         })

         var story = "";
         $(".userstuff.module",body).each(function(i,e){
            story += $(e).html();
         })

         if(state.index == state.n){
            complete();
         }
         that.works[args.id].fanfic = {
            story: story,
            summary:summary
         }

      }
      for(id in this.works){
         state.n += 1;
      }

      for(id in this.works){
         var d = this.works[id];
         var url = d.url;
         var url = url + "?view_adult=true&view_full_work=true";  
         delay(this.request_delay, 
            (function(id,url){
               return function(){ that.get_page(url, scrape_body, {id:id,url:url}); }
            })(id,url)
         )
      }
   }
   this.scrape_page = function(url,idx){
      var that = this;
      console.log("==== Crawling Page ", idx, "/", this.npages," ==== ");
      console.log(url);
      var proc_page = function(pg){
         var works = that.get_works(pg);
         for(id in works){
            that.works[id] = works[id]; 
         }
         var next = $("a",$(".next",pg)).attr("href");
         var next_url = that.base_url + next;
         delay(that.request_delay, function(){
            that.scrape_page(next_url, idx+1)
         })
      }
      if(idx >= this.npages){
         this.status = "works";
         this.scrape_works();
      }
      else {
         this.get_page(url, proc_page);
      }
   }

   this.scrape = function(){
      this.works = {};
      this.status = "index";
      this.scrape_page(this.root,0);
   }
   this.save = function(){
      var text = JSON.stringify(this.works);
      var blob = new Blob([text], {
          type: "text/plain;charset=utf-8;",
      });
      saveAs(blob, "porn.dat");
   }

   this.init(url,n);
}