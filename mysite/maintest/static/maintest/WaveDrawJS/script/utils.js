function SignalProperty(name, jsonindex, visibility, busattached) {
  this.name = name;
  this.jsonindex = jsonindex;
  this.visibility = visibility;
  this.wavecolour = ['#ff0000', //for x
  '#0000ff', //for z
  '#00ff00', //for 01
  '#000000' //hidden line
  ];
  //todo: add custom colour support in right click menu
  if (busattached) {
    this.issubbus = true;
    this.bus = busattached;
  } else if (name.includes(':')) {
    this.issubbus = false;
    this.bus = name.slice(0, name.indexOf('['));
  } else {
    this.issubbus = false;
    this.bus = null;
  }
}
function DisplaySignals() {
  //manages signals that are on display
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
  this.AddSignal = function(name, jsonpos, visibility) {
    if (name.includes('[')) {
      if (!name.includes(':')) {
        //adding part of a bus
        var busname = name.slice(0, name.indexOf('['));
        signals.push(new SignalProperty(name, jsonpos, visibility, busname));
        return;
      }
    }
    signals.push(new SignalProperty(name, jsonpos, visibility));
  };
}
var fun = (function() {
  var signals = new DisplaySignals();
  return function() {
    return signals;
  }
} ());
var global_states = (function() {
  var states = {
    mode: 0
  };
  return function() {
    return states;
  }
} ());
function filterSignalWithPara(para, type) {
  var p = para;
  var t = type;
  this.fliterfn = function(obj) {
    if (obj[t] == p) {
      return true;
    } else {
      return false;
    }
  };
  this.setcondition = function(para, type) {
    p = para;
    t = type;
  };
}
function listall(l) {
  for (var i = 0; i < l.length; i++) {
    console.log(l[i]);
  }
}
function createFilteredGroup(group, signal) {
  var fil;
  if (signal.bus && !signal.issubbus) {
    fil = new filterSignalWithPara(signal.bus, 'bus');
  } else {
    fil = new filterSignalWithPara(signal.name, 'name');
  }
  return group.filter(fil.fliterfn);
}
function _DragImpl(start, stop) {
  /*  if start and stop are 
	    (a)parts of the same bus
	    (b)independent signals:
	      swap them
        if one of start or stop is bus:
	      if the rest is bus or independent signal:
	        swap them together with their parts(if exists)
        if none of above:
	      do nothing*/
  var startsig = fun().getSignalByName(start);
  var stopsig = fun().getSignalByName(stop);
  var isswappable = false;
  if ((startsig.bus == stopsig.bus) && (startsig.issubbus == stopsig.issubbus)) {
    isswappable = true;
  } else if (startsig.bus || stopsig.bus) {
    if (!startsig.issubbus && !stopsig.issubbus) {
      isswappable = true;
    }
  }
  if (isswappable) {
    var s = fun().getAllSignals();
    var startpos = fun().getSignalIndexByName(start);
    var stoppos = fun().getSignalIndexByName(stop);
    if (startpos < stoppos) { [startpos, stoppos] = [stoppos, startpos]; [startsig, stopsig] = [stopsig, startsig];
    }
    var startgroup = createFilteredGroup(s, startsig);
    var stopgroup = createFilteredGroup(s, stopsig);
    var startlen = startgroup.length;
    var stoplen = stopgroup.length;
    stopgroup.unshift(startpos, startlen);
    Array.prototype.splice.apply(s, stopgroup);
    startgroup.unshift(stoppos, stoplen);
    Array.prototype.splice.apply(s, startgroup);
    var canvasNodes = $("#canvasl- canvas");
    for (var i = 1; i < s.length + 1; i++) {
      console.log(canvasNodes[i]);
      var newclass = s[i - 1].name;
      canvasNodes.eq(i).attr('class', newclass);
      if (s[i - 1].visibility) {
        canvasNodes.eq(i).show();
      } else {
        canvasNodes.eq(i).hide();
      }
    }
  }
  return isswappable;
}
function DragHelper() {
  //Implements drag
  var start = '';
  var stop = '';
  this.setstart = function(name) {
    this.start = name;
  };
  this.setstop = function(name) {
    this.stop = name;
    if (this.start == this.stop) {
      if (name.includes(':')) {
        bus_toggle(name.slice(0, name.search('\\[')));
        /*maybe refresh the whole set is better?
	--Sorry, elements will disappear
   */
      }
      return;
    }
    var updateflag = _DragImpl(this.start, this.stop);
    scrollbarmove().changecanvas(updateflag);
  };
}
var DragHelperClosure = (function() {
  var i = new DragHelper();
  return function() {
    return i;
  }
} ());
function _WaveZoomImpl(start, stop) {
  //convert px to actual time values
  var scrbar = scrollbarmove();
  var timebegin = scrbar.t_begin;
  var timerange = scrbar.t_end - scrbar.t_begin;
  //now calculate new begin and end
  var width = scrbar.width;
  var newbeginoffset = 0 | (timerange / width * start);
  scrbar.t_begin += newbeginoffset;
  var newendoffset = 0 | (timerange / width * stop);
  scrbar.t_end = timebegin + newendoffset;
  scrbar.changecanvas(false);
  var jstime = get_json_data().time[0] - 0;
  var propbar = $("#propotion-");
  var propv = propbar.attr('max') * scrbar.t_begin / jstime;
  propbar.attr('value', propv)
}
function WaveZoomHelper() {
  //Implements zoom in/out
  var start = 0;
  var stop = 0;
  //start and stop are in px
  this.setstart = function(pos) {
    this.start = pos;
  };
  this.setstop = function(pos) {
    this.stop = pos;
    if (1
    /*a delay is needed to enable zooming
   */
    ) {}
    _WaveZoomImpl(this.start, this.stop);
  };
}
var WaveZoomHelperClosure = (function() {
  var i = new WaveZoomHelper();
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
  //rounds time values. using 1/2/5 as the only significant number
  //e.g., 12345->10000, 23456->20000, 45678->50000, 78901->100000
  var ar = new Array();
  var res;
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
function reduce_timescale(time, src_scale) {
  var t_grades = ['p', 'n', 'u', 'm', '', 'k', 'M', 'G'];
  var src_index = t_grades.indexOf(src_scale[0]);
  var grade_diff = Math.floor((time.length - 1) / 3);
  var dst_index = src_index + grade_diff;
  return [time * Math.pow(0.001, grade_diff), t_grades[dst_index]];
}
function convert_timescale(time, dst_scale, src_scale) {
  var t_grades = ['p', 'n', 'u', 'm', '', 'k', 'M', 'G'];
  var src_index = t_grades.indexOf(src_scale[0]);
  var dst_index = t_grades.indexOf(dst_scale[0]);
  var grade_diff = dst_index - src_index;
  return [time * Math.pow(0.001, grade_diff), dst_scale];
}
/*function createinvisiablebr(parentel) {
  //seperate canvases using a 0px newline
  var br = document.createElement('br');
  br.setAttribute('style', 'font-size:0');
  parentel.appendChild(br);
}*/
function findlastless(arr,el){
	var lo=0,hi=arr.length;
	while(lo < hi-1){
        var mid = Math.floor((lo + hi)/2)
        if(el >= arr[mid])lo = mid;
        else hi = mid;}
	return lo;
}
