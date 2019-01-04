from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [

    # Register new user
    url(r'^login_signup/', views.signup_user, name='signup_user'),
    # Login URL
    url(r'^login_user/', views.login_user, name='login_user'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    # Logout URL
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html','next_page': '/products'}, name='logout'),

    # send an activation URL 
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),

    # activation URL
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]