var Observer = function(){
   this.init = function(){
      this.events = {};
   }
   this.unbind = function(name,h){
      this.events[name].remove(h);
   }
   this.listen = function(name,c){
      if(!this.events[name]){
         this.events[name] = [];
      }
      var i = this.events[name].length();
      this.events[name].push(c);
      return i;
   }
   this.trigger = function(name){
      if(this.events[name]){
         this.events[name].each(function(i,e){
            e();
         })
      }
   }
   this.init();
}