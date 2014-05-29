from django.views.generic import TemplateView
from stx_presence_analyzer.analyzer import utils
import calendar
import logging
import json
from django.http import HttpResponse
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
    """docstring for MainPage"""
    template_name = 'presence_weekday.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['active_page'] = 'presence_weekday'
        return context


class MeanTimePresence(TemplateView):
    """docstring for MeanTimePresence"""
    template_name = 'mean_time_weekday.html'

    def get_context_data(self, **kwargs):
        context = super(MeanTimePresence, self).get_context_data(**kwargs)
        context['active_page'] = 'mean_time_weekday'
        return context


class PresenceStartEnd(TemplateView):
    """docstring for MeanTimePresence"""
    template_name = 'presence_start_end.html'

    def get_context_data(self, **kwargs):
        context = super(PresenceStartEnd, self).get_context_data(**kwargs)
        context['active_page'] = 'presence_start_end'
        return context


class APIPresenceWeekday(JSONResponseMixin, TemplateView):

    def get_context_data(self, **kwargs):
        user_id = kwargs.get('user_id')
        data = utils.get_data()

        weekdays = utils.group_by_weekday(data[int(user_id)])
        result = [(calendar.day_abbr[weekday], sum(intervals))
                  for weekday, intervals in weekdays.items()]

        result.insert(0, ('Weekday', 'Presence (s)'))

        return result


class APIMeanTimePresence(JSONResponseMixin, TemplateView):

    def get_context_data(self, **kwargs):
        user_id = kwargs.get('user_id')
        data = utils.get_data()

        weekdays = utils.group_by_weekday(data[int(user_id)])
        result = [(calendar.day_abbr[weekday], utils.mean(intervals))
                  for weekday, intervals in weekdays.items()]

        return result


class APIPresenceStartEnd(JSONResponseMixin, TemplateView):

    def get_context_data(self, **kwargs):
        user_id = kwargs.get('user_id')
        data = utils.get_data()

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
    """docstring for Users"""

    def get_context_data(self, **kwargs):
        return utils.parse_users_xml()
