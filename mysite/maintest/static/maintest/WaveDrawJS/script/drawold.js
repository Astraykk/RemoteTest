var flag_canvas_OK=false;
function draw_hline(ctx, x_st, y_st, x_off, color) {
  ctx.lineWidth = 1;
  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.moveTo(x_st, y_st);
  ctx.lineTo(x_st + x_off, y_st);
  ctx.stroke();
  ctx.closePath();
}
function draw_vline(ctx, x_st, y_st, y_off, color) {
  ctx.lineWidth = 1;
  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.moveTo(x_st, y_st);
  ctx.lineTo(x_st, y_st + y_off);
  ctx.stroke();
  ctx.closePath();
}
function write_text(ctx, x_st, y_st, textc) {
  ctx.font = "12px Arial";
  ctx.fillStyle = "#ffffff";
  ctx.fillText(textc, x_st, y_st);
}
function check_canvas_availablity() {
  //简单地检测当前浏览器是否支持Canvas对象，以免在一些不支持html5的浏览器中提示语法错误
  var canvas = document.createElement('canvas');
  if (canvas.getContext) return true;
  else return false;
}
function query_canvas(canvasname, height, width) {
/*for bus signal serach
var x1=canvasname.replace('[','\\[');
x1=x1.replace(']','\\]');
  var ret = $('canvas.'+x1);
console.log(ret)
  if (ret.length) {
    ret[0].height = height;
    ret[0].width = width;
  return ret[0];
  } else {
console.log(x1)
    var ret = document.createElement('canvas');
    ret.setAttribute('class', canvasname);
    parentnode.appendChild(ret);
    ret.height = height;
    ret.width = width;
  return ret;
  }*/
  var canvasl = document.getElementsByClassName(canvasname);
  var ret;
  if (!canvasl.length) {
    var ret = document.createElement('canvas');
    ret.setAttribute('class', canvasname);
    ret.height = height;
    ret.width = width;
    return [false, ret];
  } else {
    for (var i = 0; i < canvasl.length; i++) {
      if (canvasl[i].nodeName == 'CANVAS') {
        ret = canvasl[i];
        ret.height = height;
        ret.width = width;
        return [true, ret];
      }
    }
  }
  return ret;
}
function draw_grid(parentcontainer, x_st, y_st, x_range, time) {
  var cl = document.getElementById("canvasl-").firstChild;
  var qcanvas = query_canvas('wavedraw-gridc', 1 + 0 | y_st, x_range);
  var canvas = qcanvas[1];
  if (!qcanvas[0]) {
    cl.appendChild(canvas);
  }
  var ctx = canvas.getContext("2d");
  draw_hline(ctx, x_st, y_st, x_range, '#ffffff');
  var timediff = (time[1][1] - time[1][0]).toFixed(0);
  //determine the size of a grid
  var gridsize = round_scale(timediff);
  var gridscale = reduce_timescale(gridsize, time[0][1]);
  gridsize = 0 | gridsize;
  //get the first gridline to draw
  //e.g. if starttime=1051ns and grid=10ns
  //then the first gridline is at 1050ns
  var first_visible_pos = (time[1][0] / gridsize);
  var fv_time =(0 | first_visible_pos) * gridsize;
  var fv_scale = reduce_timescale(round_scale(fv_time), time[0][1]);
  var scale_text=0;
  for (var i = 0,
  val = fv_time;
  val < time[1][1]; i++) {
    var x_off = 0 | ((x_range - 0) * (val - time[1][0]) / timediff);
    draw_vline(ctx, x_st + x_off, y_st, -(y_st / 2), '#ffffff');
    write_text(ctx, x_st + x_off, y_st / 2, (i * gridsize + fv_time) + '' + time[0][1]);
    val += gridsize;
  }
}
function get_bus_color(wave) {
// return 0 for x, 1 for z, 2 for others
  var hasx = false,
  hasz = false;
  for (var i = 0; i < wave.length; i++) {
    if ('x' == wave[i]) hasx = true;
    else if ('z' == wave[i]) hasz = true;
  }
  if (hasx) return 0;
  else if (hasz) return 1;
  return 2;
}
function draw(cwidth, time_begin, time_end, reset_flag) {
  //获取Canvas对象(画布)
  var canvasl = $("#canvasl- ul")[0];
  var namel = $("#namel- ul")[0];
  //removs all old canvas name items before starting drawing
if(reset_flag){
  clearallchildren(namel);
    var nametag = document.createElement('li');
    nametag.innerHTML = 'Signals';
    nametag.setAttribute('id', 'wavedrawing-heading');
    namel.appendChild(nametag);}
  if (flag_canvas_OK) {
    var jsdata = get_json_data();
    var timerange = [time_begin,time_end];
		var $timebar=$(".\\.timebar");
		//$timebar.show();
		var timebarspan=$timebar.children('span').toArray();
		addInputandJump(timebarspan[0]);
		addInputandJump(timebarspan[1]);
		timebarspan[0].childNodes[0].innerHTML=time_begin+jsdata.time[1];
		timebarspan[1].childNodes[0].innerHTML=time_end+jsdata.time[1];
    draw_grid(canvasl, 0.5, 22.5, cwidth, [jsdata['time'], timerange]);
    for (var i = 0; i < jsdata.dat.length; i++) {
      //check if any new signals are added to json
      var wave = jsdata.dat[i];
      var wabeobj = fun().getSignalByName(wave['name']);
      if (!wabeobj) {
        fun().AddSignal(wave['name'], i, true);
      }
    }
    for (var ca = 0,
    sig = fun().getAllSignals(); ca < sig.length; ca++) {
      var wave = jsdata.dat[sig[ca].jsonindex];
      if (!sig[ca].visibility) {
        continue;
      }
      var qcanvas = query_canvas(wave['name'], 35, cwidth);
      var canvas = qcanvas[1];
if(reset_flag){
      nametag = document.createElement('li');
      nametag.innerHTML = '<span>' + wave['name'] + '</span>';
      if (wave['width'] > 1) {nametag.setAttribute('class', wave['name']+' w-bus');}
      else {
      nametag.setAttribute('class', wave['name']);}
      addDrag(nametag);
      namel.appendChild(nametag);}
      var xmargin = 0.5;
      var xpos;
      var ypos;
      var xend;
      var ctx=canvas.getContext("2d");
      if (wave['time'].indexOf(jsdata['time'][0]) == -1) {
        wave['time'].push(jsdata['time'][0]);
      }
var timediffval=time_end-time_begin;
var cwidth=canvas.width - 0;
      var wavecache = [];
      var colourused = sig[ca].wavecolour;
      for (var i = 0; i < wave.state.length; i++) {
        if ((wave['time'][i] <= time_end) && (wave['time'][i + 1] >= time_begin)) {
        xpos = (0 | (canvas.width - 0) * (wave['time'][i] - timerange[0]) / ((timerange[1] - timerange[0]))) + xmargin;
        xend = (0 | (canvas.width - 0) * (wave['time'][i + 1] - timerange[0]) / ((timerange[1] - timerange[0]))) + xmargin;
          switch (wave['state'][i]) {
          case 0:
          case 1:
          case 2:
          case 3:
            ypos = 20.5;
            wavecache.push([xpos, ypos, 0]);
            wavecache.push([xend, ypos, 0]);
            break;
          case 4:
          case 5:
          case 6:
          case 7:
            ypos = 20.5;
            wavecache.push([xpos, ypos, 1]);
            wavecache.push([xend, ypos, 1]);
            break;
          case 8:
          case 9:
          case 10:
          case 11:
            ypos = 30.5;
            wavecache.push([xpos, ypos, 2]);
            wavecache.push([xend, ypos, 2]);
            break;
          case 12:
          case 13:
          case 14:
          case 15:
            ypos = 10.5;
            wavecache.push([xpos, ypos, 2]);
            wavecache.push([xend, ypos, 2]);
            break;
          case 16://this state will not appear, remove later
            break;
          /*case 17:
            cl = get_bus_color(wave['wave'][i - 1]);
            draw_vline(canvas, xpos + xmargin - 1, 10.5, 5, cl);
            draw_vline(canvas, xpos + xmargin - 1, 30.5, -5, cl);
          case 18:
            cl = get_bus_color(wave['wave'][i]);
            draw_vline(canvas, xpos + xmargin, 15.5, 10, cl);
            draw_vline(canvas, xpos + xmargin + 1, 10.5, 5, cl);
            draw_vline(canvas, xpos + xmargin + 1, 30.5, -5, cl);
            draw_hline(canvas, xpos + xmargin + 1, 10.5, xend - xpos - 2, cl);
            draw_hline(canvas, xpos + xmargin + 1, 30.5, xend - xpos - 2, cl);*/
          case 17:
            cl = get_bus_color(wave['wave'][i - 1]);
            draw_vline(ctx, xpos  - 1, 10.5, 5, cl);
            draw_vline(ctx, xpos  - 1, 30.5, -5, cl);
          case 18:
            cl = get_bus_color(wave['wave'][i]);
            wavecache.push([xend, 30.5, 3]);
            wavecache.push([xpos, 30.5, cl]);
            //wavecache.push([xpos, 24.5, cl]);
            //wavecache.push([xpos-1, 24.5, cl]);
            wavecache.push([xpos-1, 20.5, cl]);
            //wavecache.push([xpos-1, 16.5, cl]);
            //wavecache.push([xpos, 16.5, cl]);
            wavecache.push([xpos, 10.5, cl]);
            wavecache.push([xend, 10.5, cl]);
            if (xpos < 0) xpos = 0;
            write_text(ctx, xpos  + 2, 24.5, wave['wave'][i]);
            break;
          }
        }
    }
        ctx.beginPath();
        ctx.strokeStyle = colourused[wavecache[0][2]];
        ctx.moveTo(wavecache[0][0], wavecache[0][1]);
        for (var i = 1; i < wavecache.length; i++) {
          if (wavecache[i][2] != ctx.strokeStyle) {
            ctx.stroke();
            ctx.closePath();
            ctx.beginPath();
            ctx.strokeStyle = colourused[wavecache[i][2]];
            ctx.moveTo(wavecache[i - 1][0], wavecache[i - 1][1]);
          }
          ctx.lineTo(wavecache[i][0], wavecache[i][1]);
        }
        ctx.stroke();
        ctx.closePath();
      if (!qcanvas[0]) {
        canvasl.appendChild(canvas);
      }
    var sep = document.getElementById('column-sep');
    sep.style.height = canvasl.parentNode.offsetHeight + 'px';
  }
}}
