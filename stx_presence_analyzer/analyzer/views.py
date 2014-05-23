from django.shortcuts import render
from django.views.generic import TemplateView
from stx_presence_analyzer.analyzer import utils
from django import http
from django.utils import simplejson


# Create your views here.
class JSONResponseMixin(object):
    def render_to_response(self, context):
        """
        Returns a JSON respone containing 'context' as payload
        """
        return self.get_json_respone(self.convert_context_to_json(context))

    def get_json_response(self, context, **httpresponse_kwargs):
        return http.HttpResponse(
            context, content_type="application/json", **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return simplejson.dumps(context)

    def get_data(self):
        """
        """
        user_id = self.kwargs['user_id']
        data = PresenceWeekday.objects.filter(user__legacy_id=user_id)
        if not data:
            logger.debug('User %s not found!', user_id)
            return {}

        data_presence_dict = {
            presence.day:
                {
                    'start': presence.start,
                    'end': presence.end
                } for presence in data}

        return data_presence_dict


class PresenceWeekday(JSONResponseMixin, TemplateView):
    """
    Renders 'Presence by weekday' page
    """
    template_name = 'presence_weekday.html'

    def get_conextx_data(self):
        data = self.get_data()
        if user_id not in data:
            log.debug('User %s not found!', user_id)
            return []

        weekdays = utils.group_by_weekday(data[user_id])
        result = [(calendar.day_abbr[weekday], sum(intervals))
                  for weekday, intervals in weekdays.items()]

        result.insert(0, ('Weekday', 'Presence (s)'))
        return result


class PresenceMeanTimeWeekday(JSONResponseMixin, TemplateView):
    """
    Renders 'Presence mean time' page
    """
    template_name = 'mean_time_weekday.html'

    def get_context_data(self):
        data = self.get_data()
        if user_id not in data:
            log.debug('User %s not found!', user_id)
            return []

        weekdays = utils.group_by_weekday(data[user_id])
        result = [(calendar.day_abbr[weekday], utils.mean(intervals))
                  for weekday, intervals in weekdays.items()]

        return result


class PresenceStartEnd(JSONResponseMixin, TemplateView):
    """
    Renders 'Presence start-end' page
    """
    template_name = 'presence_start_end.html'

    def get_context_data(self, **kwargs):
        context = super(PresenceStartEnd, self).get_context_data(**kwargs)
        data = self.get_data()
        if user_id not in data:
            log.debug('User %s not found!', user_id)
            return []

        start_end_by_weekday = utils.group_start_end_by_weekday(data[user_id])

        result = [
            (
                calendar.day_abbr[weekday],
                utils.mean(intervals['starts']),
                utils.mean(intervals['ends'])
            )
            for weekday, intervals in start_end_by_weekday.items()
        ]

        return result


class Users(TemplateView):
    template_name = 'tmp.html'

    def get_context_data(self, **kwargs):
        context = super(Users, self).get_context_data(**kwargs)
        context['users'] = utils.parse_users_xml()
        return context
