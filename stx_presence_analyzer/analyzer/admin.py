"""
Admin panel
"""

from django.contrib import admin

from stx_presence_analyzer.analyzer.models import Presence, User

admin.site.register(User)
admin.site.register(Presence)
