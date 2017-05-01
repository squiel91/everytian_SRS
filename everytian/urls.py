from django.conf.urls import include, url
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False),
        name="favicon"
    ),
    url(r'^api/', include('api.urls'), name="domain_host"),
    url(r'^', RedirectView.as_view(
            url=staticfiles_storage.url('HSK5.html'),
            permanent=False),
        name="HSK5"
    )
    # url(r'^', include('web.urls'))

]
