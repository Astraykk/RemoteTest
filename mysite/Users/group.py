from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,FileResponse
from Users.models import Users,Group,Group_item,Invitation,au4pj,au4group
from django.core.exceptions import ObjectDoesNotExist
import os
import shutil

DONE = 2
LOADING = 1
UNDONE = 0

status = [
	["Check", UNDONE],
	["Build", UNDONE],
	["Test", UNDONE],
	["Report", UNDONE]
]


def index(request):
	username = request.session.get('username',None)
	if username:
		return my_group(request)
	else:
		return redirect('/Users/login/')
		
def my_group(request):
	username = request.session.get('username',None)
	context = {}
	groups = []
	if username:
		#group_set = Group_item.objects.filter(member__username=username).values("group_id","group_name")
		group_set = Group_item.objects.filter(member__username=username,authority=1).values("group_id")
		for iter in group_set:
			group_iter = Group.objects.filter(group_id=iter["group_id"])
			groups.append({"group_id":iter["group_id"],"group_name":group_iter[0].group_name})
			#print(iter["group_id"])
		
		context["groups"]=groups
		return render(request,"Group/my_group.html",context)
	else:
		return redirect('/Users/login/')

def create_group(request):
	username = request.session.get('username',None)
	if username:
		user = Users.objects.get(username=username)
		if request.method == "POST":
			group_name = request.POST.get("group_name")
			group = Group(group_name=group_name)
			group.save()
			group_item = Group_item(group_id=group,member=user,authority=1)
			group_item.save()
			#------------------
			path = "Users/all_groups/"+str(group.group_id)
			os.mkdir(path)
			return JsonResponse({"msg":"successfully create a group!","type":"s"})
	else:
		return redirect('/Users/login/')

def go2group(request,group_id):
	username = request.session.get('username',None)
	context = {}
	members = []
	if username:
		request.session['group_id']=group_id
		user = Users.objects.get(username=username)
		group = Group.objects.get(group_id = group_id)
		group_item = Group_item.objects.get(group_id=group,member=user)
		request.session["au"] = group_item.authority
		context["au"] = group_item.authority
		group_set = Group_item.objects.filter(group_id = group).order_by("authority")
		for iter in group_set:
			members.append({"username":iter.member.username, "authority":iter.authority})
		context["group_name"] = group.group_name
		context["members"] = members
		return render(request,"Group/Agroup.html",context)
	else:
		return redirect('/Users/login/')

def create_group_project(request):
	username = request.session.get('username',None)
	group_id = request.session.get('group_id',None)
	au = request.session.get('au',None)
	if username and group_id:
		dir_loc = request.POST.get("dir_loc", None)
		dir_name = request.POST.get("dir_name", None)
		if au != "1":
			au4group_item = au4group.objects.get(group_id=group_id)
		if au == "2" and au4group_item.au4admin[0] == "0":
			return JsonResponse({"msg":"You have no access to create!","type":"d"})
		if au == "3" and au4group_item.au4pj_admin[0] == "0":
			return JsonResponse({"msg":"You have no access to create!","type":"d"})
		if au == "4":
			return JsonResponse({"msg":"You have no access to create!","type":"d"})
		path = "Users/all_groups/" + str(group_id) + dir_loc + dir_name
		try:
			os.mkdir(path)
		except OSError:
			return JsonResponse({"msg":"Failed in create!","type":"d"})
		else:
			group = Group.objects.get(group_id=group_id)
			user = Users.objects.get(username=username)
			au4pj_item = au4pj(group=group,user=user,pj_name=dir_loc+dir_name+"/",user_au4pj="111",tag=True)
			au4pj_item.save()
			return JsonResponse({"msg":"Create successfully!","type":"s"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})

