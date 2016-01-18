
var RequestQueue = function (delay){
   this.get_page = function(url,proc,args){
      var that = this;
      console.log("url",url)
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
   this.deq = function(){
      if(this.queue.length > 0){
         var el = this.queue[0];
         this.queue.shift();
         this.get_page(el.url, el.cbk, el.args);
         this.obs.trigger("get",{url:el.url,args:el.args});

      }
      else  {
         clearInterval(this.timer);
         this.timer = null;
         this.obs.trigger("idle");
      }
   }

   this.init = function(delay){
      var that = this;
      this.delay = delay;
      this.obs = new Observer();
      this.queue = [];
   }
   
   this.resume = function(){
      if(this.timer != null){
         return;
      }
      var that = this;
      this.timer = setInterval(function(){
         that.deq();
      },this.delay);
   }

   this.enq = function(url, proc, args){
      var el = {url:url, cbk:proc, args:args}
      this.obs.trigger("enq",{url:el.url,args:el.args});
      this.queue.push(el);
      this.resume();
   }
   this.init(delay);

}

var Scraper = function(url,n){
   this.init = function(url,n){
      this.root = url;
      this.dummy = $("<div/>")
      this.npages = n;
      this.base_url = "http://www.archiveofourown.com";
      this.obs = new Observer();
      this.queue = new RequestQueue(10);
      this.paused = false;
      this.works = {};
      this.curr_url = null;
      this.curr_idx = -1;

      var that = this;
      this.queue.obs.listen("idle", function(){
         that.obs.trigger("idle");
         if(that.isCompleted()){
            that.obs.trigger("complete");
         }
      })
      this.queue.obs.listen("get", function(args){
         that.obs.trigger("get",args.url)
      })
   }

   this.event = function(){
      return this.obs;
   }
   
   this.scrape_work = function(id){
      var that = this 

      var scrape_body = function(body,args){
         var summary = ""
         $(".userstuff.summary",body).each(function(i,e){
            summary += $(e).html();
         })

         var story = "";
         $(".userstuff.module",body).each(function(i,e){
            story += $(e).html();
         })

         console.log("> Received Work "+id);
         that.obs.trigger("work",id);

         that.works[args.id].fanfic = {
            story: story,
            summary:summary
         }

      }

      var d = this.works[id];
      var url = d.url;
      var url = url + "?view_adult=true&view_full_work=true";  
      console.log("enq:",url)
      this.queue.enq(url, scrape_body, {id:id,url:url}); 

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
         var ifndef0 = function(e){
            if(e == undefined){
               return 0;
            }
            else{
               return parseInt(e);
            }
         }
         stats.language = $("dd.language",elem).html();
         stats.words = ifndef0($("dd.words",elem).html());
         stats.hits = ifndef0($("dd.hits",elem).html());
         stats.kudos =  ifndef0($("a",$("dd.kudos",elem)).html()); 
         stats.bookmarks = ifndef0($("a",$("dd.bookmarks",elem)).html());
         stats.comments =  ifndef0($("a",$("dd.comments",elem)).html());  


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
      $(".work",D).each(function(i,e){
         var d = get_work_data(e);   
         that.works[d.id] = d;
         that.scrape_work(d.id);      
      })
   }

   this.scrape_page = function(url,idx){
      var that = this;
      console.log("==== Crawling Page ", idx, "/", this.npages," ==== ");
      console.log(url);
      this.curr_url = url;
      this.curr_idx = idx;
      that.obs.trigger("page",{idx:idx,url:url})
      
      var proc_page = function(pg){
         that.get_works(pg);

         var next = $("a",$(".next",pg)).attr("href");
         var next_url = that.base_url + next;
         that.scrape_page(next_url, idx+1)
      }

      if(idx < this.npages) {
         if(that.paused == false){
            this.queue.enq(url, proc_page, {});
         }
      }
   }
   this.getNWorks = function(){
      var i =0; 
      for(id in this.works){
         i+=1;
      }
      return i;
   }
   this.clearWorks = function(){
      this.works = {};
   }

   this.isCompleted = function(){
      return (this.curr_idx >= this.npages);
   }
   this.isPaused = function(){
      return this.paused;
   }
   this.pause = function(){
      this.paused = true;
   }

   this.resume = function(){
      this.paused = false;
      if(this.curr_url != null){
         this.scrape_page(this.curr_url, this.curr_idx);
      }
   } 

   this.scrape = function(){
      this.scrape_page(this.root,0);
   }
   

   this.init(url,n);
}