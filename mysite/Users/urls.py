from django.conf.urls import url

from . import views
from . import info
from . import task_handle
from . import group
from . import manage,build

urlpatterns = [
 #   url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^sign_up/',views.sign_up, name='sign_up'),
    url(r'^add_user/',views.add_user,name='add_user'),
    #url(r'^check/',views.check,name='check'),
    url(r'^identify/',views.identify,name='identify'),
    url(r'^upload/',views.upload,name='upload'),
    url(r'^mkdir/',views.mkdir,name='mkdir'),
    url(r'^logout/',views.logout,name='logout'),
	url(r'^del_file4user/',views.del_file,name="del_file"),
	url(r'^down_fileofuser/',views.download,name="download"),
	
	#--------------------info--------------------------------
	url(r'^info/', info.user_info, name='user_info'),
	url(r'^profile/',info.profile,name="profile"),
	url(r'^update_account/', info.update_account, name='update_account'),
	url(r'^update_email/', info.update_email, name='update_email'),
	url(r'^account/',info.account,name="account"),
	url(r'^email/',info.email,name="email"),
	url(r'^history/',info.history,name="history"),
	url(r'^log/',views.log,name="log"),
	url(r'^test_request/',task_handle.test_request,name="test_request"),
	
	#--------------------group-------------------
	url(r'^group_page/',group.index, name="index_page"),
	url(r'^my_group/',group.my_group,name="my_group"),
	url(r'^teams_work/',group.teams_work,name="teams_work"),
	url(r'^go2group/(?P<group_id>[0-9]*)/$', group.go2group,name="go2group"), 
	url(r'^create_group/',group.create_group,name="create_group"),
	url(r'^create_group_project/',group.create_group_project,name="create_group_project"),
	url(r'^upload_group_project_file/',group.upload,name="upload_group_project_file"),
	url(r'^group_invite/',group.invite,name="group_invite"),
	url(r'^invitations/',views.invitations,name="inv"),
	url(r'^reply_inv/(?P<group_id>[0-9]*)/(?P<reply>[a-z]*)/(?P<au>[0-9]*)/$', group.reply_inv,name="reply"), 
	url(r'^del_file/',group.del_file,name="del_file"),
	url(r'^down_fileofgroup/',group.download,name="download"),
	url(r'^check4group/',group.check,name="check4group"),
	url(r'^report4group/',group.report,name="report4group"),
	url(r'^stream4group_get/',group.stream4group_get,name="stream4group_get"),
	url(r'^build4group/',build.build4group,name="build4group"),
	
	#---------------------manage-------------------
	url(r'^manage/(?P<group_id>[0-9]*)/$',manage.index,name="manage"),
	url(r'^manage/',manage.index,name="manage"),
	url(r'^au_update/',manage.au_update,name="authority4group update"),
	url(r'^group_au_settings/',manage.group_au_settings,name="group_au_settings"),
	url(r'^change_au/',manage.change_au,name="change authority as a member//priority"),
	url(r'^change_au_memlist/',manage.memlist,name="change_au_memlist"),
	url(r'^change_au4member/',manage.change_au4member,name="change_au4member"),
	url(r'^memlist4del/',manage.memlist4del,name="memlist4del"),
	url(r'^delete_member/',manage.delete_member,name="delete_member"),
	url(r'^au4pj_change/',manage.au4pj_change,name="au4pj_change"),
	url(r'^mem_au4pj/',manage.mem_au4pj,name="mem_au4pj"),
	url(r'^pj_au/',manage.pj_au,name="pj_au"),
	url(r'^pj_au_ml/',manage.pj_au_ml,name="pj_au_ml"),
	
	#---------------------task_list--------------------
	url(r'^task_list4user/',task_handle.task_list4user,name="record"),
	url(r'^task_list4group/',task_handle.task_list4group,name="record"),
	
]
