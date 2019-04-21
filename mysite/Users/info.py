from django.shortcuts import render,redirect
from Users.models import Users
from Users.models import Task

def user_info(request,link="",msg=""):
	username = request.session.get('username',None)
	if username:
		context = info_context(username)
		context['msg'] = msg
		html = "Users/account.html";
		if link:
			html = "Users/" + link + ".html"
		return render(request,html,context)    #  <-------
	else:
		return redirect('/Users/login/')
		
		
def info_context(username):
	info = {}
	user = Users.objects.get(username=username)
	info['username'] = user.username
	info['authority'] = user.authority
	info['email'] = user.email
	info['subscribe'] = user.subscribe
	return {'info':info}
					

def profile(request):
	username = request.session.get('username',None)
	if username:
		return user_info(request,"profile")
	else:
		return redirect('/Users/login/')					

def account(request):
	username = request.session.get('username',None)
	if username:
		return render(request,"Users/account.html")
	else:
		return redirect('/Users/login/')

		
def email(request):
	username = request.session.get('username',None)
	if username:
		return user_info(request,"email")
	else:
		return redirect('/Users/login/')

def history(request):
	username = request.session.get('username',None)
	if username:
		return render(request,"Users/history.html")
	else:
		return redirect('/Users/login/')



def update_account(request):
	username = request.session.get('username',None)
	if username:
		user = Users.objects.get(username=username)
		if request.method == "POST":
			new_pwd = request.POST.get("new_pwd")
			if new_pwd:
				if request.POST.get("old_pwd") == user.password:
					user.password = new_pwd
					user.save()
					return user_info(request,"account","change password successfully!")
				else:
					return user_info(request,"account","please input right password!")
			#else:
				#return user_info(request,"change email successfully!")
		else:
			return user_info(request)
		
	else:
		return redirect('/Users/login/')

def update_email(request):
	username = request.session.get('username',None)
	if username:
		user = Users.objects.get(username=username)
		if request.method == "POST":
			email = request.POST.get("email")
			subscribe_or = request.POST.get("subscribe_or")
			if subscribe_or == "yes":
				user.subscribe = True
			else:
				user.subscribe = False
			user.email = email
			user.save()
			return user_info(request,"email","change email settings successfully!")
		else:
			return user_info(request)
	else:
		return redirect('/Users/login/')