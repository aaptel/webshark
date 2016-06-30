from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<trace_id_str>[0-9]+)/$', views.show_trace, name='show_trace'),
    url(r'^(?P<trace_id_str>[0-9]+)/info$', views.data_info, name='data_info'),
    url(r'^(?P<trace_id_str>[0-9]+)/packet-(?P<start_id_str>[0-9]+)-(?P<count_str>[0-9]+)/$', views.data_packet_list, name='data_packet_list'),
    url(r'^new/$', views.new_trace, name='new_trace'),
    url(r'^latest/$', views.latest_trace, name='latest_trace'),
]
