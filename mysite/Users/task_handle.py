#import mysite.urls
import os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
 
django.setup()

from Users.models import Users
from Users.models import Task
from Users.views import create_history

from django.http import HttpResponse

import multiprocessing
import time
import sys
import functools



class TailRecurseException(BaseException):
	def __init__(self, args, kwargs):
		self.args = args
		self.kwargs = kwargs

def tail_call_optimized(g):
	"""
	This function decorates a function with tail call
	optimization. It does this by throwing an exception
	if it is it's own grandparent, and catching such
	exceptions to fake the tail call optimization.

	This function fails if the decorated
	function recurses in a non-tail context.
	"""
	@functools.wraps(g)
	def func(*args, **kwargs):
		f = sys._getframe()
		if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
			raise TailRecurseException(args, kwargs)
		else:
			while 1:
				try:
					return g(*args, **kwargs)
				except TailRecurseException as e:
					args = e.args
					kwargs = e.kwargs
				
	func.__doc__ = g.__doc__
	return func


def test_request(request):
	username = request.session.get("username")
	if username and request.method == 'POST':
		project_name = request.POST.get('project_name',None)
		authority = Users(username=username).authority
		task_create(username,project_name,authority)
		task_number = Task.objects.count()#len(Task.objects.all())
		
		if task_number == 1:
			
			task = Task.objects.order_by('task_priority','request_serial_num')[0]
			pro = multiprocessing.Process(target = test_pack,args = (task,))
			pro.start()
			return HttpResponse("<script>alert(\"add first test task successfully! your test task is running!\");window.location.href=\"/\";</script>")
			
		else:
			return HttpResponse("<script>alert(\"add test task successfully!\");window.location.href=\"/\";</script>")
	else:
		return HttpResponse("<script>alert(\"Login first!\");window.location.href=\"/Users/login/\";</script>")
	
	
def response_to_first():
	return HttpResponse("<script>alert(\"add first test task successfully! your test task is running!\");window.location.href=\"/\";</script>")

	
@tail_call_optimized
def test_pack(task):
	test(task)                    #     <<--------------
	
	del_task(task)
	new_task_number = Task.objects.count()
	if new_task_number:
		new_task = Task.objects.order_by('task_priority','request_serial_num')[0]
		return test_pack(new_task)
	else:
		print("server has finished all the tasks!")
		

	
# def task_query():
	# task = Task.objects.order_by('task_priority','request_serial_num')[0]
	# return task





def task_create(username,project_name,authority):
	
	if Task.objects.count():
		t = Task.objects.order_by('-request_serial_num')[0]
		request_serial_num = t.request_serial_num + 1
	else:
		request_serial_num = 1
	task_priority = priority_weigh(authority,request_serial_num)
	task = Task(username=username,project_name=project_name,authority=authority,request_serial_num=request_serial_num,task_priority=task_priority)
	task.save()
	create_history(task.username,"add testing task",task.project_name)

def priority_weigh(authority,request_serial_num):
	dict = {"common_user":5}
	authority_weight = 1
	request_weight = 1
	task_priority = dict[authority]*authority_weight + request_serial_num*request_weight
	return task_priority
	
def del_task(task):
	t = Task.objects.filter(request_serial_num=task.request_serial_num)
	t.delete()
	
def test(task):
	create_history(task.username,"testing",task.project_name)
	path = "/home/mysite/Users/all_users/" + task.username
	print("sudo /home/linaro/BR0101/z7_v4_com/z7_v4_ip_app "+path+"/mul5.ptn "+path+"/mul5.trf "+"1 1 1")
	os.popen("sudo /home/linaro/BR0101/z7_v4_com/z7_v4_ip_app "+path+"/mul5.ptn "+path+"/mul5.trf "+"1 1 1")
	# for i in range(8):
		# time.sleep(2)
		# print("testing "+task.username+" "+task.project_name+".....")
	
	print("finish testing "+task.username+" "+task.project_name+"....")
	
	create_history(task.username,"finish testing",task.project_name)
		
	