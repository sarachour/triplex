var Debugger = function(id,max){
  this.init = function(id,max){
    this.id = id;
    this.n = 0;
    this.max = max;
  }
  this.append = function(div){
    if(this.n > this.max){
      $("div",this.id).last().remove();
      this.n-=1;
    }
    $(this.id).prepend(div);
    this.n += 1;
  }

  this.add_resume = function(){
    var div = $("<div/>");
    div.html("cmd: resume").addClass("cmd");;
    this.append(div);
  }
  this.add_pause = function(){
    var div = $("<div/>");
    div.html("cmd: pause").addClass("cmd");;
    this.append(div);
  }
  this.add_get = function(url){
    var div = $("<div/>");
    div.html("queue: get "+url).addClass("queue");
    //this.append(div);
  }
  this.add_idle = function(){
    var div = $("<div/>");
    div.html("queue: idle").addClass("queue");
    //this.append(div);
  }
  this.add_save = function(){
    var div = $("<div/>");
    div.html("cmd: save").addClass("cmd");
    this.append(div);
  }
  this.add_completed = function(){
    var div = $("<div/>");
    div.html("notify: completed").addClass("notify");
    this.append(div);
  }
  this.add_page = function(idx,page){
    var div = $("<div/>");
    div.html("notify: page "+idx).addClass("notify");
    this.append(div);
  }
  this.add_work = function(id){
    var div = $("<div/>");
    div.html("notify: work "+id+" processed").addClass("notify");
    //this.append(div);
  }
  this.clear = function(){
    $(this.id).empty();
  }
  this.init(id,max);
}

var debug = new Debugger("#debug",50)

data = {
   npages : 0,
   url : ""
}

scraper = null;

var update_npages = function(){
    val = $("#npages").val()
    $("#npages-label").html(val)
    data.npages=parseInt(val)
}

var update_url = function(){
  text = $("#url").val();
  console.log("url",text)
  data.url = text
}
var update_paused = function(){
  if(scraper != null){
    if(scraper.isPaused){
      $("#pause").html("Continue")
    }
    else{
      $("#pause").html("Pause")
    }
  }
}
var toggle_paused = function(){
  if(scraper != null){
    if(scraper.isPaused()){
      scraper.resume();
      debug.add_resume();
    }
    else{
      scraper.pause();
      debug.add_pause();
    }
  }
}

var add_page = function(){
  console.log("retrieved page");
}

var dumper = new Dumper();

$(document).ready(function(){
  $("#url").change(function(){
    update_url();
  })
  $("#npages").mousemove(function(){
    update_npages();
  })

  update_npages();
  update_url();

  $("#scrape").click(function(){
    scraper = new Scraper(data.url, data.npages);
    scraper.event().listen("idle", function(){
      debug.add_idle();
    })
    scraper.event().listen("get", function(url){
      debug.add_get(url);
    })
    scraper.event().listen("complete", function(url){
      debug.add_completed();
    })
    scraper.event().listen("page", function(data){
      debug.add_page(data.idx,data.url);
    })
    scraper.event().listen("work", function(id){
      debug.add_work(id);
      dumper.saveJSON(id+".json", scraper.works[id])
      scraper.works[id] = undefined;
    })
    scraper.scrape(add_page);
  });
  $("#pause").click(function(){
    toggle_paused();
    update_paused();
  })
  $("#dump").click(function(){
    if(scraper == null) return;
    var n = scraper.getNWorks();
    if(n > 1000){
      var n = Math.round(n/1000)+"K"
    }

    var meta = {
      query: data,
      curr_url: scraper.curr_url,
      curr_idx: scraper.curr_idx,
      n: n
    }
    dumper.saveJSON("query.json", meta);
    /*
    for(id in scraper.works){
      dumper.saveJSON(id+".json", scraper.works[id])
    }
    */

    
    /*
    dumper.saveZip("porn"+n+".zip", scraper.works, function(that,zfile,dat){
      zfile.file("query.json", JSON.stringify(meta));
      zfile.folder("works");
      for(id in dat){
        zfile.file("works/"+id+".json", JSON.stringify(dat[id]))
      }
    })
    */
    

  })
  $("#clear").click(function(){
    debug.clear();
    if(scraper != null) scraper.clearWorks();
  })
  update_paused();
})

