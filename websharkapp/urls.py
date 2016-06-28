from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<trace_id_str>[0-9]+)/$', views.show_trace, name='show_trace'),
    url(r'^new/$', views.new_trace, name='new_trace'),
]
