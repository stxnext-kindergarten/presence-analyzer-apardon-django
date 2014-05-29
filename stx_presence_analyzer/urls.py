"""
Defines urls
"""

from django.conf.urls import patterns, url
from django.contrib import admin
from stx_presence_analyzer.analyzer import views

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^api/presence_weekday/(?P<user_id>\d+)/$',
        views.APIPresenceWeekday.as_view()),
    url(r'^api/mean_time_presence/(?P<user_id>\d+)/$',
        views.APIMeanTimePresence.as_view()),
    url(r'^api/presence_start_end/(?P<user_id>\d+)/$',
        views.APIPresenceStartEnd.as_view()),
    url(r'^users/$', views.Users.as_view()),
    url(r'^$', views.MainPage.as_view()),
    url(r'^mean_time_presence/$', views.MeanTimePresence.as_view()),
    url(r'^presence_start_end/$', views.PresenceStartEnd.as_view()),
)
