
function mem_au4pj_get(path){
	$.get("/Users/mem_au4pj/",{"path":path},function(au,status){
		var au_list4checked = au.au_list4checked;
		var au_list4unchecked = au.au_list4unchecked;
		if(au.msg){
			alert("Your session has expired, please relogin first!");
			window.location.href="/Users/login/";
		}
		for(var i=0;i<au_list4checked.length;i++){
			document.getElementById(au_list4checked[i]).checked = true;
		}
		for(var i=0;i<au_list4unchecked.length;i++){
			document.getElementById(au_list4unchecked[i]).checked = false;
		}
	});
}

function getGroupProjectTree(){
	var path = "";
	$.get("/Nav/getGroupTree/",{'path':path},function(tree,status){
		$('#project_tree').treeview({
			data: tree.data,
			collapseIcon:"glyphicon glyphicon-folder-open",
			expandIcon:"glyphicon glyphicon-folder-close",
			emptyIcon:"glyphicon glyphicon-file",
			onNodeSelected:function(event, data){
				var path = "";
				parentNode = $('#project_tree').treeview('getParent', data);
				while(parentNode.nodes){
					path = parentNode.text + "/" +path;
					Node = parentNode;
					parentNode = $('#project_tree').treeview('getParent', Node);
					
				}
				if(data.nodes){
					path += data.text + '/';
				}
				path = "/" + path;
				document.getElementById("project4open").value = path;
				
			}
		});
		$('#project_tree').treeview('collapseAll', { silent: true });
		
	});
			
}

function getGroupTree(){
	var path = document.getElementById("project4open").value;
	$.get("/Nav/getGroupTree/",{'path':path},function(tree,status){
		$('#tree').treeview({
			data: tree.data,
			collapseIcon:"glyphicon glyphicon-folder-open",
			expandIcon:"glyphicon glyphicon-folder-close",
			emptyIcon:"glyphicon glyphicon-file",
			onNodeSelected:function(event, data){
				var path = "";
				var path4del;
				var addon = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"");
				parentNode = $('#tree').treeview('getParent', data);
				while(parentNode.nodes){
					path = parentNode.text + "/" +path;
					Node = parentNode;
					parentNode = $('#tree').treeview('getParent', Node);
					
				}
				if(data.nodes){
					path += data.text + '/';
					path4del = path;
				}else{
					path4del = path + data.text;
					document.getElementById("file_name4down").value = data.text;
					document.getElementById("tfo_name").value = data.text;
					document.getElementById("loc4edit").value = addon + "/" + path4del;
					edit4group(addon + "/" + path,data.text);
				}
				path = "/" + path;
				path4del = "/" + path4del;
				
				
				
				document.getElementById("tfo_loc").value = addon + path;
				document.getElementById("file_loc").value = addon + path;
				document.getElementById("dir_loc").value = addon + path;
				document.getElementById("loc4del").value = addon + path4del;
				document.getElementById("loc4down").value = addon + path;
				
				//$('#tree').treeview('mem_au4pj_get', path);  
				//mem_au4pj_get(path);
				//alert("aa");
				
			},
			onNodeUnselected:function(event,data){
				document.getElementById("file_loc").value = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"")+"/";
				document.getElementById("dir_loc").value = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"")+"/";
			}
		});
		$('#tree').treeview('collapseAll', { silent: true });
		
	});
	stream4group_get();		
}

function open_pj4group_pack(){
	getGroupTree();
	$("#myModal_project").modal('hide');
}


function getGroupTree4au(){
	var path = "";
	$.get("/Nav/getGroupTree/",{'path':path},function(tree,status){
		$('#tree').treeview({
			data: tree.data,
			collapseIcon:"glyphicon glyphicon-folder-open",
			expandIcon:"glyphicon glyphicon-folder-close",
			emptyIcon:"glyphicon glyphicon-file",
			onNodeSelected:function(event, data){
				var path = "";
				parentNode = $('#tree').treeview('getParent', data);
				while(parentNode.nodes){
					path = parentNode.text + "/" +path;
					Node = parentNode;
					parentNode = $('#tree').treeview('getParent', Node);
					
				}
				if(data.nodes){
					visitAllNodes(data,"/"+path);
					path += data.text + '/';					
				}
				path = "/" + path;
				//document.getElementById("dir_loc").value = path;
				var file_locs = document.getElementsByName("file_loc");
				for(var i=0;i<file_locs.length;i++){
					file_locs[i].value = path;
				}
				//document.getElementById("tfo_loc").value = path;
				
				mem_au4pj_get(path);
				//alert("aa");
				
			},
			onNodeUnselected:function(event,data){
				var file_locs = document.getElementsByName("file_loc");
				for(var i=0;i<file_locs.length;i++){
					file_locs[i].value = path;
				}
			}
			
		});
		$('#tree').treeview('collapseAll', { silent: true });
		
	});
			
}

