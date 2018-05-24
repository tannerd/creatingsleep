# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.test import Client as HttpClient
from django.utils import timezone

from faker import Factory

from core import models


class ViewsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ViewsTestCase, cls).setUpClass()
        fake = Factory.create()
        call_command('migrate', verbosity=0)
        call_command('fake', verbosity=0)

        cls.c = HttpClient()

        fake_user = fake.simple_profile()
        cls.credentials = {
            'username': fake_user['username'],
            'password': fake.password()
        }
        cls.user = User.objects.create_user(
            is_superuser=True, **cls.credentials)

        cls.c.login(**cls.credentials)

    def test_child_views(self):
        page = self.c.get('/children/')
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/children/add/')
        self.assertEqual(page.status_code, 200)

        entry = models.Child.objects.first()
        page = self.c.get('/children/{}/'.format(entry.slug))
        self.assertEqual(page.status_code, 200)
        page = self.c.get(
            '/children/{}/'.format(entry.slug),
            {'date': timezone.localdate() - timezone.timedelta(days=1)})
        self.assertEqual(page.status_code, 200)

        page = self.c.get('/children/{}/edit/'.format(entry.slug))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/children/{}/delete/'.format(entry.slug))
        self.assertEqual(page.status_code, 200)

    def test_diaperchange_views(self):
        page = self.c.get('/changes/')
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/changes/add/')
        self.assertEqual(page.status_code, 200)

        entry = models.DiaperChange.objects.first()
        page = self.c.get('/changes/{}/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/changes/{}/delete/'.format(entry.id))
        self.assertEqual(page.status_code, 200)

    def test_feeding_views(self):
        page = self.c.get('/feedings/')
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/feedings/add/')
        self.assertEqual(page.status_code, 200)

        entry = models.Feeding.objects.first()
        page = self.c.get('/feedings/{}/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/feedings/{}/delete/'.format(entry.id))
        self.assertEqual(page.status_code, 200)

    def test_note_views(self):
        page = self.c.get('/notes/')
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/notes/add/')
        self.assertEqual(page.status_code, 200)

        entry = models.Note.objects.first()
        page = self.c.get('/notes/{}/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/notes/{}/delete/'.format(entry.id))
        self.assertEqual(page.status_code, 200)

    def test_sleep_views(self):
        page = self.c.get('/sleep/')
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/sleep/add/')
        self.assertEqual(page.status_code, 200)

        entry = models.Sleep.objects.first()
        page = self.c.get('/sleep/{}/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/sleep/{}/delete/'.format(entry.id))
        self.assertEqual(page.status_code, 200)

    def test_timer_views(self):
        page = self.c.get('/timers/')
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/timer/add/')
        self.assertEqual(page.status_code, 200)

        page = self.c.get('/timer/add/quick/')
        self.assertEqual(page.status_code, 302)
        entry = models.Timer.objects.first()
        page = self.c.get('/timer/{}/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/timer/{}/edit/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/timer/{}/delete/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/timer/{}/stop/'.format(entry.id))
        self.assertEqual(page.status_code, 302)
        page = self.c.get('/timer/{}/restart/'.format(entry.id))
        self.assertEqual(page.status_code, 302)

    def test_tummytime_views(self):
        page = self.c.get('/tummy-time/')
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/tummy-time/add/')
        self.assertEqual(page.status_code, 200)

        entry = models.TummyTime.objects.first()
        page = self.c.get('/tummy-time/{}/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/tummy-time/{}/delete/'.format(entry.id))
        self.assertEqual(page.status_code, 200)

    def test_weight_views(self):
        page = self.c.get('/weight/')
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/weight/add/')
        self.assertEqual(page.status_code, 200)

        entry = models.Weight.objects.first()
        page = self.c.get('/weight/{}/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
        page = self.c.get('/weight/{}/delete/'.format(entry.id))
        self.assertEqual(page.status_code, 200)
