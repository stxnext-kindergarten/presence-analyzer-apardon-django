# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar
import logging
import json
from django.http import HttpResponse
from django.views.generic import TemplateView

from stx_presence_analyzer.analyzer import utils
from stx_presence_analyzer.analyzer.models import User, Presence

log = logging.getLogger(__name__)  # pylint: disable=C0103


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def get_data(self, user_id):
        presences = Presence.objects.filter(user__user_id=user_id)

        return {
            presence.day: {
                "start": presence.start,
                "end": presence.end
            }
            for presence in presences
        }

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response containing 'context' as payload
        """
        return self.render_to_json_response(
            self.convert_context_to_json(context),
            **response_kwargs)

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            context,
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class MainPage(TemplateView):
    """
    Redirects to front page.
    """
    template_name = 'presence_weekday.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data()
        name = kwargs.get('template')
        if name is None:
            self.template_name = 'presence_weekday.html'
            context['active_page'] = 'presence_weekday'
        elif name == 'mean_time_weekday':
            self.template_name = 'mean_time_weekday.html'
            context['active_page'] = 'mean_time_weekday'
        elif name == 'presence_start_end':
            self.template_name = 'presence_start_end.html'
            context['active_page'] = 'presence_start_end'
        return context


class Users(JSONResponseMixin, TemplateView):
    """"
    Users listing for dropdown.
    """
    def get_context_data(self, **kwargs):
        users = User.objects.all()
        return [
            {
                "user_id": user.user_id,
                "name": user.name
            }
            for user in users
        ]


class APIPresenceWeekday(JSONResponseMixin, TemplateView):
    """docstring for Test"""
    def get_context_data(self, **kwargs):
        user_id = kwargs.get('user_id')

        if user_id is None:
            return []

        data = self.get_data(int(user_id))

        weekdays = utils.group_by_weekday(data)
        result = [(calendar.day_abbr[weekday], sum(intervals))
                  for weekday, intervals in weekdays.items()]

        result.insert(0, ('Weekday', 'Presence (s)'))

        return result


class APIMeanTimePresence(JSONResponseMixin, TemplateView):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    def get_context_data(self, **kwargs):
        user_id = kwargs.get('user_id')

        if user_id is None:
            return []

        data = self.get_data(int(user_id))

        weekdays = utils.group_by_weekday(data)
        result = [(calendar.day_abbr[weekday], utils.mean(intervals))
                  for weekday, intervals in weekdays.items()]

        return result


class APIPresenceStartEnd(JSONResponseMixin, TemplateView):
    """
    Return average presence time of given user
    """
    def get_context_data(self, **kwargs):
        user_id = kwargs.get('user_id')

        if user_id is None:
            return []

        data = self.get_data(int(user_id))

        start_end_by_weekday = utils.group_start_end_by_weekday(data)

        return [
            (
                calendar.day_abbr[weekday],
                utils.mean(intervals['starts']),
                utils.mean(intervals['ends'])
            )
            for weekday, intervals in start_end_by_weekday.items()
        ]
