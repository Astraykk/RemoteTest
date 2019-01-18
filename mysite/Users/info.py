from django.shortcuts import render,redirect
from Users.models import Users
from Users.models import Task

def user_info(request,msg=""):
	username = request.session.get('username',None)
	if username:
		context = info_context(username)
		context['msg'] = msg
		return render(request,"Users/info.html",context)
	else:
		return redirect('/Users/login/')
		
		
def info_context(username):
	info = {}
	user = Users.objects.get(username=username)
	info['username'] = user.username
	info['authority'] = user.authority
	info['email'] = user.email
	
	return {'info':info}
					
def update_info(request):
	username = request.session.get('username',None)
	if username:
		user = Users.objects.get(username=username)
		if request.method == "POST":
			new_pwd = request.POST.get("new_pwd")
			if new_pwd:
				if request.POST.get("old_pwd") == user.password:
					user.password = new_pwd
					user.save()
					return user_info(request,"change password successfully!")
				else:
					return user_info(request,"please input right password!")
			else:
				user.email = request.POST.get("email")
				user.save()
				return user_info(request,"change email successfully!")
		else:
			return user_info(request)
		
	else:
		return redirect('/Users/login/')
	

	