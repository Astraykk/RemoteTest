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

//open project
$(document).ready(function(){
  $("#submit-o-p-path").click(function(){
    currentTVPath = $(".node-selected").text();
    //var dir = $("[data-nodeid='0']").attr("class");
    //console.log(currentTVPath);
    loadTreeview(currentTVPath);
    $('#open-project-modal').modal('hide')
  });
});