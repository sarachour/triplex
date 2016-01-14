var Scraper = function(url,n){
   this.init = function(url,n){
      this.root = url;
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
            }
         }
      })
   }
   this.scrape_page = function(url){
      var proc_page = function(pg){
         console.log(pg);

      }
      this.get_page(url, proc_page);
   }

   this.scrape = function(){
      this.scrape_page(this.root);
   }

   this.init(url,n);
}