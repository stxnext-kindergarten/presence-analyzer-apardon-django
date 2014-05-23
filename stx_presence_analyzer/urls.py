from django.conf.urls import patterns, url
from django.contrib import admin
from analyzer.views import PresenceWeekday, PresenceMeanTimeWeekday, PresenceStartEnd, Users

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^presenceweekday/$', PresenceWeekday.as_view()),
    url(r'^meantimeweekday/$', PresenceMeanTimeWeekday.as_view()),
    url(r'^startend/$', PresenceStartEnd.as_view()),
    url(r'^users/$', Users.as_view()),
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