def upload(request):
	username = request.session.get('username',None)
	group_id = request.session.get('group_id',None)
	au = request.session.get('au',None)
	if username and group_id:
		dirname = request.POST.get('file_loc',None)
		path = str(group_id) + dirname;
		if au == "3" or au == "4":
			group = Group.objects.get(group_id=group_id)
			user = Users.objects.get(username=username)
			#path_parse_list = path_parse(dirname)
			#bool = False
			# for iter in path_parse_list:
				# au4pj_item = au4pj.objects.filter(group=group,pj_name=iter,user=user)
				# if au4pj_item:
					# if "_".join(au4pj_item[0].user_au4pj).split("_")[1] == "1":
						# bool = True
						# break
			au4pj_item = au4pj.objects.get(group=group,pj_name=dirname,user=user)
			if au4pj_item.user_au4pj[1] == "0":
			#if not bool:
				return JsonResponse({"msg":"no access to upload to this dir!","type":"d"})
			
		files = request.FILES.getlist("myfile")
		for file in files:
			with open("Users/all_groups/%s%s" % (path,file.name),'wb') as fp:
				for chunk in file.chunks():
					fp.write(chunk)
				fp.close()
				#create_history(username,"upload file",file.name)
		if len(files):	
			return JsonResponse({"msg":"Upload successfully!","type":"s"})
		else:
			return JsonResponse({"msg":"Please select files to upload!","type":"w"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})
	
def invite(request):
	username = request.session.get('username',None)
	group_id = request.session.get('group_id',None)
	au = request.session.get("au",None)
	if username and group_id:
		invitee_name = request.POST.get('invitee_name',None)
		invitee_au = request.POST.get('invitee_au',None)
		notes = request.POST.get('notes',None)
		au4group_item = au4group.objects.get(group_id=group_id)
		if au == "2" and au4group_item.au4admin[2] == "0":
			return JsonResponse({"msg":"You have no access to invite others!","type":"d"})
		if au == "3" and au4group_item.au4pj_admin[2] == "0":
			return JsonResponse({"msg":"You have no access to invite others!","type":"d"})
		if au == "4":
			return JsonResponse({"msg":"You have no access to invite others!","type":"d"})
		
		try:
			invitee = Users.objects.get(username=invitee_name)
		except ObjectDoesNotExist:
			return JsonResponse({"msg":"No user called "+ invitee_name,"type":"d"})
		else:
			invited_or = Invitation.objects.filter(invitee=invitee,group_id=group_id)
			if invited_or:
				msg = invitee_name + " has been invited to this group by someone before. Please wait for reply patiently!"
				return JsonResponse({"msg":msg,"type":"i"})
			else:
				in_or = Group_item.objects.filter(member=invitee,group_id=group_id)
				if in_or:
					msg = invitee_name + " is in this group now!"
				else:
					invitation = Invitation(invitee=invitee,group_id=group_id,inviter_name=username,invitee_au=invitee_au,notes=notes)
					invitation.save()
					msg = "Invitation has been sent to " + invitee_name +"."
				return JsonResponse({"msg":msg,"type":"s"})
			
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})

def reply_inv(request,group_id,reply,au):
	username = request.session.get('username',None)
	if username:
		user = Users.objects.get(username=username)
		if reply == "yes":			
			group = Group.objects.get(group_id = group_id)
			in_or = Group_item.objects.filter(member=user,group_id=group_id) #
			if in_or:   #
				pass
				msg = "You are already in the group"
			else:
				group_item = Group_item(group_id=group,member=user,authority=au)
				group_item.save()
				msg = "You accept the invitation"			
		else:
			msg = "You reject the invitation"
			
		Invitation.objects.get(invitee=user,group_id=group_id).delete()
		
		return JsonResponse({"msg":msg,"type":"i"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})
		
def teams_work(request):
	username = request.session.get('username',None)
	context = {}
	groups = []
	if username:
		user = Users.objects.get(username=username)
		groups = user.group_item_set.all().order_by("authority").values("group_id","authority")
		for iter in groups:
			gid = Group.objects.get(group_id = iter["group_id"])
			iter["group_name"] = gid.group_name
		context["groups"]=groups
		return render(request,"Group/teams_work.html",context)
	else:
		return redirect('/Users/login/')
		
def path_parse(path):
	path_parse_list = []
	dir_list = path[1:-1].split("/")
	path_parse_list.append("/"+dir_list[0]+"/")
	if len(dir_list) > 1:
		for i in range(2,len(dir_list)+1):
			path_parse_list.append("/"+ "/".join(dir_list[0:i]) +"/")
	
	return path_parse_list
	
