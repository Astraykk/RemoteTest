from django.conf.urls import url

from . import views

app_name = "maintest"

urlpatterns = [
	url(r'^index/$', views.index, name='index'),
	url(r'^test/$', views.test, name='test'),
	url(r'^arith_result/$', views.arithmetic_app, name='arith_result'),
	url(r'^tv_ajax/$', views.treeview_ajax, name='tv_ajax'),
	url(r'^save_file/$', views.save_file, name='save_file'),

]