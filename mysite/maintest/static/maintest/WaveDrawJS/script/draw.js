var flag_canvas_OK = false;
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
function write_text(ctx, x_st, y_st, textc, maxWidth) {
  ctx.font = "12px Monospace";
  ctx.fillStyle = "#ffffff";
  ctx.fillText(textc, x_st, y_st, maxWidth);
}
function check_canvas_availablity() {
  //简单地检测当前浏览器是否支持Canvas对象，以免在一些不支持html5的浏览器中提示语法错误
  var canvas = document.createElement('canvas');
  if (canvas.getContext) return true;
  else return false;
}
function query_canvas(canvasname, height, width) {
  var canvasl = document.getElementsByTagName('CANVAS');
  var ret;
  if (canvasl.length){
    for (var i = 0; i < canvasl.length; i++) {
      if (canvasl[i].getAttribute("data-canvasname") == canvasname) {
        ret = canvasl[i];
        ret.height = height;
        ret.width = width;
        return [true, ret];
      }
    }
  }
    ret = document.createElement('canvas');
    ret.setAttribute('data-canvasname', canvasname);
    ret.height = height;
    ret.width = width;
    return [false, ret];
}
function draw_grid(x_st, y_st, x_range, time) {
  var gridcanvas = $('#wavedrawing-gridc')[0];
  gridcanvas.width = x_range;
  gridcanvas.height = Math.ceil(y_st);
  var ctx = gridcanvas.getContext("2d");
  draw_hline(ctx, x_st, y_st, x_range, '#ffffff');
  var timediff = (time[1][1] - time[1][0]).toFixed(0);
  //determine the size of a grid
  var gridsize = round_scale(timediff);
  var gridscale = reduce_timescale(gridsize, time[0][1]);
  gridsize = Math.floor(gridsize);
  //get the first gridline to draw
  //e.g. if starttime=1051ns and grid=10ns
  //then the first gridline is at 1050ns
  var first_visible_pos = (time[1][0] / gridsize);
  var fv_time = Math.floor(first_visible_pos) * gridsize;
  var fv_scale = reduce_timescale(round_scale(fv_time), time[0][1]);
  var scale_text = 0;
  for (var i = 0,
  val = fv_time; val < time[1][1]; i++) {
    var x_off = Math.floor((x_range - 0) * (val - time[1][0]) / timediff);
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
function draw(cwidth, time_begin, time_end, flag_reset) {
  var canvasfragment = document.createDocumentFragment();
  var namefragment = document.createDocumentFragment();
  var timerange = [time_begin, time_end];
  if (flag_canvas_OK) {
    var jsdata = get_json_data();
    var timerange = [time_begin, time_end];
    draw_grid(0.5, 22.5, cwidth, [jsdata['time'], timerange]);
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
      if (flag_reset) {
        var nametag = document.createElement('li');
        nametag.setAttribute('data-canvasname', wave['name']);
        nametag.setAttribute('class', 'list-group-item');
        if (wave['width'] > 1) {
          nametag.innerHTML = "<span class=\"icon node-icon glyphicon glyphicon-plus\"></span>";
        } else {
          nametag.innerHTML = "<span class=\"icon glyphicon\"></span>";
        }
        nametag.innerHTML += '<span>' + wave['name'] + '</span>';
        addDrag(nametag);
        namefragment.appendChild(nametag);
      }
      var xmargin = 0.5;
      var xpos;
      var ypos;
      var xend;
      if (wave['time'].indexOf(jsdata['time'][0]) == -1) {
        wave['time'].push(jsdata['time'][0]);
      }
      var timediffval = time_end - time_begin;
      var cwidth = canvas.width - 0;
      var wavecache = [];
      var ctx = canvas.getContext("2d");
      var beginindex = findlastless(wave['time'], time_begin);
      xpos = Math.floor((canvas.width - 0) * (wave['time'][beginindex] - timerange[0]) / timediffval) + xmargin;
      for (var i = beginindex, endindex = findlastless(wave['time'], time_end) + 1; i < endindex; i++) { 
        xend = Math.floor((canvas.width - 0) * (wave['time'][i + 1] - timerange[0]) / timediffval) + xmargin;
        switch (wave['state'][i]) {
        case 0:
          ypos = 20.5;
          wavecache.push([xpos, ypos, 0]);
          wavecache.push([xend, ypos, 0]);
          break;
        case 1:
          ypos = 20.5;
          wavecache.push([xpos, ypos, 1]);
          wavecache.push([xend, ypos, 1]);
          break;
        case 2:
          ypos = 30.5;
          wavecache.push([xpos, ypos, 2]);
          wavecache.push([xend, ypos, 2]);
          break;
        case 3:
          ypos = 10.5;
          wavecache.push([xpos, ypos, 2]);
          wavecache.push([xend, ypos, 2]);
          break;
        case 4:
          cl = get_bus_color(wave['wave'][i - 1]);
          draw_vline(ctx, xpos - 1, 10.5, 5, cl);
          draw_vline(ctx, xpos - 1, 30.5, -5, cl);
        case 5:
          //commented out actions provide better rendering effect (no blurring)
          //but takes a little more time to complete
          cl = get_bus_color(wave['wave'][i]);
          wavecache.push([xend, 30.5, 3]);
          wavecache.push([xpos, 30.5, cl]);
          //wavecache.push([xpos, 24.5, cl]);
          //wavecache.push([xpos-1, 24.5, cl]);
          wavecache.push([xpos - 1, 20.5, cl]);
          //wavecache.push([xpos-1, 16.5, cl]);
          //wavecache.push([xpos, 16.5, cl]);
          wavecache.push([xpos, 10.5, cl]);
          wavecache.push([xend, 10.5, cl]);
          if (xpos < 0) xpos = 0;
          write_text(ctx, xpos + 2, 24.5, wave['wave'][i], xend - xpos);
          break;
        }
xpos=xend;
      }
      var colourused = sig[ca].wavecolour;
      ctx.beginPath();
      ctx.strokeStyle = colourused[wavecache[0][2]];
      ctx.moveTo(wavecache[0][0], wavecache[0][1]);
      for (var i = 1; i < wavecache.length; i++) {
        if (wavecache[i][2] == 3) {
          ctx.moveTo(wavecache[i][0], wavecache[i][1]);
        }
        else if (wavecache[i][2] != wavecache[i-1][2]) {
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
        canvasfragment.appendChild(canvas);
      }
    }
  }
  var canvasl = $("#canvasl- ul")[0];
  var namel = $("#namel- ul")[0];
  //all elements are ready, add them to page
  if (flag_reset) {
    namel.appendChild(namefragment);
  }
  canvasl.appendChild(canvasfragment);
  var seps = document.getElementsByClassName('column-sep');
  seps[0].style.height = seps[0].parentNode.offsetHeight + 'px';
  seps[1].style.height = seps[1].parentNode.offsetHeight + 'px';
  CursorMover.$cursor.css({
    'height': seps[1].parentNode.offsetHeight
  });
  TimeBarManager.sync(time_begin, time_end, jsdata['time'][1]);
}
