from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from Users.models import Users,Group,Group_item,au4group,au4pj
from Users.group import path_parse,clr_status4group
import json
import os
import re

def home (request):
	#username = request.POST.get('username',None)
    #context = {'username': username}
	username = request.session.get('username',None)
	if(username):
		dirs = show_file(username)
		context = {'username': username,'dirs':dirs}
		return render(request, 'nav/homepage.html', context)

	else:
		return render(request, 'nav/homepage.html')#, context)




def show_file(username):
	dirs={}
	sec_dir={}
	dirs['content']=[]
	dirs['dirname']=username
	path = "Users/all_users/"+username
	dir_list=os.listdir(path)
	
	for iter_dir in dir_list:
		path_iter = path + "/" +iter_dir
		if(os.path.isdir(path_iter)):
			#content=os.listdir(path)
			# sec_dir['dirname']=iter_dir
			# sec_dir['content']=os.listdir(path_iter)
			dirs['content'].append({'dirname':iter_dir,'content':os.listdir(path_iter)})
		else:
			dirs['content'].append(iter_dir)
	# print(dirs)
	return dirs
	
def getTree(request):
	tree = []
	username = request.session.get("username")
	if username:
		path4pj = request.GET.get("path")
		if path4pj:
			path = "Users/all_users/"+ username + path4pj
			tree = [{'text':path4pj.split("/")[-2],'nodes':dir_search(path)}]
		else:
			path = "Users/all_users/"+ username
			tree = dir_search(path)
		return JsonResponse({"data":tree})
	else:
		return JsonResponse({"data":[{"text":"None before login"}]})

def getGroupTree(request):
	tree = []
	username = request.session.get("username")
	group_id = request.session.get("group_id")
	au = request.session.get("au")
	if username and group_id:
		clr_status4group(request)
		path4pj = request.GET.get("path")

		if au == "1" or au == "2":
			if path4pj:
				path = "Users/all_groups/"+ str(group_id) + path4pj
				tree = [{'text':path4pj.split("/")[-2],'nodes':dir_search(path)}]
			else:
				path = "Users/all_groups/"+ str(group_id)
				tree = dir_search(path)
		else:
			if path4pj:
				path = "Users/all_groups/"+ str(group_id) + path4pj 
				path4parse = "Users/all_groups/"+ str(group_id)
				tree = [{'text':path4pj.split("/")[-2],'nodes':dir_search4group(request,path,path4parse)}]
			else:
				path = "Users/all_groups/"+ str(group_id)
				tree = dir_search4group(request,path,path)
		return JsonResponse({"data":tree})
	else:
		return JsonResponse({"data":[{"text":"None before login"}]})
	
def dir_search(path):
	tree = []
	tree_node = {}
	dir_list = os.listdir(path)
	
	for iter_dir in dir_list:
		if not iter_dir.startswith('.'):
			path_iter = path + '/' + iter_dir
			if(os.path.isdir(path_iter)):
				#tree_node[] = iter_dir
				#tree_node['nodes'] = dir_search(path_iter)
				tree.append({'text':iter_dir,'nodes':dir_search(path_iter)})
			else:
				tree.append({"text":iter_dir})
	
	return tree
	
