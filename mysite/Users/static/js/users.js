function modify_email(){
	//var id=obj.id;
	//document.getElementById(id).style.display="none";
	document.getElementById("mod_email").style.display="none";
	//document.getElementById("mod_pwd").style.display="none";
	/* if(id == "mod_pwd"){
		document.getElementById("old_pwd").style.display="table-row";
		document.getElementById("new_pwd").style.display="table-row";
		document.getElementById("new_pwd2").style.display="table-row";
		
		document.getElementById("id_insert").innerHTML = "<input type=\"password\" class=\"tran\" name=\"old_pwd\" required oninvalid=\"setCustomValidity('password can\'t be empty!')\" oninput=\"setCustomValidity('')\">"
	}else{ */
	document.getElementById("email").disabled="";
	/* } */
	/* document.getElementById("back").style.display="inline";
	document.getElementById("save").style.display="inline"; */
}


function idcheck_sign_up(){
	
	var arg=/[^a-zA-Z0-9]/;
	var id=document.getElementById("id").value;
	if(id==null||id==""){
		document.getElementById("id").focus();
		document.getElementById("id_info").innerHTML = "username can't be empty!!!";
	}else if(arg.test(id)){
		document.getElementById("id").focus();
		document.getElementById("id_info").innerHTML = "only letters and digits are accepted!!!";
	}else if(id.length<3){
		document.getElementById("id").focus();
		document.getElementById("id_info").innerHTML = "username can't be shorter than 3!!!";
	}else{
		document.getElementById("id_info").innerHTML = "";
	}
}

function pwcheck_sign_up() {  
	var arg=/[^a-zA-Z0-9]/;
	var pwd=document.getElementById("pw1").value;
	var pwd2=document.getElementById("pw2").value;
	if(pwd==null||pwd==""){			
		document.getElementById("pw1").focus();
		document.getElementById("pw1_info").innerHTML = "password can't be empty!!!";
	}else if(arg.test(pwd)){
		document.getElementById("pw1").focus();
		document.getElementById("pw1_info").innerHTML = "only letters and digits are accepted!!!";
	}else if(pwd.length<6){
		document.getElementById("pw1").focus();
		document.getElementById("pw1_info").innerHTML = "password can't be shorter than 6!!!";
	}else if(pwd2!="" && pwd!=pwd2){
		document.getElementById("pw2_info").innerHTML = "two passwords should be same to each other!";
	}else{
		document.getElementById("pw1_info").innerHTML = "";
		document.getElementById("pw2_info").innerHTML = "";
	}
}

function pwcheck() {
	var arg=/[^a-zA-Z0-9]/;
	var pwd=document.getElementById("pw1").value;
	var pwd2=document.getElementById("pw2").value;
	if(pwd==null||pwd==""){			
		document.getElementById("pw1").focus();
		document.getElementById("label").style.display="table-row";
		document.getElementById("pw_info").innerHTML = "password can't be empty!!!";
	}else if(arg.test(pwd)){
		document.getElementById("pw1").focus();
		document.getElementById("label").style.display="table-row";
		document.getElementById("pw_info").innerHTML = "only letters and digits are accepted!!!";
	}else if(pwd.length<6){
		document.getElementById("pw1").focus();
		document.getElementById("label").style.display="block";
		document.getElementById("pw_info").innerHTML = "password can't be shorter than 6!!!";
	}else if(pwd2!="" && pwd!=pwd2){
		document.getElementById("label").style.display="table-row";
		document.getElementById("pw_info").innerHTML = "two passwords should be same to each other!";
	}else{
		document.getElementById("label").style.display="none";
		document.getElementById("pw_info").innerHTML = "";
	}
}

function check(){
	var pwd=document.getElementById("pw1").value;
	var pwd2=document.getElementById("pw2").value;
	if (pwd != pwd2){
		alert("two passwords should be same to each other!");
		return false;
	}else{
		return true;
	}
}

function get_log(){
	$.getJSON("/Users/log/",function(txt){
		log_list = txt.log;
		log="<thead><tr><th>behavior</th><th>object</th><th>time</th></tr></thead>";
		each_log="";
		for(var i = 0,len = log_list.length; i < len; i++){
			each_log = log_list[i].replace(/\|/g,"</td><td>")
			log += "<tr><td>"+each_log+"</td></tr>";
		}
		document.getElementById("log").innerHTML = log;
	});		
}




/* function getFilename(){
	var filename=document.getElementById("file").value;
	if(filename==undefined||filename==""){
	} else{
		var fn=filename.substring(filename.lastIndexOf("\\")+1);
		document.getElementById("filename").innerHTML+=fn+"<br>";
		//document.getElementById("filename").innerHTML=filename+"<br>";		
	}
} */

function getFilename(){
	var files=document.getElementById("file").files;
	var fn="";
	for(var i=0;i<files.length;i++){
		if(filename==undefined||filename==""){
		} else{
			fn=files[i].name.substring(files[i].name.lastIndexOf("\\")+1);
			document.getElementById("filename").innerHTML+=fn+"<br>";
			//document.getElementById("filename").innerHTML=filename+"<br>";		
		}
	}
}

function getUserProjectTree(){
	var path = "";
	$.get("/Nav/getTree/",{'path':path},function(tree,status){
		$('#project_tree').treeview({
			data: tree.data,
			collapseIcon:"glyphicon glyphicon-folder-open",
			expandIcon:"glyphicon glyphicon-folder-close",
			onNodeSelected:function(event, data) {
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

function getTree(){
	var path = document.getElementById("project4open").value;
	$.get("/Nav/getTree/",{'path':path},function(tree,status){
		$('#tree').treeview({
			data: tree.data,
			collapseIcon:"glyphicon glyphicon-folder-open",
			expandIcon:"glyphicon glyphicon-folder-close",
			onNodeSelected:function(event, data) {
				var path = "";
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
				}
				path = "/" + path;
				path4del = "/" + path4del;
				
				addon = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"");
				
				document.getElementById("tfo_loc").value = addon + path;
				document.getElementById("file_loc").value = addon + path;
				document.getElementById("dir_loc").value = addon + path;
				document.getElementById("loc4del").value = addon + path4del;
				document.getElementById("loc4down").value = addon + path;
			},
			onNodeUnselected:function(event,data){
				document.getElementById("file_loc").value = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"")+"/";
				document.getElementById("dir_loc").value = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"")+"/";
			}
		});
		$('#tree').treeview('collapseAll', { silent: true });
		
	});
			
}

function open_pj_pack(){
	getTree();
	$("#myModal_project").modal('hide');
}

function reply(obj){
	var form_id = obj.id.replace(/\/.*/,"");
	document.getElementById(form_id).action += obj.id + "/";
	document.getElementById(form_id).style.display="none";
	$("#"+form_id+"submit").click();
}

function del_file4user_pack(obj){
	form_submit4reply(obj);
	$("#myModal_del").modal('hide');
	window.setTimeout(function(){
		getTree();
	},100);
	document.getElementById("tfo_loc").value = "";
	document.getElementById("loc4del").value = "";
	document.getElementById("file_loc").value = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"");
	document.getElementById("dir_loc").value = document.getElementById("project4open").value.replace(/\/[^\/]*\/$/,"");
	document.getElementById("file_name4down").value = "";
	return false;	
}

function clear_files(){
	document.getElementById("filename").innerHTML="";
}
