from django.conf.urls import url, patterns

from rango import views


urlpatterns = [
    url(regex=r'^$', view=views.index, name='index'),
    url(regex=r'^about/$', view=views.about, name='about'),
    url(regex=r'^add_category/$', view=views.add_category, name='add_category'),
    url(regex=r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        view=views.add_page, name='add_page'),
    url(regex=r'^category/(?P<category_name_slug>[\w\-]+)/$',
        view=views.category, name='category'),
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    url(regex=r'^restricted/', view=views.restricted, name='restricted'),
    # url(r'^logout/$', views.user_logout, name='logout')
    url(regex=r'^goto/$', view=views.track_url, name='goto'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
]
