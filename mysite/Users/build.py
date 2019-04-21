import os
from django.http import JsonResponse

from Users.models import Users,Group,au4pj

DONE = 2

def build4group(request):
	from maintest.mytools.batch import batch_build
	username = request.session.get("username",None)
	group_id = request.session.get("group_id",None)
	au = request.session.get("au",None)
	if username:
		query = request.GET
		user = Users.objects.get(username=username)
		group = Group.objects.get(group_id=group_id)
		if au == "3" or au == "4":				
			#user = Users.objects.get(username=username)
			au4pj_item = au4pj.objects.get(group=group,pj_name=path,user=user)
			if au4pj_item.user_au4pj[2] == "0":
				return JsonResponse({"msg":"no access to build in this project!","type":"d"})
		path = query.get('path')[1:-1].split("/")		
		
		tfo_path = os.path.join("Users","all_groups",str(group_id))		
		for path_iter in path:
			tfo_path = os.path.join(tfo_path,path_iter)
		
		file_name = query.get('file_name')
				
		if not file_name.endswith('.tfo'):
			dir_list = os.listdir(tfo_path)
			tfo_list = []
			for iter in dir_list:
				if iter.endswith('.tfo'):
					tfo_list.append(iter)
			if len(tfo_list) != 1:
				return JsonResponse({"msg":"no tfo file or more than one tfo file in chosen location but you didn't choose one of them","type":"w"})
			else:
				file_name = tfo_list[0]
		
		tfo_path = request.session.get("tfo_path4group",tfo_path)
		file_name = request.session.get("tfo_name4group",file_name)
		
		print('initialization success!')
		batch_build(tfo_path, file_name)
		print('write success!')
		request.session['stream_status4group'][1][1] = DONE  # Build status
		return JsonResponse({"msg":"Build Success!","type":"s"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})