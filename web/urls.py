from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^list_users$', views.list_users, name='list_users'),
    url(r'^create_user$', views.create_user, name='create_user')
]
