#import mysite.urls
import os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
 
django.setup()

from Users.models import Users,Group,au4pj
from Users.models import Task,allTask4user,allTask4group,task_db,user_in_queue,user4serving
from Users.views import create_history
#from Users.patternGen import tfo_parser

from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect,render

import multiprocessing
import time
import sys
import functools
import bs4
import random

DONE = 2
LOADING = 1
UNDONE = 0

# class TailRecurseException(BaseException):
	# def __init__(self, args, kwargs):
		# self.args = args
		# self.kwargs = kwargs

# def tail_call_optimized(g):
	# """
	# This function decorates a function with tail call
	# optimization. It does this by throwing an exception
	# if it is it's own grandparent, and catching such
	# exceptions to fake the tail call optimization.

	# This function fails if the decorated
	# function recurses in a non-tail context.
	# """
	# @functools.wraps(g)
	# def func(*args, **kwargs):
		# f = sys._getframe()
		# if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
			# raise TailRecurseException(args, kwargs)
		# else:
			# while 1:
				# try:
					# return g(*args, **kwargs)
				# except TailRecurseException as e:
					# args = e.args
					# kwargs = e.kwargs
				
	# func.__doc__ = g.__doc__
	# return func


def test_request(request):
	#from maintest.mytools.patternGen import tfo_parser
	username = request.session.get("username",None)
	group_id = request.session.get("group_id",None)
	au = request.session.get("au",None)
	
	if username:
		user = Users.objects.get(username=username)
		project_loc = request.POST.get('tfo_loc',None)
		tfo_name = request.POST.get('tfo_name',None)
		if not project_loc:
			project_loc = request.session.get("tfo_path",None).split(os.path.join("Users","all_users",username,""))[1]
			tfo_name = request.session.get("tfo_name",None)
		else:
			pj_loc_os_path_join=""
			for iter in project_loc.split("/"):
				pj_loc_os_path_join = os.path.join(pj_loc_os_path_join,iter)
			project_loc = pj_loc_os_path_join
		tag = request.POST.get('user_or_group',None)
		msg = check4waitingInfo()
		if tag != 'group':
			user_or_group = '0'
			u_or_g = username
			path = os.path.join("Users","all_users",username,project_loc)
			user_in_queue_item = user_in_queue(user=user,x=1)
			request.session['stream_status'][2][1] = DONE
		else:
			request.session['stream_status4group'][2][1] = DONE
			group = Group.objects.get(group_id=group_id)
			if au == "3" or au == "4":				
				#user = Users.objects.get(username=username)
				au4pj_item = au4pj.objects.get(group=group,pj_name=project_loc,user=user)
				if au4pj_item.user_au4pj[2] == "0":
					return JsonResponse({"msg":"no access to test in this project!","type":"d"})
			user_in_queue_item = user_in_queue(group=group,x=1)
			user_or_group = '1'
			u_or_g = str(group_id)
			path = os.path.join("Users","all_groups",str(group_id),project_loc)
		
		# dir_list = os.listdir(path)
		# tfo_list = []
		# for iter in dir_list:
			# if iter.endswith('.tfo'):
				# tfo_list.append(iter)
		
		# if len(tfo_list) != 1:
			# return JsonResponse({"msg":"no tfo file or more than one tfo file in chosen location","type":"w"})
		
		file_list_list = tfo_parser(path,tfo_name)
		print(file_list_list)
		user_in_queue_item.x = len(file_list_list)
		user_in_queue_item.save()
		
		for iter in file_list_list:
			project_loc = iter[0]

			ptn_name = iter[1][0]
			
			dir_list = os.listdir(project_loc)
	
			input_ptn = ptn_name + ".ptn"
			if input_ptn not in dir_list:
				if request.POST.get('tfo_loc',None):
					return JsonResponse({"msg":"no ptn file called " + input_ptn + " in " + project_loc +". Please check tfo file!","type":"w"})
				else:
					return HttpResponse("no ptn file called " + input_ptn + " in " + project_loc +". Please check tfo file!")
			addIndb(request,u_or_g,project_loc,user_or_group,ptn_name)
			#msg = {"msg":"add test task successfully!","type":"s"}
		


		if request.POST.get('tfo_loc',None):
			return JsonResponse({"msg":msg,"type":"s"})
		else:
			return HttpResponse(msg)
	else:
		return redirect("Users/login/")
	
	


#----------递归版---------    
# @tail_call_optimized     
# def test_pack(task):
	# test(task)                    	
	# del_task(task)
	# new_task_number = Task.objects.count()
	# if new_task_number:
		# new_task = Task.objects.order_by('task_priority','request_serial_num')[0]
		# return test_pack(new_task)
	# else:
		# print("server has finished all the tasks!")
		
#---------------------------------------
	
#----------非递归版--------------------- <<-----推荐使用
def test_pack(task):
	new_task = task
	new_task_number = Task.objects.count()
	while new_task_number:
		test(new_task)
		complete_task(new_task)		
		del_task(new_task)
		new_task_number = Task.objects.count()
		if new_task_number:
			new_task = Task.objects.order_by('request_serial_num')[0]
	print("server has finished all the tasks!")	

