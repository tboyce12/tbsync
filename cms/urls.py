from django.conf.urls import patterns, url

from cms import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^sync', views.sync, name='sync'),
)
