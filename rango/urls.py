# from django.conf.urls import patterns, url
# from django.conf.urls import patterns, url
# from django.conf import settings
# from django.conf.urls import include, url

from django.conf.urls import url, patterns

from rango import views


urlpatterns = [
    url(regex=r'^$', view=views.index, name='index'),
    url(regex=r'^about/$', view=views.about, name='about'),
    url(regex=r'^add_category/$', view=views.add_category, name='add_category'),
    url(regex=r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', view=views.add_page, name='add_page'),
    url(regex=r'^category/(?P<category_name_slug>[\w\-]+)/$',
        view=views.category, name='category'),
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    # url(r'^logout/$', views.user_logout, name='logout')
]
# urlpatterns = patterns('',
#         url(r'^$', views.index, name='index'),
#         url(r'^about/$', views.about, name='about'),
#         url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'), )
