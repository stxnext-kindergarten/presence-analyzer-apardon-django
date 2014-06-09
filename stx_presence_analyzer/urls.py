"""
Defines urls
"""

from django.conf.urls import patterns, url, include
from django.contrib import admin

from stx_presence_analyzer.analyzer import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.MainPage.as_view()),
    url(r'^(?P<template>\w+)/$', views.MainPage.as_view()),
    url(r'^api/presence_weekday/(?P<user_id>\d+)/$',
        views.APIPresenceWeekday.as_view(), name='presence_weekday_api'),
    url(r'^api/mean_time_presence/(?P<user_id>\d+)/$',
        views.APIMeanTimePresence.as_view(), name='mean_time_presence_api'),
    url(r'^api/presence_start_end/(?P<user_id>\d+)/$',
        views.APIPresenceStartEnd.as_view(), name='presence_start_end_api'),
    url(r'^api/users/$', views.Users.as_view(), name='users'),
)