def del_file(request):
	group_id = request.session.get("group_id",None)
	username = request.session.get("username",None)
	au = request.session.get("au",None)
	if group_id:
		loc4del = request.POST.get("loc4del")
		user = Users.objects.get(username=username)
		group = Group.objects.get(group_id=group_id)
		au4group_item = au4group.objects.get(group_id=group_id)
		pj_name = "/"+"/".join(loc4del.split("/")[1:-1])+"/"
		
		if au == "2" and au4group_item.au4admin[1] == "0":
			return JsonResponse({"msg":"You have no access to delete dirs or files!","type":"d"})
		if au == "3":
			if au4group_item.au4pj_admin[1] == "0":
				return JsonResponse({"msg":"You have no access to delete dirs or files!","type":"d"})
			else:
				au4pj_item = au4pj.objects.filter(group=group,pj_name=pj_name,user=user)
				if au4pj_item:
					if not au4pj_item[0].tag:
						return JsonResponse({"msg":"You have no access to delete dirs or files!","type":"d"})
			
		if au == "4":
			return JsonResponse({"msg":"You have no access to delete dirs or files!","type":"d"})
			
		# if loc4del[-1] == "/":
			# path = "Users/all_groups/" + str(group_id) + loc4del[0:-1]
		# else:
		path = "Users/all_groups/" + str(group_id) + loc4del
		if os.path.isdir(path):
			ls = os.listdir(path)
			for i in ls:
				c_path = os.path.join(path, i)
				if os.path.isdir(c_path):
					shutil.rmtree(c_path,True)
				else:
					os.remove(c_path)
			shutil.rmtree(path,True)
			return JsonResponse({"msg":"delete the dir successfully!","type":"s"})
		else:
			os.remove(path)
			return JsonResponse({"msg":"delete the file successfully!","type":"s"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"d"})

def download(request):
	username = request.session.get('username',None)
	group_id = request.session.get('group_id',None)
	au = request.session.get('au',None)
	if username and group_id:
		loc4down = request.POST.get('loc4down',None)
		filename = request.POST.get('file_name4down',None)
		path = "Users/all_groups/"+ str(group_id) + loc4down + filename;
		if au == "3" or au == "4":
			group = Group.objects.get(group_id=group_id)
			user = Users.objects.get(username=username)
			#path_parse_list = path_parse(loc4down)
			# bool = False
			# for iter in path_parse_list:
				# au4pj_item = au4pj.objects.filter(group=group,pj_name=iter,user=user)
				# if au4pj_item:
					# if au4pj_item[0].user_au4pj[1] == "1":
						# bool = True
						# break
			# if not bool:
				# return HttpResponse("no access to download in this dir location!")
			au4pj_item = au4pj.objects.get(group=group,pj_name=loc4down,user=user)
			if au4pj_item.user_au4pj[1] == "0":
			#if not bool:
				return JsonResponse({"msg":"no access to upload to this dir!","type":"d"})
		file = open(path,'rb')
		response = FileResponse(file)	
		response['Content-Disposition']='attachment;filename='+'"'+filename+'"'
		return response
			
	else:
		return redirect('/Users/login/')

def stream4group_get(request):
	if not request.session.get('stream_status4group', None):
		request.session['stream_status4group'] = status
	return render(request,"Group/stream_status.html",{'stream_status':request.session.get("stream_status4group",status)})
	
def check(request):
	username = request.session.get("username",None)
	group_id = request.session.get("group_id",None)
	if username:
		query = request.GET
		path = query.get('path')[1:-1].split("/")
		tfo_path = os.path.join("Users","all_groups",str(group_id))
		for path_iter in path:
			tfo_path = os.path.join(tfo_path,path_iter)		
		file_name = query.get('file_name')
		
		request.session['stream_status4group'][0][1] = DONE
		#print(request.session['stream_status4group'][0][1])
		request.session['tfo_path4group'] = tfo_path
		request.session['tfo_name4group'] = file_name
		return JsonResponse({"msg":"check successfully!","type":"s"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"d"})
		
def report(request):
	from maintest.mytools.batch import batch_trf2vcd, batch_merge
	username = request.session.get("username",None)
	if username:
		tfo_path = request.session.get("tfo_path4group",None)
		file_name = request.session.get("tfo_name4group",None)
		if tfo_path and file_name:
			print(tfo_path, file_name)
			batch_trf2vcd(tfo_path, file_name)
			batch_merge(tfo_path, file_name)
			request.session['stream_status4group'][3][1] = DONE
			return JsonResponse({"msg":"Report ready!","type":"s"})
		else:
			return JsonResponse({"msg":"check first!","type":"i"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"d"})
	
def clr_status4group(request):
	request.session["stream_status4group"]=status
	