def dir_search4group(request,path,path4parse):
	tree = []
	tree_node = {}
	dir_list = os.listdir(path)
	
	username = request.session.get("username")
	group_id = request.session.get("group_id")
	
	for iter_dir in dir_list:
		if not iter_dir.startswith('.'):
			if path[-1] == "/":
				path_iter = path + iter_dir
			else:
				path_iter = path + '/' + iter_dir
			if(os.path.isdir(path_iter)):
				group = Group.objects.get(group_id=group_id)
				user = Users.objects.get(username=username)
				#path_parse_list = path_parse((path_iter+"/").split(path4parse)[1])
				bool = False
				# for iter in path_parse_list:
					# au4pj_item = au4pj.objects.filter(group=group,pj_name=iter,user=user)
					# if au4pj_item:
						# if au4pj_item[0].user_au4pj != "000":
							# bool = True
							# break
							
				
				au4pj_item_set = au4pj.objects.filter(group=group,user=user,pj_name__regex="^"+(path_iter+"/").split(path4parse)[1])
				if au4pj_item_set:
					for iter in au4pj_item_set:
						if iter.user_au4pj != "000":
							bool = True
				
				if bool:
					tree.append({'text':iter_dir,'nodes':dir_search4group(request,path_iter,path4parse)})
				else:
					tree.append({'text':iter_dir,'nodes':dir_search4group(request,path_iter,path4parse),'state':{'disabled':'true'}})
			else:
				tree.append({"text":iter_dir})
	
	return tree

def edit_file(request):
	import binascii
	username = request.session.get("username")
	if username:
		file_path = "Users/all_users/" + username + request.GET.get("path") + request.GET.get("file_name")
		if os.path.isfile(file_path):
			if os.path.splitext(file_path)[1] == '.ptn' or os.path.splitext(file_path)[1] == '.rbt':
				return render(request,"nav/content.html",{'content':"file is too large to load!"})
			with open(file_path, 'rb+') as f:
				content = f.read()
				# if os.path.splitext(file_path)[1] == '.ptn':
					# pattern = re.compile('.{32}')
					# content = str(binascii.hexlify(content)).lstrip("b'").upper()
					# content = '\t'.join(re.findall(r'.{4}', content))
					# content = '\n'.join(re.findall(r'.{40}', content))
			# print(type(content))
			return render(request,"nav/content.html",{'content':content})
		else:
			return render(request,"nav/content.html",{'content':"edit your file here."})
	else:
		return render(request,"nav/content.html",{'content':"login first"})
		
def save_file(request):
	username = request.session.get("username")
	if username:
		try:
			content = request.POST.get("edit-text")
			path = "Users/all_users/" + username + request.POST.get("loc4edit")
			with open(path, 'w') as f:
				f.write(content)
			return JsonResponse({"msg":"Edit-text submit successfully!","type":"s"})
		except Exception as exc:
			return JsonResponse({"msg":exc,"type":"d"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})
		
		
def edit_file4group(request):
	import binascii
	group_id = request.session.get("group_id")
	if group_id:
		file_path = "Users/all_groups/" + str(group_id) + request.GET.get("path") + request.GET.get("file_name")
		if os.path.isfile(file_path):
			if os.path.splitext(file_path)[1] == '.ptn' or os.path.splitext(file_path)[1] == '.rbt':
				return render(request,"nav/content.html",{'content':"file is too large to load!"})
			with open(file_path, 'rb+') as f:
				content = f.read()
				# if os.path.splitext(file_path)[1] == '.ptn':
					# pattern = re.compile('.{32}')
					# content = str(binascii.hexlify(content)).lstrip("b'").upper()
					# content = '\t'.join(re.findall(r'.{4}', content))
					# content = '\n'.join(re.findall(r'.{40}', content))
			# print(type(content))
			return render(request,"nav/content.html",{'content':content})
		else:
			return render(request,"nav/content.html",{'content':"edit your file here."})
	else:
		return render(request,"nav/content.html",{'content':"login first"})
		
def save_file4group(request):
	group_id = request.session.get("group_id")
	if group_id:
		try:
			clr_status4group(request)
			content = request.POST.get("edit-text")
			path = "Users/all_groups/" + str(group_id) + request.POST.get("loc4edit")
			with open(path, 'w') as f:
				f.write(content)
			return JsonResponse({"msg":"Edit-text submit successfully!","type":"s"})
		except Exception as exc:
			return JsonResponse({"msg":exc,"type":"d"})
	else:
		return JsonResponse({"msg":"Your session has expired, please relogin first!","type":"w"})