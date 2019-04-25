var get_json_data = (function() {
  var jsdata;

  return function(newdat) {
    if(newdat){
      jsdata = JSON.parse(newdat);
    }
    return jsdata;
  }
} ());
