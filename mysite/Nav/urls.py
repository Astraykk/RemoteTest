from django.conf.urls import url

from . import views


urlpatterns = [
 #   url(r'^$', views.index, name='index'),
    url(r'^$', views.home, name='home'),
    url(r'^getTree/',views.getTree,name="getTree"),
	url(r'^getGroupTree/',views.getGroupTree,name="getGroupTree"),
	url(r'^edit_file/',views.edit_file,name="edit_file"),
	url(r'^save_file/',views.save_file,name="save_file"),
	url(r'^edit_file4group/',views.edit_file4group,name="edit_file4group"),
	url(r'^save_file4group/',views.save_file4group,name="save_file4group"),
]
