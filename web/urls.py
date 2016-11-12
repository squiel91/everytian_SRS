from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
	
	url(r'^practice$', views.practice, name='practice'),
	url(r'^favorites$', views.favorites, name='favorites'),
	url(r'^evolution$', views.evolution, name='evolution'),
	url(r'^settings$', views.settings, name='settings'),
]
