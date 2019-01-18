from django.conf.urls import url

from . import views
from . import info
from . import task_handle

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
	
	
	url(r'^info/', info.user_info, name='user_info'),
	
	#url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
	
	url(r'^update_info/', info.update_info, name='update_info'),
	
	#url(r'^sendemail_code/$', SendEmailCodeView.as_view(),name='sendemail_code'),
	
	#url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
	
	#url(r'^myproject/$', info.myproject, name='myproject'),
	
	#url(r'^mymessage/$', MymessageView.as_view(), name='mymessage'),
	
	url(r'^log/',views.log,name="log"),
	url(r'^test_request/',task_handle.test_request,name="test_request"),

	
]
