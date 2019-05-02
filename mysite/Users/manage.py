from Users.models import Users,Group,Group_item,au4group,au4pj
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from Users.group import path_parse


def index(request,group_id=0):
	username = request.session.get('username',None)
	context = {}
	if username:
		if group_id:
			user = Users.objects.get(username=username)
			group = Group.objects.get(group_id=group_id)
			group_item = Group_item.objects.get(group_id=group,member=user)
			context["au"] = group_item.authority
			context["group_name"] = group.group_name
			if group_item.authority == "4":
				return render(request,"Manage/no_access.html")			
			
			request.session["group_id"] = group_id
			request.session["group_name"] = group.group_name
			request.session["authority"] = group_item.authority
			request.session["au"] = group_item.authority
			#------------------------
			have_or = au4group.objects.filter(group_id=group_id)
			if not have_or:
				new = au4group(group_id=group_id)
				new.save()
			au4group_item = au4group.objects.get(group_id=group_id)
			if group_item.authority == "1":
				request.session["au4group"] = "11111"
			elif group_item.authority == "2":
				request.session["au4group"] = au4group_item.au4admin 
			elif group_item.authority == "3":
				request.session["au4group"] = au4group_item.au4pj_admin
			else:
				request.session["au4group"] = "00000"
			#--------------------------------------------------------
		else:
			id = request.session.get('group_id',None)
			if id:
				return index(request,id)
			else:
				return redirect("/Users/login");
		
		return render(request,"Manage/index.html",context)
	else:
		return redirect("/Users/login");
		
def group_au_settings(request):
	group_id = request.session.get('group_id',None)
	au_list = []
	if group_id:
		#----------------------------------
		have_or = au4group.objects.filter(group_id=group_id)
		if not have_or:
			new = au4group(group_id=group_id)
			new.save()
		au4group_item = au4group.objects.get(group_id=group_id)
		au4ad = '_'.join(au4group_item.au4admin).split('_')
		au4pj_ad = '_'.join(au4group_item.au4pj_admin).split('_')
		for i in range(len(au4ad)):
			if au4ad[i] == '1':
				au_list.append("au4admin"+str(i+3))
		
		for i in range(len(au4pj_ad)):
			if au4pj_ad[i] == '1':
				au_list.append("au4pj_ad"+str(i+3))
		return JsonResponse({"au_list":au_list})
	else:
		return JsonResponse({"msg":"emmmm"})
		




def au_update(request):
	group_id = request.session.get('group_id',None)
	au4admin_list = ['0','0','0','0','0']
	au4pj_ad_list = ['0','0','0','0','0']
	if group_id:
		au4admin = request.POST.getlist("au4admin")
		au4pj_ad = request.POST.getlist("au4pj_ad")
		for index in au4admin:
			au4admin_list[int(index)] = '1'
		for index in au4pj_ad:
			au4pj_ad_list[int(index)] = '1'
		au4group_item = au4group.objects.get(group_id=group_id)
		au4group_item.au4admin = ''.join(au4admin_list)
		au4group_item.au4pj_admin = ''.join(au4pj_ad_list)
		au4group_item.save()
		return JsonResponse({"msg":"Update authority settings successfully!","type":"s"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})
		
		
def change_au(request):
	username = request.session.get('username',None)
	au = request.session.get('authority',None)
	if username:
		return render(request,"Manage/change_au.html",{"au":au,"group_name":request.session.get("group_name")})
	else:
		return redirect("/Users/login/")

def memlist(request):
	au4group = request.session.get('au4group',None)
	context = {}
	members = []
	if au4group:
		au4 = "_".join(au4group).split("_")
		if au4[3] == "1":
			group_id = request.session.get('group_id',None)
			group = Group.objects.get(group_id = group_id)
			group_set = Group_item.objects.filter(group_id = group).order_by("authority")
			for iter in group_set:
				members.append({"username":iter.member.username, "authority":iter.authority})
			context["members"] = members
			context["au"] = request.session.get('authority',None)
			return render(request,"Manage/memlist.html",context)
		else:
			return render(request,"Manage/no_access.html")
	else:
		return redirect("/Users/login/")
		
def change_au4member(request):
	group_id = request.session.get('group_id',None)
	if group_id:
		user4ch = request.POST.get('username')
		au4g_new = request.POST.get('au4g_new')
		# if int(au4g_new) > int(request.session.get('au')):
			# return JsonResponse({"msg":"no access to change "+user4ch+"'s authority successfully!","type":"d"})
		# else:
		member = Users.objects.get(username=user4ch)
		group_item = Group_item.objects.get(group_id=group_id,member=member)
		group_item.authority = au4g_new
		group_item.save()
		return JsonResponse({"msg":"change "+user4ch+"'s authority successfully!","type":"s"})
	else:
		return redirect("/Users/login/")
		
