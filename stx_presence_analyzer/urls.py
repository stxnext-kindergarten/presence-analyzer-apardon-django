from django.conf.urls import patterns, url
from django.contrib import admin
from stx_presence_analyzer.analyzer import views

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.PresenceWeekday.as_view()),
    url(r'^(?P<user_id>\d+)/$', views.PresenceWeekday.as_view()),
    url(r'^mean_time_presence/$', views.MeanTimePresence.as_view()),
    url(r'^mean_time_presence/(?P<user_id>\d+)/$',
        views.MeanTimePresence.as_view()),
    url(r'^presence_start_end/$', views.PresenceStartEnd.as_view()),
    url(r'^presence_start_end/(?P<user_id>\d+)/$',
        views.PresenceStartEnd.as_view()),
    url(r'^users/$', views.Users.as_view()),
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
