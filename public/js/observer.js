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
      var i = this.events[name].length;
      this.events[name].push(c);
      return i;
   }
   this.trigger = function(name,args){
      if(this.events[name]){
         this.events[name].forEach(function(e,i){
            e(args);
         })
      }
   }
   this.init();
}