from django.conf.urls import url 
from . import views

urlpatterns = [
 url(r'^$', views.index),
 url(r'^register$', views.register),
 url(r'^success$', views.success),
 url(r'^login$', views.login),
 url(r'^logout$', views.logout),
 url(r'^createitem$', views.createitem),
#  url(r'^createitem$', views.createitem),
 url(r'^userinfo', views.userinfo),
#  url(r'^remove/(?P<num>\d+)', views.remove),
#  url(r'^add/(?P<num>\d+)', views.add),
#  url(r'^delete/(?P<num>\d+)', views.delete),


]




