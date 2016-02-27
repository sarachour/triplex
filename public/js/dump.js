
var Dumper = function(){
   this.init = function(){

   }  
   this.save = function(type,filename,text){
      var blob = new Blob([text], {
          type: type+";charset=utf-8;",
      });
      saveAs(blob, filename);
   }

   this.saveJSON = function(filename,data){
      var text = JSON.stringify(data);
      this.save("application/json",filename,text);
   }

   this.saveZip = function(filename,data, tofile){
      var zip = new JSZip();
      tofile(this,zip,data);
      var cntnt = zip.generate({type:"blob"})
      saveAs(cntnt, filename)
   }

   this.init();

}