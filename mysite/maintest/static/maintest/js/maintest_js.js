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

//function loadTreeview(path){
//  var tv_ajaxURL = "{% url 'maintest:tv_ajax' %}";
//  console.log(tv_ajaxURL)
//  htmlobj = $.ajax({url:tv_ajaxURL,async:false, data:{dir:path}});
//  console.log(typeof(htmlobj.responseText));
//  //console.log(htmlobj.responseText);
//  console.log("hello");
//  json = $.parseJSON(htmlobj.responseText);
//  console.log(typeof(json));
//  $("#tree").treeview({data:json});
//  $('#tree').treeview('collapseAll', { silent: true });
//}