"""urlybird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from crisco.views import AllBookmarks,UserPage,HomePage,BookmarkInfo

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
       {'template_name': 'urlybird/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^recent', AllBookmarks.as_view() , name='recent'),
    url(r'^user/(?P<pk>[\w.]+)', UserPage.as_view(), name='user_page'),
    url(r'^register', 'crisco.views.register_user', name='register_user'),
    url(r'^home/(?P<pk>[\w.]+)', HomePage.as_view(), name='home_page'),
    url(r'^add', 'crisco.views.add_bookmark', name='add_bookmark'),
    url(r'^delete/(?P<bookmark_id>\d+)', 'crisco.views.delete_bookmark', name='delete_bookmark'),
    url(r'^update/(?P<bookmark_id>\d+)', 'crisco.views.edit_bookmark', name='edit_bookmark'),
    url(r'^info/(?P<pk>\w+)', BookmarkInfo.as_view(), name='bookmark_info'),
    url(r'^graph/(?P<short_url>\w+)', 'crisco.views.pie_chart', name='line_graph'),
    url(r'^stats/(?P<username>[\w.]+)', 'crisco.views.bar_chart', name='bar_chart'),
    url(r'^alltime/(?P<username>[\w.]+)', 'crisco.views.all_time', name='all_time'),
    url(r'^(?P<short_url>\w+)$', 'crisco.views.new_click', name='clickthrough'),
    url(r'^$', 'crisco.views.start'),
]
