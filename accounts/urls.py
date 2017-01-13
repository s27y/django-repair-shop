from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^$', views.profile_view, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^profile_update/$', views.profile_update, name='profile_update'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin_view, name='signin'),
    url(r'^hello/', views.hello),
    url(r'^home/', views.home),
]
