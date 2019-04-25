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
      }
    });
  } else {
    $(".wavedrawing-").hide();
  }
  $("#wave-draw")[0].onclick = function() {
    fun().clearAllSignals();
    clearallchildren($("#canvasl- ul")[0]);
    clearallchildren($("#namel- ul")[0]);
    scrollbarmove().reset_to_default();
    $("canvas").each(addZoom);
  }
  $("#column-sep")[0].onclick = function(event) {}
  $("#width-")[0].onchange = function() {
    var p = this.value / this.max;
    var bar = scrollbarmove();
    bar.width = 0 | p * $('#canvasl-').width();
    if ($("#wave-draw").attr('disabled') != 'disabled') bar.changecanvas(false);
  }
  $("#propotion-")[0].oninput = function() {
    var propotion = this.value / this.max;
    var totaltime = get_json_data().time[0] - 0;
    var bar = scrollbarmove();
    var diff = bar.t_end - bar.t_begin;
    var newleft = propotion * (totaltime - diff);
    bar.t_begin = newleft;
    bar.t_end = bar.t_begin + diff;
    if ($("#wave-draw").attr('disabled') != 'disabled') bar.changecanvas(false);
  }
  $(":radio").click(function() {
    var $this = $(this);
    global_states().mode = $this.val();
    if ($this.val() == 0) {
      $('[type=range]').attr("disabled", 'disabled');
    } else if ($this.val() == 1) {
      $('[type=range]').attr("disabled", false);
    }
  });
  $(window).resize(function() {
    $("#width-")[0].onchange();
  });
});
