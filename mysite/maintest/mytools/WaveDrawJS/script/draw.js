function draw_hline(canvas, x_st, y_st, x_off, color) {
  var ctx = canvas.getContext("2d");
  //开始一个新的绘制路径
  ctx.lineWidth = 1;
  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.moveTo(x_st, y_st);
  ctx.lineTo(x_st + x_off, y_st);
  ctx.stroke();
  ctx.closePath();
}
function draw_vline(canvas, x_st, y_st, y_off, color) {
  var ctx = canvas.getContext("2d");
  //开始一个新的绘制路径
  ctx.lineWidth = 1;
  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.moveTo(x_st, y_st);
  ctx.lineTo(x_st, y_st + y_off);
  ctx.stroke();
  ctx.closePath();
}
function check_canvas_availablity() {
  //简单地检测当前浏览器是否支持Canvas对象，以免在一些不支持html5的浏览器中提示语法错误
  var canvas = document.createElement('canvas');
  if (canvas.getContext) return true;
  else return false;
}
function r_or_c_canvas(parentnode, canvasid, height, width) {
  var canvasl = document.getElementsByClassName(canvasid);
  var ret;
  if (!canvasl.length) {
    var ret = document.createElement('canvas');
    ret.setAttribute('style', 'background-color: black;');
    ret.setAttribute('class', canvasid);
    parentnode.appendChild(ret);
    ret.height = height;
    ret.width = width;
  } else {
    for (var i = 0; i < canvasl.length; i++) {
      if (canvasl[i].nodeName == 'CANVAS') {
        ret = canvasl[i];
        ret.height = height;
        ret.width = width;
        break;
      }
    }
  }
  return ret;
}
function draw_grid(x_st, y_st, x_range, time) {
  var cl = document.getElementById("canvasl");
  var canvas = r_or_c_canvas(cl, 'wavedraw-gridc', 1 + 0 | y_st, x_range);
  draw_hline(canvas, x_st, y_st, x_range, '#ffffff');
  var timediff = (time[1][1] - time[1][0]).toFixed(0);
  var gridsize = round_scale(timediff);
  var gridscale = convert_timescale(gridsize, time[0][1]);
  gridsize = 0 | gridsize;
  var first_visible = (time[1][0] / gridsize);
  var fv_disp = 0 | first_visible;
  var fv_scale = fv_disp * gridsize;
  for (var i = 0,
  val = fv_scale,
  scale = convert_timescale(val + '', time[0][1]); val < time[1][1]; i++) {
    var x_off = 0 | ((x_range - 0) * (val - time[1][0]) / timediff);
    draw_vline(canvas, x_st + x_off, y_st, -(y_st / 2), '#ffffff');
    write_text(canvas, x_st + x_off, y_st / 2, (i * gridscale[0] + scale[0]) + '' + gridscale[1] + 's');
    val += gridsize;
  }
}
function write_text(canvas, x_st, y_st, textc) {
  var ctx = canvas.getContext("2d");
  ctx.font = "12px Arial";
  ctx.fillStyle = "#ffffff";
  ctx.fillText(textc, x_st, y_st);
}
function get_bus_color(wave) {
  var hasx = false,
  hasz = false;
  for (var i = 0; i < wave.length; i++) {
    if ('x' == wave[i]) hasx = true;
    else if ('z' == wave[i]) hasz = true;
  }
  if (hasx) return '#ff0000';
  else if (hasz) return '#0000ff';
  return '#00ff00';
}
function draw(cwidth, scale, propotion) {
  //获取Canvas对象(画布)
  var canvasl = document.getElementById("canvasl");
  var namel = document.getElementById("namel");
  //removs all old canvases(if any) before starting drawing
  clearallchildren(namel);
  if (check_canvas_availablity()) {
    var jsdata = get_json_data();
    var timemax = jsdata['time'][0]
    var timerange = [propotion * jsdata.time[0] * (1 - scale)];
    timerange.push(timerange[0] + jsdata.time[0] * scale);
    draw_grid(0.5, 22.5, cwidth, [jsdata['time'], timerange]);
    createinvisiablebr(canvasl);
    var nametag = document.createElement('li');
    nametag.innerHTML = 'Signals';
    namel.appendChild(nametag);
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
      var jsonindex = sig[ca].jsonindex;
      var wave = jsdata.dat[jsonindex];
      if (!sig[ca].visibility) {
        continue;
      }
      var canvas = r_or_c_canvas(canvasl, wave['name'], 35, cwidth);
      addDrag(canvas);
      nametag = document.createElement('li');
      nametag.innerHTML = '<div style=\'color:blue\'>' + wave['name'] + '</div>';
      nametag.setAttribute('class', wave['name']);
      nametag.setAttribute('style', 'outline: 1px solid red;margin:5px;font-size:1.4em;');
      namel.appendChild(nametag);
      if (wave['width'] > 1) nametag.onclick = bus_toggle;
      var xmargin = 0.5;
      var xpos;
      var ypos;
      var xoff;
      var yoff;
      if (wave['time'].indexOf(jsdata['time'][0]) == -1) {
        wave['time'].push(jsdata['time'][0]);
      }
      for (var i = 0; i < wave.state.length; i++) {
        xpos = 0 | (canvas.width - 0) * (wave['time'][i] - timerange[0]) / (timerange[1] - timerange[0]);
        xoff = 0 | ((canvas.width - 0) * (wave['time'][i + 1] - timerange[0]) / (timerange[1] - timerange[0]) - xpos);
        if ((xpos <= cwidth) && (xpos + xoff >= 0)) {
          switch (wave['state'][i]) {
          case 0:
          case 1:
            ypos = 20.5;
            yoff = 0;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#ff0000');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#ff0000');
            break;
          case 2:
            ypos = 20.5;
            yoff = 10;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#ff0000');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#ff0000');
            break;
          case 3:
            ypos = 20.5;
            yoff = -10;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#ff0000');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#ff0000');
            break;
          case 4:
          case 5:
            ypos = 20.5;
            yoff = 0;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#0000ff');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#0000ff');
            break;
          case 6:
            ypos = 20.5;
            yoff = 10;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#0000ff');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#0000ff');
            break;
          case 7:
            ypos = 20.5;
            yoff = -10;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#0000ff');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#0000ff');
            break;
          case 8:
          case 9:
            ypos = 30.5;
            yoff = -10;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#00ff00');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#00ff00');
            break;
          case 10:
            ypos = 30.5;
            yoff = 0;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#00ff00');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#00ff00');
            break;
          case 11:
            ypos = 30.5;
            yoff = -20;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#00ff00');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#00ff00');
            break;
          case 12:
          case 13:
            ypos = 10.5;
            yoff = 10;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#00ff00');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#00ff00');
            break;
          case 14:
            ypos = 10.5;
            yoff = 20;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#00ff00');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#00ff00');
            break;
          case 15:
            ypos = 10.5;
            yoff = 0;
            draw_vline(canvas, xpos + xmargin, ypos, yoff, '#00ff00');
            draw_hline(canvas, xpos + xmargin, ypos, xoff, '#00ff00');
            break;
          case 16:
            draw_vline(canvas, xpos + xmargin, 15.5, 10, '#00ff00');
            draw_vline(canvas, xpos + xmargin + 1, 10.5, 5, '#00ff00');
            draw_vline(canvas, xpos + xmargin + 1, 30.5, -5, '#00ff00');
            draw_hline(canvas, xpos + xmargin + 1, 10.5, xoff - 2, '#00ff00');
            draw_hline(canvas, xpos + xmargin + 1, 30.5, xoff - 2, '#00ff00');
            write_text(canvas, xpos + xmargin + 2, 24.5, wave['wave'][i]);
            break;
          case 17:
            cl = get_bus_color(wave['wave'][i - 1]);
            draw_vline(canvas, xpos + xmargin - 1, 10.5, 5, cl);
            draw_vline(canvas, xpos + xmargin - 1, 30.5, -5, cl);
          case 18:
            cl = get_bus_color(wave['wave'][i]);
            draw_vline(canvas, xpos + xmargin, 15.5, 10, cl);
            draw_vline(canvas, xpos + xmargin + 1, 10.5, 5, cl);
            draw_vline(canvas, xpos + xmargin + 1, 30.5, -5, cl);
            draw_hline(canvas, xpos + xmargin + 1, 10.5, xoff - 2, cl);
            draw_hline(canvas, xpos + xmargin + 1, 30.5, xoff - 2, cl);
            if (xpos < 0) xpos = 0;
            write_text(canvas, xpos + xmargin + 2, 24.5, wave['wave'][i]);
            break;
          }
        }
      }
      createinvisiablebr(canvasl);
    }
    var sep = document.getElementById('sep');
    sep.style.height = canvasl.clientHeight + 'px';
  }
}