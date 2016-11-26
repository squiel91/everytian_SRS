from django.conf.urls import url
from .services import resources, words

urlpatterns = [
	# url(r'^user$', settings, name='settings'), # GET
	# url(r'^user/favorites$', settings, name='settings'), # GET
	# url(r'^user/evolution$', settings, name='settings'), # GET

	# url(r'^users$', settings, name='settings'), # GET
	# url(r'^users/favorites$', settings, name='settings'), # GET
	# url(r'^users/evolution$', settings, name='settings'), # GET

	url(r'^resources(/(?P<id>[^/]+))?$', resources, name='resources'), # GET, POST, PUT
	url(r'^words(/(?P<id>[^/]+))?$', words, name='words'), # GET, POST
]