#------------------------------------


def task_create(request,username,project_loc,user_or_group,ptn_name):	
	if Task.objects.count():
		t = Task.objects.order_by('-request_serial_num')[0]
		request_serial_num = t.request_serial_num + 1
	else:
		request_serial_num = 1
	#task_priority = priority_weigh(authority,request_serial_num)
	task = Task(username=username,project_loc=project_loc,request_serial_num=request_serial_num,user_or_group=user_or_group,ptn_name=ptn_name)
	task.save()
	

	
def addIndb(request,username,project_loc,user_or_group,ptn_name):
	if user_or_group == '0':
		user = Users.objects.get(username=username)
		task_record = allTask4user(user=user,project_loc=project_loc,ptn_name=ptn_name)
		task_record.save()
		request_serial_num = user.task_db_set.count() + 1
		task_db_item = task_db(user=user,username=username,project_loc=project_loc,request_serial_num=request_serial_num,user_or_group=user_or_group,ptn_name=ptn_name)
		task_db_item.save()
	else:
		group = Group.objects.get(group_id=int(username))
		task_record = allTask4group(group=group,submitter=request.session.get('username'),project_loc=project_loc,ptn_name=ptn_name)
		task_record.save()
		request_serial_num = group.task_db_set.count() + 1
		task_db_item = task_db(group=group,username=username,project_loc=project_loc,request_serial_num=request_serial_num,user_or_group=user_or_group,ptn_name=ptn_name)
		task_db_item.save()
	if task_db.objects.count() == 1:
		pro = multiprocessing.Process(target = minute_process)
		pro.start()
		#pro.join()
	#create_history(task.username,"add testing task",task.project_loc,user_or_group)

def minute_process():
	times = 0
	beta = 4
	while(task_db.objects.count()>0):
		time.sleep(1)
		queue2serving()		
		task_db2task()		             #
		times = times + 1
		if times % beta*4 == 0:
			times = 0
			weight_update()
			
def queue2serving():
	alpha = 0.75
	N = 5
	serving_num = user4serving.objects.count()
	if  serving_num < N and user_in_queue.objects.count() > 0:
		for i in range(serving_num,N+1):
			if user_in_queue.objects.count() > 0:
				queue_first = user_in_queue.objects.order_by('serial')[0]   #repeat
				w = alpha ** queue_first.x
				user4serving_item = user4serving(user=queue_first.user,group=queue_first.group,x=queue_first.x,x_current=queue_first.x,w=w)
				user4serving_item.save()
				queue_first.delete()
			else:
				break

def task_db2task():
	FIFO_length = 2
	task_num = Task.objects.count()
	if task_num < FIFO_length and task_db.objects.count() > 0:
		for i in range(task_num,FIFO_length):
			if task_db.objects.count() > 0 and user4serving.objects.count()>0:
				task_db_item = choose_task()
				if Task.objects.count() > 0:
					request_serial_num = Task.objects.order_by('-request_serial_num')[0].request_serial_num + 1
					task_item = Task(username=task_db_item.username,user_or_group=task_db_item.user_or_group,project_loc=task_db_item.project_loc,request_serial_num=request_serial_num,ptn_name=task_db_item.ptn_name)
					task_item.save()
				else:
					task_item = Task(username=task_db_item.username,user_or_group=task_db_item.user_or_group,project_loc=task_db_item.project_loc,request_serial_num=1,ptn_name=task_db_item.ptn_name)
					task_item.save()
					#task = Task.objects.order_by('request_serial_num')[0]
					pro = multiprocessing.Process(target = test_pack,args = (task_item,))
					pro.start()
					#pro.join()
				
				# if user4serving.objects.count()>0:
				if task_db_item.user:
					user4serving_item = user4serving.objects.filter(user=task_db_item.user)[0]
				else:
					user4serving_item = user4serving.objects.filter(group=task_db_item.group)[0]
					
				if user4serving_item.x_current == 1:			
					user4serving_item.delete()
				else:
					user4serving_item.x_current -= 1
					user4serving_item.save()
					
				task_db_item.delete()
			else:
				break

def choose_task():
	serving_set = user4serving.objects.all()
	rand = random.random()
	local_sum = 0
	sum = 0
	serving_item = serving_set[0]
	for iter in serving_set:
		sum += iter.w
	for iter in serving_set:
		local_sum += iter.w/sum
		if  rand <= local_sum:
			serving_item = iter
			break
	if serving_item.user:
		task_db_item = task_db.objects.filter(user=serving_item.user).order_by('request_serial_num')[0]
	else:
		task_db_item = task_db.objects.filter(group=serving_item.group).order_by('request_serial_num')[0]
	return task_db_item
	
	
def weight_update():
	k = 1.3
	alpha = 0.75
	serving_set = user4serving.objects.all()
	for iter in serving_set:
		iter.w = iter.w * k
		if iter.w > alpha:
			iter.w = alpha
		iter.save()


