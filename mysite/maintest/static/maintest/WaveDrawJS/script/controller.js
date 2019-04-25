function clearallchildren(parentel) {
  while (parentel.hasChildNodes()) {
    parentel.removeChild(parentel.firstChild);
  }
}
function bus_toggle(bus_name) {
  //shows or hides all branches of specific bus
  //note: all hidden branches are NOT updated
  var fil = new filterSignalWithPara(bus_name, 'bus');
  var toggled = fun().getAllSignals().filter(fil.fliterfn);
  var $canvas = $('#canvasl- canvas').toArray();
  var $nameli = $('#namel- li').toArray();
  for (var i = 0; i < toggled.length; i++) {
    //change display list
    if (toggled[i].name.includes(':')) continue;
    toggled[i].visibility = !toggled[i].visibility;
    //sync with DOM
    fil.setcondition(toggled[i].name, 'className');
    var toggledDOM = $canvas.filter(fil.fliterfn);
    $(toggledDOM).toggle();
  }
  //update the element '#namel- ul.inner-list'
  //and refresh canvases that are set to visible
  scrollbarmove().changecanvas();
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
    console.log(this.offsetLeft);
    DragHelperClosure().setstop(el.getAttribute('class').replace(' w-bus', ''));
  }
  el.onmousedown = function(event) {
    DragHelperClosure().setstart(el.getAttribute('class').replace(' w-bus', ''));
  }
}
function addZoom() {
  this.onmouseup = function(event) {
    var left = 0 | $(this).offset().left;
    //console.log(event.clientX,left);
    WaveZoomHelperClosure().setstop(event.clientX - left);
  };

  this.onmousedown = function(event) {
    var left = 0 | $(this).offset().left;
    //console.log(event.clientX,left);
    WaveZoomHelperClosure().setstart(event.clientX - left);
  };
}
function addInputandJump(obj) {
  var $children = $(obj).children();
  if ($children.length) {
    return;
  } else {
    obj.innerHTML = "<text></text><input type=\"text\"  style=\"display:none\">";
    $children = $(obj).children();
    $children[0].onclick = function() {
      $children.toggle();
      $children[1].value = $children[0].innerHTML;
      $children[1].focus();
    };
    $children[1].onblur = function() {
      $children[0].innerHTML = $children[1].value;
      $children.toggle();

    };
  }
}
