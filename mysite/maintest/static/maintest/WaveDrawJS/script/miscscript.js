$(document).ready(function() {
  flag_canvas_OK = check_canvas_availablity();
  if (uservcdfile.match('.vcd')) {
    var data = {
      vcd_file: uservcdfile
    };
    $.ajax({
      type: 'POST',
      url: vcd2pic_url,
      data: data,
      success: function(ret) {
        get_json_data(ret);
        scrollbarmove().reset_to_default();
        $("canvas").each(addZoom);
        ScorllSyncHelperClosure().calibrateTracking();
        global_states().mode = 0;
      }
    });
  } else {
    $(".wavedrawing-").hide();
  }
  $("#wavedraw-reset")[0].onclick = function() {
    fun().clearAllSignals();
    clearallchildren($("#canvasl- ul")[0]);
    clearallchildren($("#namel- ul")[0]);
    scrollbarmove().reset_to_default();
    $("canvas").each(addZoom);
    ScorllSyncHelperClosure().calibrateTracking();
    $("#wavedraw-zoom")[0].onclick();
    CursorMover.movetoX(0);
  };
  $("#width-")[0].onchange = function() {
    var p = this.value / this.max;
    var bar = scrollbarmove();
    bar.width = Math.floor(p * $('#canvasl-').width());
    bar.changecanvas(false);
  };
  $("#propotion-")[0].oninput = function() {
    var propotion = this.value / this.max;
    var totaltime = get_json_data().time[0] - 0;
    var bar = scrollbarmove();
    var diff = bar.t_end - bar.t_begin;
    var newleft = propotion * (totaltime - diff);
    bar.t_begin = newleft;
    bar.t_end = bar.t_begin + diff;
    CursorMover.movetoX(CursorMover.nowpos);
    bar.changecanvas(false);
  };
  $("#wavedraw-cursor")[0].onclick = function() {
    global_states().mode = 1;
    CursorMover.movetoX(CursorMover.nowpos);
    CursorMover.$cursor.css({
      'visibility': 'visible'
    });
    CursorMover.$info.css({
      'visibility': 'visible'
    });
  };
  $("#wavedraw-zoom")[0].onclick = function() {
    global_states().mode = 0;
    CursorMover.$cursor.css({
      'visibility': 'hidden'
    });
    CursorMover.$info.css({
      'visibility': 'hidden'
    });
  };
  $(window).resize(function() {
    $("#width-")[0].onchange();
  });
});
