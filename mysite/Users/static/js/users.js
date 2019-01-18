function modify_info(obj){
	var id=obj.id;
	//document.getElementById(id).style.display="none";
	document.getElementById("mod_email").style.display="none";
	document.getElementById("mod_pwd").style.display="none";
	if(id == "mod_pwd"){
		document.getElementById("old_pwd").style.display="table-row";
		document.getElementById("new_pwd").style.display="table-row";
		document.getElementById("new_pwd2").style.display="table-row";
		
		document.getElementById("id_insert").innerHTML = "<input type=\"password\" class=\"tran\" name=\"old_pwd\" required oninvalid=\"setCustomValidity('password can\'t be empty!')\" oninput=\"setCustomValidity('')\">"
	}else{
		document.getElementById("email").disabled="";
	}
	document.getElementById("back").style.display="inline";
	document.getElementById("save").style.display="inline";
}


function idcheck_sign_up(){
	
	var arg=/[^a-zA-Z0-9]/;
	var id=document.getElementById("id").value;
	if(id==null||id==""){
		document.getElementById("id").focus();
		document.getElementById("id_info").innerHTML = "username can't be empty!！！！！";
	}else if(arg.test(id)){
		document.getElementById("id").focus();
		document.getElementById("id_info").innerHTML = "only letters and digits are accepted！！！！";
	}else if(id.length<3){
		document.getElementById("id").focus();
		document.getElementById("id_info").innerHTML = "username can't be shorter than 3！！！";
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
		document.getElementById("pw1_info").innerHTML = "password can't be empty!！！！";
	}else if(arg.test(pwd)){
		document.getElementById("pw1").focus();
		document.getElementById("pw1_info").innerHTML = "only letters and digits are accepted！！！";
	}else if(pwd.length<6){
		document.getElementById("pw1").focus();
		document.getElementById("pw1_info").innerHTML = "password can't be shorter than 6！！！";
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
		document.getElementById("pw_info").innerHTML = "password can't be empty!！！！";
	}else if(arg.test(pwd)){
		document.getElementById("pw1").focus();
		document.getElementById("label").style.display="table-row";
		document.getElementById("pw_info").innerHTML = "only letters and digits are accepted！！！";
	}else if(pwd.length<6){
		document.getElementById("pw1").focus();
		document.getElementById("label").style.display="table-row";
		document.getElementById("pw_info").innerHTML = "password can't be shorter than 6！！！";
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
		log="";
		for(var i = 0,len = log_list.length; i < len; i++){
			log += log_list[i]+"<br>";
		}
		document.getElementById("log").innerHTML = log;
	});		
}




function getFilename(){
	var filename=document.getElementById("file").value;
	if(filename==undefined||filename==""){
	} else{
	  var fn=filename.substring(filename.lastIndexOf("\\")+1);
	  document.getElementById("filename").innerHTML+=fn+"<br>"; 
	}
}