function visitAllNodes(node,path){
	if(node.nodes){
		var path4recursion = path;
		path4recursion += node.text + "/";
		$.get("/Users/mem_au4pj/",{"path":path4recursion},function(au,status){});
		for(var i=0;i<node.nodes.length;i++){
			visitAllNodes(node.nodes[i],path4recursion);
		}
	}else{
		return true;
	}
}

function form_submit4reply(obj) { 
	var form_id = "#" + obj.id;

	$(form_id).ajaxSubmit(function(message) { 

		inner = "<div style=\"margin:0px\" class=\"alert ";
		c_button = " alert-dismissable\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\"> &times; </button>";
		if(message.type == "s"){
			inner += "alert-success";
		}else if(message.type == "i"){
			inner += "alert-info";
		}else if(message.type == "w"){
			inner += "alert-warning";
		}else{
			inner += "alert-danger";
		}
		document.getElementById("message").innerHTML = inner + c_button + message.msg + "</div>";
		window.setTimeout(function(){
			$('[data-dismiss="alert"]').alert('close');
		},3000);
		
	}); 
	
	return false; //  
}

function form_submit(obj) { 
	form_submit4reply(obj);
	$("#myModal_1").modal('hide');
	$("#myModal_2").modal('hide');
	$("#myModal_add").modal('hide');
	
	window.setTimeout(function(){
		getGroupTree();
	},100);
	return false; //  
}

function form_submit4up(obj) { 
	form_submit4reply(obj);
	$("#myModal_1").modal('hide');
	$("#myModal_2").modal('hide');
	$("#myModal_add").modal('hide');
	
	window.setTimeout(function(){
		getGroupTree();
	},1000);
	return false; //  
}

function au4pj_change_pack(obj){
	form_submit4reply(obj);
	window.setTimeout(function(){
		path = document.getElementById("file_loc").value;
		mem_au4pj_get(path);
	},100);
	return false;
}

function test4m_pack(obj){
	form_submit4reply(obj);
	$("#myModal_test").modal('hide');
	return false;	
}

function down_file_pack(){
	$("#myModal_down").modal('hide');
}

function del_file_pack(obj){
	form_submit4reply(obj);
	$("#myModal_del").modal('hide');
	window.setTimeout(function(){
		getGroupTree();
	},100);
	document.getElementById("tfo_loc").value = "";
	document.getElementById("loc4del").value = "";
	document.getElementById("file_loc").value = "/";
	document.getElementById("dir_loc").value = "/";
	document.getElementById("file_name4down").value = "";
	return false;	
}


function user_submit_pack(obj){
	form_submit4reply(obj);
	window.setTimeout(function(){
		getTree();
	},100);
	$("#myModal_1").modal('hide');
	$("#myModal_2").modal('hide');
	return false;
}

function user_submit_pack4up(obj){
	form_submit4reply(obj);
	window.setTimeout(function(){
		getTree();
	},1000);
	$("#myModal_1").modal('hide');
	$("#myModal_2").modal('hide');
	document.getElementById("filename").innerHTML = "";
	return false;
}


function au_check(){
	var array4au = document.getElementsByName("au4admin");
	var array4pj = document.getElementsByName("au4pj_ad");
	for(var i=0;i<array4au.length;i++){
		array4au[i].checked = false;
	}
	for(var i=0;i<array4pj.length;i++){
		array4pj[i].checked = false;
	}
	$.getJSON("/Users/group_au_settings/",function(au){
		var au_list = au.au_list;
		if(au.msg){
			alert("Your session has expired, please relogin first!");
			window.location.href="/Users/login/";
		}
		for(var i=0;i<au_list.length;i++){
			document.getElementById(au_list[i]).checked = true;
		}
	});
}





function au_set_pack(obj){
	form_submit4reply(obj);
	//au_check();
	return false;
}



function d2pjad(obj){
	var form_id = "form_id_"+obj.id.replace(/_.*/,"");
	var au4g_id = "au4g_"+obj.id.replace(/_.*/,"");
	document.getElementById(au4g_id).value = "3";
	$("#"+form_id+"_click").click();
}

function p2ad(obj){
	var form_id = "form_id_"+obj.id.replace(/_.*/,"");
	var au4g_id = "au4g_"+obj.id.replace(/_.*/,"");
	document.getElementById(au4g_id).value = "2";
	$("#"+form_id+"_click").click();
	
}

