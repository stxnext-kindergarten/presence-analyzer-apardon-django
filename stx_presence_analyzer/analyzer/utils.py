# -*- coding: utf-8 -*-
"""
Helper functions used in views.
"""

import csv
from functools import wraps
from datetime import datetime
from lxml import etree
from collections import defaultdict
import threading
import time

import logging
log = logging.getLogger(__name__)  # pylint: disable=C0103


def cache(cache_time):
    """
    Caches result od function for given time
    """
    cached = defaultdict(dict)
    lock = threading.Lock()

    def is_cache_expired(function_name):
        return (time.time() - cached[function_name]['created']) > cache_time

    def decorator(function):
        @wraps(function)
        def inner(*args, **kwargs):
            func_name = repr(function) + repr(args) + repr(kwargs)
            with lock:
                if func_name not in cached or is_cache_expired(func_name):
                    cached[func_name]['data'] = function(*args, **kwargs)
                    cached[func_name]['created'] = time.time()
                return cached[func_name]['data']
        return inner
    return decorator


@cache(600)
def get_data(filename):
    """
    Extracts presence data from CSV file and groups it by user_id.

    It creates structure like this:
    data = {
        'user_id': {
            datetime.date(2013, 10, 1): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 30, 0),
            },
            datetime.date(2013, 10, 2): {
                'start': datetime.time(8, 30, 0),
                'end': datetime.time(16, 45, 0),
            },
        }
    }
    """
    data = {}
    with open(filename, 'r') as csvfile:
        presence_reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(presence_reader):
            if len(row) != 4:
                # ignore header and footer lines
                continue

            try:
                user_id = int(row[0])
                date = datetime.strptime(row[1], '%Y-%m-%d').date()
                start = datetime.strptime(row[2], '%H:%M:%S').time()
                end = datetime.strptime(row[3], '%H:%M:%S').time()
            except (ValueError, TypeError):
                log.debug('Problem with line %d: ', i, exc_info=True)

            data.setdefault(user_id, {})[date] = {'start': start, 'end': end}

    return data


def group_by_weekday(items):
    """
    Groups presence entries by weekday.
    """
    result = {i: [] for i in range(7)}
    for date in items:
        start = items[date]['start']
        end = items[date]['end']
        result[date.weekday()].append(interval(start, end))
    return result


def group_start_end_by_weekday(items):
    """
    Groups start and end by weekday.
    """
    result = {i: {'starts': [], 'ends': []} for i in range(7)}
    for date in items:
        start = items[date]['start']
        end = items[date]['end']
        result[date.weekday()]['starts'].append(seconds_since_midnight(start))
        result[date.weekday()]['ends'].append(seconds_since_midnight(end))
    return result


def seconds_since_midnight(time):
    """
    Calculates amount of seconds since midnight.
    """
    return time.hour * 3600 + time.minute * 60 + time.second


def interval(start, end):
    """
    Calculates inverval in seconds between two datetime.time objects.
    """
    return seconds_since_midnight(end) - seconds_since_midnight(start)


def mean(items):
    """
    Calculates arithmetic mean. Returns zero for empty lists.
    """
    return float(sum(items)) / len(items) if len(items) > 0 else 0


def parse_users_xml(filename):
    """
    Parses the XML file
    """

    with open(filename, 'r') as xml_file:
        users = etree.parse(xml_file).find('users')

    return [
        {
            'user_id': int(user.get('id')),
            'name': user.find('name').text
        }
        for user in users
    ]
