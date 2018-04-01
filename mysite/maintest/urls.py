from django.conf.urls import url

from . import views

app_name = "maintest"

urlpatterns = [
	url(r'^index/$', views.index, name='index'),
	url(r'^test/$', views.test, name='test'),
	url(r'^arith_result/$', views.arithmetic_app, name='arith_result'),

]