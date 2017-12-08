from django.conf.urls import url

from . import views

app_name = "files"

urlpatterns = [
	url(r'^$', views.index, name='temp_index'), # temporaray index
	url(r'^upload/$', views.upload_file, name='upload'),
	url(r'^index/$', views.site.file_browse, name='browse'),
	url(r'^newdrct/$', views.site.create_dir, name='create_dir'),

	#url(r'^success/$', views.success, name='success'),
]