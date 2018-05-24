# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from babybuddy.models import Settings


class SettingsTestCase(TestCase):
    def setUp(self):
        call_command('migrate', verbosity=0)

    def test_settings(self):
        credentials = {
            'username': 'Test',
            'password': 'User'
        }
        user = User.objects.create_user(is_superuser=True, **credentials)
        self.assertIsInstance(user.settings, Settings)
        self.assertEqual(str(user.settings), 'Test\'s Settings')
        self.assertEqual(
            user.settings.dashboard_refresh_rate_milliseconds, 60000)

        user.settings.dashboard_refresh_rate = None
        user.save()
        self.assertIsNone(user.settings.dashboard_refresh_rate_milliseconds)