def delete_member(request):
	group_id = request.session.get('group_id',None)
	au = request.session.get('au',None)
	if group_id:
		au4group_item = au4group.objects.get(group_id=group_id)
		if au == "2" and au4group_item.au4admin[2] == "0":
			return JsonResponse({"msg":"You have no access to delete members!","type":"d"})
		if au == "3" and au4group_item.au4pj_admin[2] == "0":
			return JsonResponse({"msg":"You have no access to delete members!","type":"d"})
		if au == "4":
			return JsonResponse({"msg":"You have no access to delete members!","type":"d"})
		username = request.POST.get("username",None)
		group = Group.objects.get(group_id=group_id)
		user = Users.objects.get(username=username)
		au4pj.objects.filter(group=group,user=user).delete()
		Group_item.objects.get(member=user,group_id=group).delete()
		return JsonResponse({"msg":"delete "+username+"from group successfully!","type":"s"})
	else:
		return redirect("/Users/login/")
		
def memlist4del(request):
	au4group = request.session.get('au4group',None)
	context = {}
	members = []
	if au4group:
		au4 = "_".join(au4group).split("_")
		if au4[2] == "1":
			group_id = request.session.get('group_id',None)
			group = Group.objects.get(group_id = group_id)
			group_set = Group_item.objects.filter(group_id = group).order_by("authority")
			for iter in group_set:
				members.append({"username":iter.member.username, "authority":iter.authority})
			context["members"] = members
			context["au"] = request.session.get('authority',None)
			return render(request,"Manage/memlist4del.html",context)
		else:
			return render(request,"Manage/no_access.html")
	else:
		return redirect("/Users/login/")
		
def au4pj_change(request):
	group_id = request.session.get('group_id',None)
	username = request.session.get('username',None)
	au = request.session.get('au',None)
	au4pj_list = ["0","0","0"]
	if group_id and username:
		file_loc = request.POST.get("file_loc")

		if file_loc == "/":
			return JsonResponse({"msg":"choose dir first!","type":"w"})
		target_username = request.POST.get("username",None)
		au4pj_box_list = request.POST.getlist("au4pj")
		group = Group.objects.get(group_id = group_id)
		target_user = Users.objects.get(username=target_username)			
		au4pj_item = au4pj.objects.get(group=group,pj_name=file_loc,user=target_user)
		
		if au == "1" or au == "2":
			for index in au4pj_box_list:
				au4pj_list[int(index)] = "1"
			bool = True
		else:
			user = Users.objects.get(username=username)
			#----------------------
			bool = False
			# path_parse_list = path_parse(file_loc)
			# for iter in path_parse_list:
			au4pj_host = au4pj.objects.get(group=group,pj_name=file_loc,user=user)
			for index in au4pj_box_list:
				if au4pj_host.user_au4pj[int(index)] == "1":
					au4pj_list[int(index)] = "1"
					bool = True
				else:
					bool = False
					return JsonResponse({"msg":"You have no access or you just have some of access to this dir!","type":"w"})
		if bool:
			au4pj_item.user_au4pj = ''.join(au4pj_list)
			au4pj_item.save()
			
			au4pj_item_sub = au4pj.objects.filter(group=group,user=target_user,pj_name__regex="^"+file_loc)
			for iter in au4pj_item_sub:
				iter.user_au4pj = ''.join(au4pj_list)
				iter.save()
			return JsonResponse({"msg":"change "+ target_username +"'s authority of dir successfully!","type":"s"})
		else:
			return JsonResponse({"msg":"You have no access or you just have some of access to this dir!","type":"w"})
		
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"d"})

def mem_au4pj(request):
	group_id = request.session.get("group_id")
	path = request.GET.get("path")
	au_list4checked = []
	au_list4unchecked = []
	if group_id:	
		group = Group.objects.get(group_id=group_id)
		group_item_4pj_ad = Group_item.objects.filter(group_id = group,authority="3")
		group_item_4od_mem = Group_item.objects.filter(group_id = group,authority="4")
		group_item = group_item_4pj_ad | group_item_4od_mem
		for iter in group_item:
		#-------------------------------------------------------------------
			au4pj_set = au4pj.objects.filter(user=iter.member,pj_name=path)
			if au4pj_set:
				au4pj_item = au4pj_set[0]
			else:
				au4pj_item = au4pj(group=group,user=iter.member,pj_name=path,user_au4pj="000")
				au4pj_item.save()
		#-------------------------------------------------------	
			index = 0
			for i in "_".join(au4pj_item.user_au4pj).split("_"):
				if i == "1":
					au_list4checked.append(au4pj_item.user.username+"_"+str(index))						
				else:
					au_list4unchecked.append(au4pj_item.user.username+"_"+str(index))
				index += 1
		return JsonResponse({"au_list4checked":au_list4checked,"au_list4unchecked":au_list4unchecked})
				
	else:
		return JsonResponse({"msg":"emmm"})
		
def pj_au(request):
	group_id = request.session.get('au4group',None)
	if group_id:
		return render(request,"Manage/au4project.html")
	else:
		return render(request,"Manage/expired.html")
		
		
def pj_au_ml(request):
	group_id = request.session.get('au4group',None)
	context = {}
	members = []
	if group_id:
		group_id = request.session.get('group_id',None)
		group = Group.objects.get(group_id = group_id)
		group_set = Group_item.objects.filter(group_id = group).order_by("authority")
		for iter in group_set:
			members.append({"username":iter.member.username, "authority":iter.authority})
		context["members"] = members
		context["au"] = request.session.get('authority',None)
		return render(request,"Manage/au4pj_list.html",context)
	else:
		return render(request,"Manage/expired.html")
		


			