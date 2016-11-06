from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.list_users, name='list_users'),
    url(r'^create_user$', hello.views.create_user, name='create_user'),
    url(r'^admin/', include(admin.site.urls)),
]
