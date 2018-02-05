from django.conf.urls import url

from . import views

app_name = "files"

urlpatterns = [
	url(r'^$', views.index, name='temp_index'), # temporary index
	url(r'^upload/$', views.myFBsite.upload_file, name='upload'),
	url(r'^index/$', views.myFBsite.file_browse, name='browse'),
	url(r'^newdrct/$', views.myFBsite.create_dir, name='create_dir'),
	url(r'^detail/$', views.myFBsite.detail, name='detail'),
	url(r'^delete/$', views.myFBsite.delete, name='f_delete'),
	url(r'^download/$', views.myFBsite.download, name='f_download'),
	# url(r'^success/$', views.success, name='success'),
]