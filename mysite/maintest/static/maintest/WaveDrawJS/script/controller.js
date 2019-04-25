function clearallchildren(parentel) {
  while (parentel.hasChildNodes()) {
    parentel.removeChild(parentel.firstChild);
  }
}
function bus_toggle(event) {
  console.log(event.clientX, event.clientY);
  console.log(this);
  var bus_class = this.getAttribute('class');
  var bus_name = bus_class.slice(0, bus_class.search('\\['));
  var $bus = $('[class^=' + bus_name + '\\[]:not([class*=":"])');
  $bus.toggle();
  var cvbus = $bus.filter('canvas').toArray();
  for (var i = 0; i < cvbus.length; i++) {
    var name = cvbus[i].getAttribute('class');
    var vis = fun().getSignalByName(name);
    vis.visibility = !vis.visibility;
  }
  var sep = $("#sep").get(0);
  var cl = $("#canvasl").get(0);
  sep.style.height = cl.clientHeight + 'px';

  scrollbarmove().onchange();
}
function null_fun_1(event) {
  console.log(event.clientX, event.clientY);
  console.log(this);
  var bus_class = this.getAttribute('class');
  var bus_name = bus_class.slice(0, bus_class.search('\\['));
  var $bus = $('[class^=' + bus_name + '\\[]:not([class*=":"])');
  $bus.toggle();
  var cvbus = $bus.filter('canvas').toArray();
  for (var i = 0; i < cvbus.length; i++) {
    var name = cvbus[i].getAttribute('class');
    var vis = fun().getSignalByName(name);
    vis.visibility = !vis.visibility;
  }
  var sep = $("#sep").get(0);
  var cl = $("#canvasl").get(0);
  sep.style.height = cl.clientHeight + 'px';

  scrollbarmove().onchange();
}
var scrollbarmove = (function() {
  var states = {
    propotion: 1,
    scale: 1,
    widthfactor: .7,
    width: $('div:eq(1)').width() * .7,
    onchange: function() {
      draw(states.width, states.scale, states.propotion);
    },
    reset_to_default: function() {
      states.propotion = 1;
      states.scale = 1;
      states.width = $('div:eq(1)').width() * .7;
      draw(states.width, states.scale, states.propotion);
    }
  };
  return function() {
    return states;
  }
} ());
function addDrag(canvas) {
  canvas.onmouseup = function(event) {
    DragHelperClosure().setstop(canvas.getAttribute('class'));
    scrollbarmove().onchange();
  }
  canvas.onmousedown = function(event) {
    DragHelperClosure().setstart(canvas.getAttribute('class'));
  }
}
$(document).ready(function() {
  $("#load")[0].onclick = function() {
    $("#draw").attr("disabled", false);
    scrollbarmove().onchange();
  }
  $("#draw")[0].onclick = function() {
    fun().clearAllSignals();
    clearallchildren($("#canvasl")[0]);
    scrollbarmove().reset_to_default();
  }
  $("#sep")[0].onclick = function(event) {
    console.log(event.clientX, event.clientY);
    console.log(arguments[0]);
  }
  $("#width")[0].onchange = function() {
    var width = this.value / this.max;
    var bar = scrollbarmove();
    bar.width = 0 | bar.widthfactor * width * $('div:eq(1)').width();
    if ($("#draw").attr('disabled') != 'disabled') bar.onchange();
  }
  $("#scale")[0].onchange = function() {
    var scale = 0.1 + 0.9 * this.value / this.max;
    var bar = scrollbarmove();
    bar.scale = scale;
    if ($("#draw").attr('disabled') != 'disabled') bar.onchange();
  }
  $("#propotion")[0].onchange = function() {
    var propotion = this.value / this.max;
    var bar = scrollbarmove();
    bar.propotion = propotion;
    if ($("#draw").attr('disabled') != 'disabled') bar.onchange();
  }

});