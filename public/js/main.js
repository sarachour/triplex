
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

var add_page = function(){
  console.log("retrieved page");
}

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
    scraper.scrape(add_page);
  });
})

