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
    var startgroup = createFilteredGroup(s, startsig);
    var startlen = startgroup.length;
    startgroup.unshift(stoppos, 0);
    if (startpos < stoppos) {
      //dragging downwards
      Array.prototype.splice.apply(s, startgroup);
      s.splice(startpos, startlen);
    } else {
      //dragging upwards
      s.splice(startpos, startlen);
      Array.prototype.splice.apply(s, startgroup);
    }
    var $lists = $('.inner-list');
    for (var i = 0; i < $lists.length; i++) {
      var children = $($lists[i]).children().toArray();
      startgroup = children.slice(startpos, startpos + startlen);
      startgroup.unshift(stoppos, 0);
      if (startpos < stoppos) {
        //dragging downwards
        Array.prototype.splice.apply(children, startgroup);
        children.splice(startpos, startlen);
      } else {
        //dragging upwards
        children.splice(startpos, startlen);
        Array.prototype.splice.apply(children, startgroup);
      }
      var fragment = document.createDocumentFragment();
      for (var j = 0; j < children.length; j++) {
        fragment.appendChild(children[j]);
      }
      $lists[i].appendChild(fragment);
    }
  }
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
    _DragImpl(this.start, this.stop);
  };
}
var DragHelperClosure = (function() {
  var i = new DragHelper();
  return function() {
    return i;
  }
} ());
function _WaveZoomImpl(scrbar, start, stop, timerange, width, jstime) {
  //convert px to actual time values
  if (start > stop) {
    //right to left, zoom out
    var scalefactor = width / (start - stop);
    timerange = Math.floor(timerange * scalefactor);
    //now calculate new begin and end
    var newbeginoffset = Math.floor(timerange / width * start);
    scrbar.t_begin -= newbeginoffset;
    if (scrbar.t_begin < 0) scrbar.t_begin = 0;
    scrbar.t_end = scrbar.t_begin + timerange;
    if (scrbar.t_end > jstime) scrbar.t_end = jstime;
  }
  //now calculate new begin and end
  else {
    var timebegin = scrbar.t_begin;
    var newbeginoffset = Math.floor(timerange / width * start);
    scrbar.t_begin += newbeginoffset;
    var newendoffset = Math.floor(timerange / width * stop);
    scrbar.t_end = timebegin + newendoffset;
  }
}
function _PanImpl(scrbar, start, stop, timerange, width, jstime) {
  //convert px to actual time values
  var scalefactor = (start - stop) / width;
  var dist = Math.floor(timerange * scalefactor);
  //now calculate new begin and end
  var newtime = [scrbar.t_begin + dist, scrbar.t_end + dist];
  if (newtime[0] < 0) {
    newtime[0] = 0;
    newtime[1] = newtime[0] + timerange;
  } else if (newtime[1] > jstime) {
    newtime[1] = jstime;
    newtime[0] = newtime[1] - timerange;
  }
  scrbar.t_begin = newtime[0];
  scrbar.t_end = newtime[1];
}
function CanvasMouseClickCommon(start, stop, func) {
  var scrbar = scrollbarmove();
  var timerange = scrbar.t_end - scrbar.t_begin;
  var width = scrbar.width;
  var jstime = get_json_data().time[0] - 0;
  func(scrbar, start, stop, timerange, width, jstime);
  scrbar.changecanvas(false);
  var propbar = $("#propotion-");
  var propv = propbar.attr('max') * scrbar.t_begin / jstime;
  CursorMover.movetoX(CursorMover.nowpos);
  propbar.attr('value', propv)
}
function CanvasMouseClickHelper() {
  //Dispatches mouseclick events on canvases
  var start = 0;
  var stop = 0;
  //start and stop are in px
  this.setstart = function(pos) {
    this.start = pos;
  };
  this.setstop = function(pos) {
    this.stop = pos;
    if (global_states().mode == 0) {
      //mode is zoom, do zoom in/out
      if (this.start == this.stop) {
        //single click on canvas does not trigger zooming
        return;
      }
      CanvasMouseClickCommon(this.start, this.stop, _WaveZoomImpl);
    } else if (global_states().mode == 1) {
      //mode is cursor, move cursor to stop position
      CursorMover.movetoX(pos);
    } else {
      //mode is pan, move the canvas contents
      CanvasMouseClickCommon(this.start, this.stop, _PanImpl);
    }
  };
}
var CanvasMouseClickHelperClosure = (function() {
  var i = new CanvasMouseClickHelper();
  return function() {
    return i;
  }
} ());
function ScorllSyncHelper() {
  //Implements sync of scorllbars
  var currentTab = 0;
  this.scale = 1;
  //use labmda to preserve 'this' state, do not replace with function(){...}
  //some formatting tools may give erroneous result
  this.setup = ()=>{
    var $l = $('#namel-');
    var $r = $('#canvasl-');
    $l.scroll(()=>{
      if (this.currentTab !== 1) return;
      $r[0].scrollTop = $l[0].scrollTop * this.scale;
    });
    $r.scroll(()=>{
      if (this.currentTab !== 2) return;
      $l[0].scrollTop = $r[0].scrollTop / this.scale;
    });
    $l.mouseover(()=>{
      this.currentTab = 1;
    });
    $r.mouseover(()=>{
      this.currentTab = 2;
    });
    this.$l = $l;
    this.$r = $r;
  };
  this.calibrateTracking = ()=>{
    var $lc = this.$l.children();
    var $rc = this.$r.children();
    this.scale = ($rc[0].offsetHeight - this.$r[0].offsetHeight) / ($lc[0].offsetHeight - this.$l[0].offsetHeight);
  };
}
var ScorllSyncHelperClosure = (function() {
  var i = new ScorllSyncHelper();
  i.setup();
  i.calibrateTracking();
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
    var gridtime = Math.floor(timev / i);
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
function findlastless(arr, el) {
  var lo = 0,
  hi = arr.length;
  while (lo < hi - 1) {
    var mid = Math.floor((lo + hi) / 2);
    if (el >= arr[mid]) {
      lo = mid;
    } else {
      hi = mid;
    }
  }
  return lo;
}
function parseScaleText(scale) {
  //first, find time value
  var pat = new RegExp("[0-9]+");
  var time = pat.exec(scale);
  //next, find timescale value
  var grade = scale.replace(time, '');
  return convert_timescale(time, get_json_data()['time'][1], grade);
}
function getTextWidth(fontSize, fontFamily, text) {
  var span = document.createElement("span");
  var result = span.offsetWidth;
  span.style.visibility = "hidden";
  span.style.fontSize = fontSize;
  span.style.fontFamily = fontFamily;
  span.style.display = "inline-block";
  document.body.appendChild(span);
  if (typeof span.textContent != "undefined") {
    span.textContent = text;
  } else {
    span.innerText = text;
  }
  result = parseFloat(window.getComputedStyle(span).width) - result;
  span.parentNode.removeChild(span);
  return result;
}
