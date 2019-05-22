function clearallchildren(parentel) {
  while (parentel.hasChildNodes()) {
    parentel.removeChild(parentel.firstChild);
  }
}
function bus_toggle(bus_name) {
  //shows or hides all branches of specific bus
  //note: all hidden branches are NOT updated

  var s = fun().getAllSignals();
  var modified = [];
  for (var i = 0; i < s.length; i++) {
    //change display list
    if (s[i].bus == bus_name) {
      if (s[i].name.includes(':')) continue;
      s[i].visibility = !s[i].visibility;
      modified.push(i);
    }
  }
  var $lists = $('.inner-list');
  console.log($lists);
  for (var i = 0; i < modified.length; i++) {
    //sync with DOM
    $($lists[0].childNodes[modified[i]]).toggle();
    $($lists[1].childNodes[modified[i]]).toggle();
  }

}
var scrollbarmove = (function() {
  var states = {
    widthpar: .7,
    width: $('#canvasl-').width(),
    t_begin: 0,
    t_end: 0,
    changecanvas: function(can_update_names) {
      draw(this.width, this.t_begin, this.t_end, can_update_names);
    },
    reset_to_default: function() {
      this.width = $('#canvasl-').width();
      var jsdata = get_json_data();
      if (jsdata) {
        this.t_begin = 0;
        this.t_end = get_json_data().time[0] - 0;
        draw(this.width, this.t_begin, this.t_end, true);
      }
    }
  };
  return function() {
    return states;
  };
} ());
function addDrag(el) {
  el.onmouseup = function(event) {
    DragHelperClosure().setstop(el.getAttribute('class').split(' ')[0]);
  }
  el.onmousedown = function(event) {
    DragHelperClosure().setstart(el.getAttribute('class').split(' ')[0]);
  }
}
function addZoom() {
  this.onmouseup = function(event) {
    var left = Math.floor($(this).offset().left);
    WaveZoomHelperClosure().setstop(event.clientX - left);
  };
  this.onmousedown = function(event) {
    var left = Math.floor($(this).offset().left);
    WaveZoomHelperClosure().setstart(event.clientX - left);
  };
}
function CursorMove() {
  this.$cursor = $("#cursor-");
  this.$info = $("#wavedraw-cursor-info");
  this.cursoroffset = $("#wavedrawing-gridc").offset().left - $("#wavedrawing-heading-text").offset().left;
  this.nowpos = 0;
  this.movetoX = function(pos) {
    this.nowpos = pos;
    var scrbar = scrollbarmove();
    var width = scrbar.width;
    var timerange = scrbar.t_end - scrbar.t_begin;
    var newbeginoffset = Math.floor(timerange / width * pos);

    this.$info.html(scrbar.t_begin + newbeginoffset + get_json_data()['time'][1]);
    this.$cursor.css({
      'left': this.cursoroffset + pos + 8
    });
    this.$info.css({
      'left': this.cursoroffset + pos + 8
    });
  };
}
var CursorMover = new CursorMove();

function TimeBarManage() {
  var $timebar = $(".\\.timebar span");
  var $barelems = $timebar.children();
  var state = false; //show:true hide:false
  $barelems[1].onclick = function() {
    if (!state) {
      state = true;
      $barelems[1].innerHTML = " to ";
      $barelems.show();
    }
  };
  $barelems[3].onclick = function() {
    $barelems.hide();
    var starttime = parseScaleText($barelems[0].value);
    var stoptime = parseScaleText($barelems[2].value);
    var scrbar = scrollbarmove();
    var jstime = get_json_data().time[0] - 0;
    scrbar.t_begin = starttime[0] - 0;
    scrbar.t_end = stoptime[0] - 0;
    scrbar.changecanvas(false);
    var propbar = $("#propotion-");
    var propv = propbar.attr('max') * scrbar.t_begin / jstime;
    propbar.attr('value', propv);
    $barelems[0].value = starttime.join("");
    $barelems[2].value = stoptime.join("");
    $barelems[1].innerHTML = $barelems[0].value + " to " + $barelems[2].value;
    $($barelems[1]).show();
    state = false;
  };
  this.sync = function(t_begin, t_end, scale) {
    $barelems[0].value = t_begin + scale;
    $barelems[2].value = t_end + scale;
    $barelems[1].innerHTML = $barelems[0].value + " to " + $barelems[2].value;
  };
}
var TimeBarManager = new TimeBarManage();
