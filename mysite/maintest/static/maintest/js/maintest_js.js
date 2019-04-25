//document.write("Success import")

function loadProjectTemplate(name)
{
    alert("boom");
    document.getElementById("s-p-body").innerHTML="hello";

}

function loadXMLDoc_calc()
{
var xmlhttp;
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    document.getElementById("myAjax").innerHTML=xmlhttp.responseText;
    }
  }
//xmlhttp.open("GET","http://127.0.0.1:8000/maintest/arith_result/",true);
xmlhttp.open("GET","{% url 'maintest:arith_result' %}",true);
xmlhttp.send();
}

// file tree function
function loadTreeview(path, flag='C'){
  $.ajax({
    url: tv_ajax_url,
    async: true,
    data: {
      dir:path,
      flag:flag
    },
    success: function(data){
      generateFileTree(data);
    }
  });
}

function generateFileTree(tv_data){
  $("#tree").treeview({
    data: tv_data,
    enableLinks: true
  });
  $('#tree').treeview('collapseAll', { silent: true });
}

function treeviewOpenProject(tv_data_dir){
  $("#o-p-body").treeview({
    data: tv_data_dir,
    enableLinks: true
  });
  $('#o-p-body').treeview('collapseAll', { silent: true });
}

function changeWorkDir(alertmsg){
    var x1=location.toString();
if(x1.match(/path=(.*)/)){
        console.log('alter'+currentTVPath)
var n=x1.split('?');//n[0]: main url, n[1]: paras
var paras=n[1].split('&');//get paras
for (var i=0;i<paras.length;i++){
if(paras[i].substr(0,4)=='path'){
        console.log(i);paras[i]="path="+currentTVPath;break;}
}
x1=n[0]+"?path="+currentTVPath;
}
else{
x1+="?path="+currentTVPath;}
alert(alertmsg);
        location.assign(x1);
  }
//open project
$(document).ready(function(){
  $("#submit-o-p-path").click(function(){
    currentTVPath = $(".node-selected").text();
    changeWorkDir('successfully open project. moving to new page.');
  });
});


// flow function
function callFlowFunc(path){
  var url = check_url;
  console.log("check func start");
  console.log('url=',url);
  console.log('path=',path);
  $.ajax({
    url: url,
      async: true,
      data: {
        path: path
      },
      success: function(data){
        alert(data);
        console.log(location)//.reload();
      }
    });
}

function buildPattern(path){
  var url = build_url;
  console.log("build func start");
  console.log(url);
  $.ajax({
    url: url,
      async: true,
      data: {
        path: path
      },
      success: function(data){
        alert(data);
        //location.reload();
      }
    });
}

function runTest(path){
  var url = test_url;
  var rpt_name = $("#rptName").val();
  // waveform_path = waveform_path + rpt_name + ".jpg"
  console.log("Running test");
  console.log(url);
  $.ajax({
    url: url,
      async: true,
      data: {
        path: path,
        rpt_name: rpt_name
      },
      success: function(data){
        alert(data);
        // document.getElementById("waveform").src = waveform_path;
        console.log("change img src")
        //location.reload();
      }
    });
}
