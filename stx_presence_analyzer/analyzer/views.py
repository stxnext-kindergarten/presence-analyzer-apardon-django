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

log = logging.getLogger(__name__)  # pylint: disable=C0103


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
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


class APIPresenceWeekday(JSONResponseMixin, TemplateView):
    """
    Returns total presence time of given user grouped by weekday.
    """
    def get_context_data(self, **kwargs):
        user_id = kwargs.get('user_id')
        data = utils.get_data('runtime/data/sample_data.csv')

        weekdays = utils.group_by_weekday(data[int(user_id)])
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
        data = utils.get_data('runtime/data/sample_data.csv')

        weekdays = utils.group_by_weekday(data[int(user_id)])
        result = [(calendar.day_abbr[weekday], utils.mean(intervals))
                  for weekday, intervals in weekdays.items()]

        return result


class APIPresenceStartEnd(JSONResponseMixin, TemplateView):
    """
    Return average presence time of given user
    """
    def get_context_data(self, **kwargs):
        user_id = kwargs.get('user_id')
        data = utils.get_data('runtime/data/sample_data.csv')

        start_end_by_weekday = utils.group_start_end_by_weekday(
            data[int(user_id)])

        return [
            (
                calendar.day_abbr[weekday],
                utils.mean(intervals['starts']),
                utils.mean(intervals['ends'])
            )
            for weekday, intervals in start_end_by_weekday.items()
        ]


class Users(JSONResponseMixin, TemplateView):
    """"
    Users listing for dropdown.
    """
    def get_context_data(self, **kwargs):
        return utils.parse_users_xml('runtime/data/users.xml')
