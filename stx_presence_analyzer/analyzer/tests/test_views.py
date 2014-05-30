# -*- coding: utf-8 -*-
"""
Presence analyzer views unit tests.
"""

from django.test import TestCase


# pylint: disable=E1103
class PresenceAnalyzerViewsTestCase(TestCase):
    """
    Views tests.
    """
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
        response = self.client.get('/mean_time_weekday/')
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
        response = self.client.get('/mean_time_weekday/')
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
