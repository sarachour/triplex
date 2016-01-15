var Scraper = function(url,n){
   this.init = function(url,n){
      this.root = url;
      this.dummy = $("<div/>")
      this.npages = n;
   }

   this.get_page = function(url,proc){
      var suffix = "?view_adult=true&view_full_work=true"; 
      var full_url = url + suffix;
      var that = this;

      console.log("request:", data)
      $.ajax({
         type: "POST",
         url: "/api/get?url="+full_url,
         success:function(data){
            data = JSON.parse(data);
            if(data.error){
               console.log("ERROR",data.error)
            }
            else{
               that.data = data
               that.dom = jQuery.parseHTML(that.data.body);
               proc(that.dom);
            }
         }
      })
   }
   this.get_works = function(D){
      var get_work_data = function(w){
         var data = {};
         //get title
         data.title = $("a",$(".heading",w)).html();
         //get url
         var url = $("a",$(".heading",w)).attr("href")
         data.id = url 
         data.url = "http://www.archiveofourown.com"+url
         //get author
         data.author = $("a",$("[rel=author]",w)).html()
         data.author_url = $("a",$("[rel=author]",w)).attr("href")
         //get date created 
         data.date = $(".datetime",w).html()
         //get fandoms
         //get warnings
         //get tags
         
         //get summary
         data.summary = $("p", $(".userstuff.summary",w)).html();

         //get stats
         var stats = {};
         var elem = $(".stats",w);
         stats.language = $("dd.language",elem).html();
         stats.words = $("dd.words",elem).html();
         stats.hits = $("dd.hits",elem).html();
         stats.chapters = $("dd.chapters",elem).html();
         data.stats = stats;

         return data;
      }
      var works = []
      $(".work",D).each(function(i,e){
         var d = get_work_data(d);
         console.log(d);
         works.push(d);
      })
      return works;
   }
   this.scrape_page = function(url){
      var that = this;
      var proc_page = function(pg){
         var works = that.get_works(pg);
         //var next_url = this.get_next_url(pg);
         //var works = this.fill_works(pg);


      }
      this.get_page(url, proc_page);
   }

   this.scrape = function(){
      this.scrape_page(this.root);
   }

   this.init(url,n);
}