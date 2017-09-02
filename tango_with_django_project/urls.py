from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from registration.backends.simple.views import RegistrationView


class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/rango/'


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),  # ADD THIS NEW TUPLE!
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    )

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
            'serve', {'document_root': settings.MEDIA_ROOT}),
    )