function d2odmem(obj){
	var form_id = "form_id_"+obj.id.replace(/_.*/,"");
	var au4g_id = "au4g_"+obj.id.replace(/_.*/,"");
	document.getElementById(au4g_id).value = "4";
	$("#"+form_id+"_click").click();
	
}

function au4mem(obj){
	form_submit4reply(obj);
	window.setTimeout(function(){
		$.get("/Users/change_au_memlist/",function(data,status){
			$("#memlist").html(data);
		});
	},100);
	return false;
}


function change_au(){
	$.get("/Users/change_au_memlist/",function(data,status){
		$("#memlist").html(data);
	});
}

function mem4del(){
	$.get("/Users/memlist4del/",function(data,status){
		$("#memlist").html(data);
	});
}

function del_mem_pack(obj){
	form_submit4reply(obj);
	window.setTimeout(function(){
		$.get("/Users/memlist4del/",function(data,status){
			$("#memlist").html(data);
		});
	},100);
	return false;
}

function span_click(obj){
	var form_id = "form_id_"+obj.id.replace(/_.*/,"");
	$("#"+form_id+"_click").click();
}

function pj_au(){
	$.get("/Users/pj_au/",function(data,status){
		$("#memlist").html(data);
	});
	window.setTimeout(function(){
		getGroupTree4au();
		$.get("/Users/pj_au_ml/",function(data,status){
			$("#au4pj_list").html(data);
		});
	},100);
}

function save4group(obj){
	form_submit4reply(obj);
	window.setTimeout(function(){
		stream4group_get();
	},100);
	return false;
}

function edit4group(path,file_name){
	var url = "/Nav/edit_file4group/";
	document.getElementById("file4edit").innerHTML = file_name;
	$.ajax({
		url: url,
		async: true,
		data: {
			path: path,
			file_name: file_name,
		},
		success: function(data){
			$("#insert4edit").html(data);						
		}
    });
}

function check4group(){
	var url = "/Users/check4group/";
	var path = $("#tfo_loc").val();
	var file_name = $("#file_name4down").val();
	document.getElementById("file4edit").value = file_name;
	$.ajax({
		url: url,
		async: true,
		data: {
			path: path,
			file_name: file_name,
		},
		success: function(message){
			inner = "<div style=\"margin:0px\" class=\"alert ";
			c_button = " alert-dismissable\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\"> &times; </button>";
			if(message.type == "s"){
				inner += "alert-success";
			}else if(message.type == "i"){
				inner += "alert-info";
			}else if(message.type == "w"){
				inner += "alert-warning";
			}else{
				inner += "alert-danger";
			}
			document.getElementById("message").innerHTML = inner + c_button + message.msg + "</div>";
			stream4group_get();
			window.setTimeout(function(){
				$('[data-dismiss="alert"]').alert('close');
			},3000);      
		}
    });
}

function build4group(){
	var url = "/Users/build4group/";
	var path = $("#tfo_loc").val();
	var file_name = $("#file_name4down").val();
	document.getElementById("file4edit").value = file_name;
	$.ajax({
		url: url,
		async: true,
		data: {
			path: path,
			file_name: file_name,
		},
		success: function(message){
			inner = "<div style=\"margin:0px\" class=\"alert ";
			c_button = " alert-dismissable\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\"> &times; </button>";
			if(message.type == "s"){
				inner += "alert-success";
			}else if(message.type == "i"){
				inner += "alert-info";
			}else if(message.type == "w"){
				inner += "alert-warning";
			}else{
				inner += "alert-danger";
			}
			document.getElementById("message").innerHTML = inner + c_button + message.msg + "</div>";
			stream4group_get();
			window.setTimeout(function(){
				$('[data-dismiss="alert"]').alert('close');
			},3000);      
		}
    });
}


function report4group(){
	var url = "/Users/report4group/";
	var path = $("#tfo_loc").val();
	var file_name = $("#file_name4down").val();
	document.getElementById("file4edit").value = file_name;
	$.ajax({
		url: url,
		async: true,
		data: {
			path: path,
			file_name: file_name,
		},
		success: function(message){
			inner = "<div style=\"margin:0px\" class=\"alert ";
			c_button = " alert-dismissable\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\"> &times; </button>";
			if(message.type == "s"){
				inner += "alert-success";
			}else if(message.type == "i"){
				inner += "alert-info";
			}else if(message.type == "w"){
				inner += "alert-warning";
			}else{
				inner += "alert-danger";
			}
			document.getElementById("message").innerHTML = inner + c_button + message.msg + "</div>";
			stream4group_get();
			window.setTimeout(function(){
				$('[data-dismiss="alert"]').alert('close');
			},3000);      
		}
    });
}

function stream4group_get(){
	$.get("/Users/stream4group_get/",function(data,status){
		$("#stream4group").html(data);
	});
}
