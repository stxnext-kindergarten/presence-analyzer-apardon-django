from django.shortcuts import render
from django.views.generic import TemplateView
from stx_presence_analyzer.analyzer import utils
from django import http
from django.http import HttpResponse
import calendar
import json
import logging
log = logging.getLogger(__name__)  # pylint: disable-msg=C0103


class PresenceWeekday(TemplateView):
    template_name = 'presence_weekday.html'

    def get_context_data(self, **kwargs):
        context = super(PresenceWeekday, self).get_context_data(**kwargs)
        user_id = kwargs.get('user_id')

        users = utils.parse_users_xml()
        data = utils.get_data()

        if user_id not in data:
            context['users'] = users
            context['active_page'] = 'presence_weekday'
            return context

        weekdays = utils.group_by_weekday(data[user_id])
        result = [(calendar.day_abbr[weekday], sum(intervals))
                  for weekday, intervals in weekdays.items()]

        result.insert(0, ('Weekday', 'Presence (s)'))

        context['users'] = users
        context['presence_weekday'] = result
        context['active_page'] = 'presence_weekday'

        return context


class MeanTimePresence(TemplateView):
    template_name = 'mean_time_weekday.html'

    def get_context_data(self, **kwargs):
        context = super(MeanTimePresence, self).get_context_data(**kwargs)
        user_id = kwargs.get('user_id')

        data = utils.get_data()
        users = utils.parse_users_xml()

        if user_id not in data:
            context['users'] = users
            context['active_page'] = 'mean_time_weekday'
            return context

        weekdays = utils.group_by_weekday(data[user_id])
        result = [(calendar.day_abbr[weekday], utils.mean(intervals))
                  for weekday, intervals in weekdays.items()]

        context['users'] = users
        context['mean_time_weekday'] = result
        context['active_page'] = 'mean_time_weekday'

        return context


class PresenceStartEnd(TemplateView):
    template_name = 'presence_start_end.html'

    def get_context_data(self, **kwargs):
        context = super(PresenceStartEnd, self).get_context_data(**kwargs)
        user_id = kwargs.get('user_id')

        users = utils.parse_users_xml()
        data = utils.get_data()

        if user_id not in data:
            context['users'] = users
            context['active_page'] = 'presence_start_end'
            return context

        start_end_by_weekday = utils.group_start_end_by_weekday(data[user_id])

        result = [
            (
                calendar.day_abbr[weekday],
                utils.mean(intervals['starts']),
                utils.mean(intervals['ends'])
            )
            for weekday, intervals in start_end_by_weekday.items()
        ]

        context['users'] = users
        context['presence_start_end'] = result
        context['active_page'] = 'presence_start_end'

        return context


class Users(TemplateView):
    template_name = 'users.html'

    def get_context_data(self, **kwargs):
        context = super(Users, self).get_context_data(**kwargs)
        context['users'] = utils.parse_users_xml()
        return context
