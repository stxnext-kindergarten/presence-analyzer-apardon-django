from django.conf.urls import patterns, url
from django.contrib import admin
from analyzer.views import PresenceWeekday, MeanTimePresence, PresenceStartEnd

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', PresenceWeekday.as_view()),
    url(r'^(?P<user_id>\d+)/$', PresenceWeekday.as_view()),
    url(r'^mean_time_presence/$', MeanTimePresence.as_view()),
    url(r'^mean_time_presence/(?P<user_id>\d+)/$', MeanTimePresence.as_view()),
    url(r'^presence_start_end/$', PresenceStartEnd.as_view()),
    url(r'^presence_start_end/(?P<user_id>\d+)/$', PresenceStartEnd.as_view()),
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
