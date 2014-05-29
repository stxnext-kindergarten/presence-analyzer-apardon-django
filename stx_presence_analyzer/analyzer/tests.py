# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""

from django.test import TestCase
import os.path
import datetime
import unittest
import json
from stx_presence_analyzer.analyzer import utils


# pylint: disable=E1103
class PresenceAnalyzerViewsTestCase(TestCase):
    """
    Views tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        pass

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_home_page(self):
        """
        Tests home page template
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'presence_weekday.html')

    def test_mean_time_presence(self):
        """
        Tests mean time presence template
        """
        response = self.client.get('/mean_time_presence/')
        self.assertTemplateUsed(response, 'mean_time_weekday.html')

    def test_presence_start_end(self):
        """
        Tests presence start-end template
        """
        response = self.client.get('/presence_start_end/')
        self.assertTemplateUsed(response, 'presence_start_end.html')

    def test_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['active_page'], 'presence_weekday'
        )
        response = self.client.get('/mean_time_presence/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['active_page'], 'mean_time_weekday'
        )
        response = self.client.get('/presence_start_end/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['active_page'], 'presence_start_end'
        )

    def test_users(self):
        """
        Test users listing.
        """
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_api(self):
        response = self.client.get('/api/presence_weekday/10/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/mean_time_presence/30/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/presence_start_end/20/')
        self.assertEqual(response.status_code, 200)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        pass

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_get_data(self):
        """
        Test parsing of CSV file.
        """
        data = utils.get_data('runtime/data/test_data.csv')
        self.assertIsInstance(data, dict)
        self.assertItemsEqual(data.keys(), [10, 11])
        sample_date = datetime.date(2013, 9, 10)
        self.assertIn(sample_date, data[10])
        self.assertItemsEqual(data[10][sample_date].keys(), ['start', 'end'])
        self.assertEqual(data[10][sample_date]['start'],
                         datetime.time(9, 39, 5))

    def test_mean(self):
        """
        Test calculating arithmetic mean
        """
        self.assertIsInstance(utils.mean([1, 2, 3]), float)
        self.assertEqual(utils.mean([1, 2, 3]), 2)
        self.assertEqual(utils.mean([-10, 10]), 0)

    def test_seconds_since_midnight(self):
        """
        Test calculating amount on seconds since midnight
        """
        self.assertIsInstance(utils.seconds_since_midnight(
            datetime.datetime.now()), int)
        self.assertEqual(
            utils.seconds_since_midnight(datetime.time(2, 30, 15)), 9015)

    def test_interval(self):
        """
        Test calculating interval between two datetime.time objects in seconds
        """
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.assertIsInstance(utils.interval(start, end), int)
        self.assertEqual(utils.interval(start, end), 3600)

    def test_group_by_weekday(self):
        """
        Test groups presence entris by weekday
        """
        sample_data = utils.get_data('runtime/data/test_data.csv')
        grouped_sample = utils.group_by_weekday(sample_data[10])
        expected_result_for_empty_dict = {i: [] for i in range(7)}
        expected_result_for_grouped_sample = {
            0: [],
            1: [30047],
            2: [24465],
            3: [23705],
            4: [],
            5: [],
            6: []
        }
        self.assertEqual(len(grouped_sample), 7)
        self.assertIsInstance(grouped_sample, dict)
        self.assertEqual(
            utils.group_by_weekday({}), expected_result_for_empty_dict)
        self.assertEqual(grouped_sample, expected_result_for_grouped_sample)

    def test_group_start_end_by_weekday(self):
        """
        Test grouping start and end time by weekday
        """
        expected_result = {
            0: {
                'starts': [], 'ends': []
            },
            1: {
                'starts': [34745], 'ends': [64792]
            },
            2: {
                'starts': [33592], 'ends': [58057]
            },
            3: {
                'starts': [38926], 'ends': [62631]
            },
            4: {
                'starts': [], 'ends': []
            },
            5: {
                'starts': [], 'ends': []
            },
            6: {
                'starts': [], 'ends': []
            }
        }
        data = utils.get_data('runtime/data/test_data.csv')
        sample_data = utils.group_start_end_by_weekday(data[10])
        self.assertIsInstance(sample_data, dict)
        self.assertEqual(len(sample_data), 7)
        self.assertEqual(sample_data, expected_result)

    def test_parse_users_xml(self):
        """
        Test xml parser
        """
        parsed_data = utils.parse_users_xml('runtime/data/test_users.xml')
        expected_result = {'user_id': 19, 'name': 'Anna K.'}
        self.assertEqual(len(parsed_data), 8)
        self.assertIsInstance(parsed_data, list)
        self.assertEqual(parsed_data[5], expected_result)


def suite():
    """
    Default test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
