from accounts import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [

    # Register new user
    url(r'^login_signup/', views.signup_user, name='signup_user'),

    # Login URL
    url(r'^login_user/', views.login_user, name='login_user'),

    # Logout URL
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'logout.html', 'next_page': '/'}, name='logout'),

    # activation URL
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]
