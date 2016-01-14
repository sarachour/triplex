var express = require('express');
var cheerio = require('cheerio');
var request = require('request');
var fs = require('fs');
var app = express();
var router = express.Router();


router.route('/get')
   .get(function(req,res){
      console.log("> /get: GET request")
   })
   .post(function(req,res){
      var url = req.query.url; 
      console.log("> /get: POST request on data="+JSON.stringify(req.query));

      if(url){
         request(url, function(err,resp, body){
            if(err){
               console.log(">> failed to retrieve page");
            }
            var retobj = {body:body, response:resp, error:err}
            res.send(JSON.stringify(retobj));
         })
      }
      else {
         var retobj = {error:"ERROR: no url specified"}
         res.send(JSON.stringify(retobj))
      }
   })


app.listen('8081')
console.log('=== Server Started ===')
console.log('Web Interface: http://127.0.0.1:8081/site/')

app.use("/api", router)
app.use("/site", express.static('public'));
exports = module.exports = app;