def priority_weigh(authority,request_serial_num):
	dict = {"common_user":5}
	authority_weight = 1
	request_weight = 1
	task_priority = dict[authority]*authority_weight + request_serial_num*request_weight
	return task_priority
	
def del_task(task):
	t = Task.objects.filter(request_serial_num=task.request_serial_num)
	t.delete()
	
def complete_task(task):
	if task.user_or_group == "0":
		user = Users.objects.get(username=task.username)
		task_record = allTask4user.objects.filter(user=user,project_loc=task.project_loc,ptn_name=task.ptn_name,finish_tag=False).order_by('submit_time')[0]
		task_record.finish_tag = True
		task_record.save()
	else:
		group = Group.objects.get(group_id=int(task.username))
		task_record = allTask4group.objects.filter(group=group,project_loc=task.project_loc,ptn_name=task.ptn_name,finish_tag=False).order_by('submit_time')[0]
		task_record.finish_tag = True
		task_record.save()
		
	
def test(task):
	
	tag = task.user_or_group
	if task.user_or_group == "0":	
		path = os.path.join("Users","all_users",task.username,task.project_loc)
		file_loc = os.path.join("Users","all_users")
	else:
		path = os.path.join("Users","all_groups",task.username,task.project_loc)
		file_loc = os.path.join("Users","all_groups")
		
	dir_list = os.listdir(os.path.join(file_loc,task.username,task.project_loc))
	
	input_ptn = task.ptn_name + ".ptn"
	if input_ptn not in dir_list:
		return False
	output_trf = task.ptn_name + ".trf"
	create_history(task.username,"testing",task.project_loc,tag)
	path_in = os.path.join(path,input_ptn)
	path_o = os.path.join(path,output_trf)
	abc = os.popen("sudo /home/linaro/BR0101/z7_v4_com/z7_v4_ip_app " + path_in + " " + path_o + " 1 1 1").read()
	print(abc)
	#for i in range(5):
		#time.sleep(1)
		#print("testing "+task.username+" "+ task.project_loc + input_ptn + ".....")
	
	print("finish testing "+task.username+" "+ task.project_loc + input_ptn +"....")
	
	create_history(task.username,"finish testing",task.project_loc,tag)
		

def get_soup(path, file):
	path = os.path.join(path, file)
	# print(path)
	with open(path, "r") as f:
		soup = bs4.BeautifulSoup(f.read(), "xml")
	return soup
		
def tfo_parser(path, file):
	"""
	:param path:
	:param file:
	:return file_list_list:
	"""
	file_list_list = []
	soup = get_soup(path, file)
	name_check(file, soup.TFO['name'])
	for test_tag in soup.find_all('TEST'):
		file_list = {
			'PTN': test_tag['name'] + '.ptn',
			'LBF': soup.TFO.LBF['type'] + '.lbf',
			'TCF': 'F93K.tcf'
		}
		project_name = test_tag['name']
		for child in test_tag.children:
			if type(child) == bs4.element.Tag:
				if child.name == 'DWM' or child.name == 'BIT':
					file_list[child.name] = child['name']
				else:
					file_list[child.name] = child['name'] + '.' + child.name.lower()
		# file_list_list[test_tag['path']] = (project_name, file_list)
		file_list_list.append([os.path.join(path, test_tag['path']), (project_name, file_list)])
		# file_list_list.append([test_tag['path'], (project_name, file_list)])
	print(file_list_list)
	return file_list_list
	
def task_list4user(request):
	username = request.session.get('username',None)
	context ={}
	if username:
		user = Users.objects.get(username=username)
		task_list = user.alltask4user_set.order_by('-submit_time')
		context['task_list'] = task_list
		return render(request,"Task/task_list.html",context)
	else:
		return redirect("/Users/login/")
		
def task_list4group(request):
	username = request.session.get('username',None)
	group_id = request.session.get('group_id',None)
	context ={}
	if group_id:
		group = Group.objects.get(group_id=group_id)
		task_list = group.alltask4group_set.order_by('-submit_time')
		context['task_list'] = task_list
		return render(request,"Task/task_list4group.html",context)
	else:
		return redirect("/Users/login/")
	
def check4waitingInfo():
	serving_num = user4serving.objects.count()
	user_in_queue_num = user_in_queue.objects.count()
	task_num_list = []
	task_in_queue_list = []
	A_task_time = 4
	if serving_num + user_in_queue_num < 5:
		return "Your tasks are running"
	else:
		task_num_dict = user4serving.objects.all().values("x_current")
		task_in_queue_dict = user_in_queue.objects.all().order_by("serial").values("x")
		
		for iter in task_num_dict:
			task_num_list.append(iter["x_current"])
			
		for iter in task_in_queue_dict:
			task_in_queue_list.append(iter["x"])
		
		merge = task_num_list + task_in_queue_list
		for i in range(1,5):
			merge[merge.index(max(merge))] = 0
		wait_sec = sum(merge) * A_task_time
		return "There are %d users in serving list, and %d users in queue.\n your tasks will get to platform in about %d seconds." % (serving_num,user_in_queue_num,wait_sec)
		
		
