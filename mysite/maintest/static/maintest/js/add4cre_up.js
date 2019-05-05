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
	
	return false; 
}

function user_submit_pack(obj){
	form_submit4reply(obj);
	$("#myModal_1").modal('hide');
	$("#myModal_2").modal('hide');
	return false;
}

function user_submit_pack4up(obj){
	form_submit4reply(obj);
	$("#myModal_1").modal('hide');
	$("#myModal_2").modal('hide');
	document.getElementById("filename").innerHTML = "";
	return false;
}

function clear_files(){
	document.getElementById("filename").innerHTML="";
}