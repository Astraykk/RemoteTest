var get_json_data = (function() {
  //use hard-coded json data during offline debug
  var jsdata = JSON.parse('{"dat": [{"name": "clk", "width": "1", "wave": ["0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1"], "state": [10, 14, 11, 14, 11, 14, 11, 14, 11, 14, 11, 14, 11, 14], "time": ["0", "10000", "20000", "30000", "40000", "50000", "60000", "70000", "80000", "85000", "87500", "90000", "100000", "110000"]}, {"name": "ai[1:0]", "width": "2", "wave": ["0", "zz", "11", "xx"], "state": [18, 17, 17, 17], "time": ["0", "40000", "70000", "110000"]}, {"name": "ai[1]", "width": "1", "wave": ["0", "z", "1", "x"], "state": [10, 6, 13, 3], "time": ["0", "40000", "70000", "110000"]}, {"name": "ai[0]", "width": "1", "wave": ["0", "z", "1", "x"], "state": [10, 6, 13, 3], "time": ["0", "40000", "70000", "110000"]}], "time": ["120000", "ps", 10, "ns", 13]}');
  return function() {
    return jsdata;
  }
} ());
function SignalProperty(name, jsonindex, visibility) {
  this.name = name;
  this.jsonindex = jsonindex;
  this.visibility = visibility;
}
function DisplaySignals() {
  var signals = new Array();
  this.getAllSignals = function() {
    return signals;
  };
  this.clearAllSignals = function() {
    signals = new Array();
  };
  this.getSignalByName = function(name) {
    var index = this.getSignalIndexByName(name);
    return signals[index];
  };
  this.getSignalIndexByName = function(name) {
    var index = signals.findIndex(function(obj) {
      return obj['name'] == name;
    });
    return index;
  };
  this.getSignalByJsonPos = function(jsid) {
    var index = signals.findIndex(function(obj) {
      return obj['jsonindex'] == jsid;
    });
    return signals[index];
  };
  this.AddSignal = function(name, jsonindex, visibility) {
    signals.push(new SignalProperty(name, jsonindex, visibility));
  };
}
var fun = (function() {
  var signals = new DisplaySignals();
  return function() {
    return signals;
  }
} ());
function findDOMByType(list, type) {
  for (var i = 0; i < list.length; i++) {
    if (list[i].nodeName == type) {
      return list[i];
    }
  }
  return null;
};
function DragHelper() {
  var start = '';
  var stop = '';
  this.setstart = function(i) {
    this.start = i;
  };
  this.setstop = function(i) {
    this.stop = i;
    var startel = findDOMByType(document.getElementsByClassName(this.start), 'CANVAS');
    var stopel = findDOMByType(document.getElementsByClassName(i), 'CANVAS');
    var startpos = fun().getSignalIndexByName(this.start);
    var stoppos = fun().getSignalIndexByName(i);
    var s = fun().getAllSignals();
    var x = s[startpos];
    s[startpos] = s[stoppos];
    s[stoppos] = x;
    startel.setAttribute('class', i);
    stopel.setAttribute('class', this.start);
  };
}
var DragHelperClosure = (function() {
  var i = new DragHelper();
  return function() {
    return i;
  }
} ());
function findMost(arr) {
  if (!arr.length) return;
  if (arr.length === 1) return 1;
  var res = {};
  for (var i = 0,
  l = arr.length; i < l; i++) { (!res[arr[i]]) ? res[arr[i]] = 1 : res[arr[i]]++;
  }
  var keys = Object.keys(res);
  var maxNum = 0,
  maxEle;
  for (var i = 0,
  l = keys.length; i < l; i++) {
    if (res[keys[i]] > maxNum) {
      maxNum = res[keys[i]];
      maxEle = keys[i];
    }
  }
  return maxEle;
}
function round_scale(timev) {
  var ar = new Array();
  var judge = [Math.sqrt(50), Math.sqrt(10), Math.sqrt(2)];
  for (var i = 1; i <= 10; i++) {
    var gridtime = 0 | (timev / i);
    var zeroes = '0'.repeat(('' + gridtime).length - 1);
    var gridtimelt10 = gridtime / ('1' + zeroes);
    if (gridtimelt10 >= judge[0]) res = 10;
    else if (gridtimelt10 >= judge[1]) res = 5;
    else if (gridtimelt10 >= judge[2]) res = 2;
    else res = 1;
    ar.push('' + res + zeroes);
  }
  num = findMost(ar);
  i = ar.indexOf(num);
  return ar[i];
}
function convert_timescale(time, src_scale) {
  t_grades = ['p', 'n', 'u', 'm', '', 'k', 'M', 'G'];
  src_index = t_grades.indexOf(src_scale[0]);
  grade_diff = Math.floor((time.length - 1) / 3);
  dst_index = src_index + grade_diff;
  return [0 | (time * Math.pow(0.001, grade_diff)), t_grades[dst_index]];
}
function createinvisiablebr(parentel) {
  var br = document.createElement('br');
  br.setAttribute('style', 'font-size:0');
  parentel.appendChild(br);
}