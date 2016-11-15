from django.conf.urls import url
from .views import practice, login, logout, index, register, favorites, evolution, settings

urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^register$', register, name='register'),
	url(r'^login$', login, name='login'),
	url(r'^logout$', logout, name='logout'),

	url(r'^practice$', practice, name='practice'),
	url(r'^favorites$', favorites, name='favorites'),
	url(r'^evolution$', evolution, name='evolution'),
	url(r'^settings$', settings, name='settings'),
]
