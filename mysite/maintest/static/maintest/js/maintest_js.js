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
  var tv_ajax_url="/maintest/tv_ajax/";
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
    enableLinks: true,
	onNodeSelected:function(event, data) {				
		//var addon = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"");
		//var addon = document.getElementById("project4open").value;
		var path = "";
		var path4del="";
		parentNode = $('#tree').treeview('getParent', data);
		while(parentNode.nodes){
			path = parentNode.text + "/" +path;
			Node = parentNode;
			parentNode = $('#tree').treeview('getParent', Node);
			
		}
		if(data.nodes){
			path += data.text + '/';
			path4del = path;
			document.getElementById("file_name4down").value = "";
		}else{
			path4del = path + data.text;
			document.getElementById("file_name4down").value = data.text;
			//document.getElementById("loc4edit").value = addon + "/" + path4del;
			//edit(addon + "/" + path,data.text);
		}
		/* path = "/" + path;
		path4del = "/" + path4del; */

		//document.getElementById("tfo_loc").value = addon + path;
		document.getElementById("file_loc").value = path;
		document.getElementById("dir_loc").value = path;
		document.getElementById("loc4del").value = path4del;
		document.getElementById("loc4down").value = path;
	},
  });
  $('#tree').treeview('collapseAll', { silent: true });
}

function treeviewOpenProject(tv_data_dir){
  $("#o-p-body").treeview({
    data: tv_data_dir,
    enableLinks: true,
	onNodeSelected:function(event, data) {
		var path = "";
		parentNode = $('#o-p-body').treeview('getParent', data);
		while(parentNode.nodes){
			path = parentNode.text + "/" +path;
			Node = parentNode;
			parentNode = $('#o-p-body').treeview('getParent', Node);
			
		}
		if(data.nodes){
			path += data.text + '/';
		}
		path = "/" + path;
		
		document.getElementById("project4open").value = path;
	}
	
  });
  $('#o-p-body').treeview('collapseAll', { silent: true });
}


//open project
$(document).ready(function(){
  $("#submit-o-p-path").click(function(){
    currentTVPath = $(".node-selected").text();
    $(".node-selected").removeClass("node-selected");
    //var dir = $("[data-nodeid='0']").attr("class");
    //console.log(currentTVPath);
    loadTreeview(currentTVPath);
    $('#open-project-modal').modal('hide')
  });
});


// flow function
//function callFlowFunc(url){
//  console.log('callFlow func start')
//  $.ajax({
//    url: url,
//      async: true,
//      success: function(data){
//        alert(data);
//        location.reload();
//      }
//    });
//}
function callFlowFunc(path){
  var url = check_url;
  console.log("check func start");
  console.log(url);
  var selected_tfo = $(".node-selected").text();
//  alert('current path = ' + currentTVPath);
//  var selected_tfo = $(".list-group").text();
//  alert(selected_tfo);
  $.ajax({
    url: url,
      async: true,
      data: {
        path: path,
        tfo: selected_tfo
      },
      success: function(data){
        alert(data);
//        alert('hello')
        location.reload();
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
        location.reload();
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
        location.reload();
      }
    });
}

function genTestReport(path){
  var url = report_url;
//  var rpt_name = $("#rptName").val();
  // waveform_path = waveform_path + rpt_name + ".jpg"
  console.log("Test report");
  console.log(url);
  $.ajax({
    url: url,
      async: true,
      data: {
        path: path,
//        rpt_name: rpt_name
      },
      success: function(data){
        alert(data);
        // document.getElementById("waveform").src = waveform_path;
//        console.log("change img src")
        location.reload();
      }
    });
}

function editText(path){
    console.log(' enter editText');
}