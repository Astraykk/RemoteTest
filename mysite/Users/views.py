from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from Users.models import Users

import django.db 
import time
import os

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.


def sign_up(request):
	return render(request, 'Users/sign_up.html')


def login(request):
	return render(request,"Users/login.html")


def identify(request):
	if request.method == 'POST':
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
		user = Users.objects.get(username=username)		

		if user and user.password == password:
			#
			request.session['username']=user.username
			
			# authority
			# dirs = show_file(user.username)
			# context = {'username': username,'dirs':dirs}
			# return render(request, 'mysite/homepage.html', context)

			return redirect("/")
			# return redirect("/index")
		else:
			return HttpResponse("<script>alert(\"You entered an incorrect user name or password\");window.location.href=\"/Users/login/\";</script>")
	
	else:
		return HttpResponse("<script>window.location.href=\"/Users/login/\";</script>")
		


def add_user(request):
	if request.method == 'POST':

		username = request.POST.get("username",None)
		password = request.POST.get("password",None)
		try:
			user=Users(username=username,password=password)           #<<<<<<<<<<<<--------------------bug----------------
			user.save()
		except django.db.utils.IntegrityError:
			html_add_user_str="<p>"+ username + ''' 
			has been signed up already! Please try another one to <a href="/Users/sign_up/">sign up</a> !</p>

			'''
		else:
			request.session['username']=user.username
			path = "Users/all_users/"+username
			os.mkdir(path)

			html_add_user_str='''
				<p>Successfully sign up! Click <a href="/">here</a> to login</p>

			'''
	else:
		html_add_user_str='''
			<p>failed</p>
		'''
	return HttpResponse(html_add_user_str)





def upload(request):
	if request.method == 'POST':
		username = request.session.get('username',None)
		if username:
			dirname = request.POST.get('dir',None)
			path = username + "/" + dirname;
			# files = request.FILES.get("myfile", None)
			# if files:
			# 	for file in files:
			# 		with open("./all_users/%s/%s" % (path,file.name)) as fp:    #<<<<<<<-------------------------
			# 			for chunk in file.chunks():
			# 				fp.write(chunk)
			# 			fp.close()

			file = request.FILES.get("myfile", None)
			if file:
				with open("Users/all_users/%s/%s" % (path,file.name),'wb') as fp:
					for chunk in file.chunks():
						fp.write(chunk)
					fp.close()
					create_history(username,"upload file",file.name)
				# dirs = show_file(username)
				# context = {'username': username,'dirs':dirs}
				# return render(request, 'mysite/homepage.html', context)

				return redirect("/")
				# return redirect("/index")
							
			else:
				return HttpResponse("<script>alert(\"please select files to upload!\");window.location.href=\"/\";</script>")
		
		else:
			return HttpResponse("<script>alert(\"Login first!\");window.location.href=\"/Users/login/\";</script>")
	else:	
		return redirect("/")
		# return redirect("/index")


# def show_file(username):
# 	dirs={}
# 	sec_dir={}
# 	dirs['content']=[]
# 	dirs['dirname']=username
# 	path = "Users/all_users/"+username
# 	dir_list=os.listdir(path)
	
# 	for iter_dir in dir_list:
# 		path_iter = path + "/" +iter_dir
# 		if(os.path.isdir(path_iter)):
# 			#content=os.listdir(path)
# 			# sec_dir['dirname']=iter_dir
# 			# sec_dir['content']=os.listdir(path_iter)
# 			dirs['content'].append({'dirname':iter_dir,'content':os.listdir(path_iter)})
# 		else:
# 			dirs['content'].append(iter_dir)
# 	print(dirs)
# 	return dirs

def mkdir(request):
	if request.method == 'POST':
		username = request.session.get('username',None)

		if username:
			dirname = request.POST.get("dir4mk", None)
			#print(dirname+"--------------------------------")
			path = "Users/all_users/" + username + "/"+ dirname
			try:
				os.mkdir(path)				
			except OSError:
				#context = {'username': username,'msg':"already have this direction"}
				return HttpResponse("<script>alert(\"already have this direction!\");window.location.href=\"/\";</script>")
			else:
				# dirs = show_file(username)
				# context = {'username': username,'dirs':dirs}
				create_history(username,"create dir",dirname)
				return redirect("/")
				# return redirect("/index")
			
	# context = {'username': username,'msg':"make dir failed!"}
	# return render(request, 'mysite/homepage.html', context)
	# return redirect("/")
	# return redirect("/index")
	return HttpResponse("<script>alert(\"Login first!\");window.location.href=\"/Users/login/\";</script>")



	



def logout(request):
	del request.session['username']
	return redirect("/")



def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


def create_history(username,behavior,filename):
	with open("Users/all_users/%s/%s" % (username,"log.txt"),'a') as fp:
		fp.write(behavior+" \t "+filename+" \t "+time.asctime(time.localtime(time.time()))+"\n")
	fp.close()
	# print "time.time(): %f " %  time.time()
	# print time.localtime( time.time() )
	# print time.asctime( time.localtime(time.time()) )
	
def log(request):
	username = request.session.get("username")
	if username:
		log=[]
		try:
			fp = open("Users/all_users/"+username+"/log.txt","r")
		except FileNotFoundError:
			log.append("no log information")
		else:
			log=fp.readlines();
			fp.close()
		return JsonResponse({"log":log})
	#else:
		#return HttpResponse("<script>alert(\"Login first!\");window.location.href=\"/Users/login/\";</script>")
		
		

	
