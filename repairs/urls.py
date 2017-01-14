from django.conf.urls import url

from . import views

app_name = 'repairs'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^quotation/$', views.repair_quotation, name='quotation'),
    url(r'^comfirm_address/$', views.comfirm_address_for_job, name='comfirm_address'),
    url(r'^quotation/thanks/$', views.thanks,name='thanks'),
    url(r'^request_update/(?P<job_id>[0-9]+)$', views.request_update,name='request_update'),
    url(r'^address/(?P<job_id>[0-9]+)$', views.address_view, name='address'),
    
    
]
