from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from django.contrib.messages import get_messages
from unittest.mock import patch

from .models import Cruise, InfoRequest


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class InfoRequestEmailTests(TestCase):

    def setUp(self):
        self.cruise = Cruise.objects.create(name='Test Cruise', description='A test cruise')

    def test_successful_submit_sends_email_and_saves(self):
        data = {
            'name': 'juan',
            'email': 'juan@example.com',
            'cruise': str(self.cruise.pk),
            'notes': 'jajajaj'
        }
        response = self.client.post(reverse('info_request'), data, follow=True)

        self.assertEqual(InfoRequest.objects.count(), 1)

        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        subject_lower = sent.subject.lower()
        # subject wording may vary; assert key parts are present
        self.assertIn('informacion', subject_lower)
        self.assertIn('recibida', subject_lower)
        self.assertIn(self.cruise.name.lower(), subject_lower)

    def test_invalid_email_shows_form_error_and_not_saved(self):
        data = {
            'name': 'pepe',
            'email': 'no email',
            'cruise': str(self.cruise.pk),
            'notes': 'email invalido test'
        }
        response = self.client.post(reverse('info_request'), data)

        self.assertEqual(InfoRequest.objects.count(), 0)

        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn('email', form.errors)

    def test_send_mail_failure_is_handled_and_message_shown(self):
        data = {
            'name': 'Carlos',
            'email': 'carlos@example.com',
            'cruise': str(self.cruise.pk),
            'notes': 'SMTP fail test'
        }

        with patch('relecloud.views.send_mail', side_effect=Exception('SMTP fail')):
            response = self.client.post(reverse('info_request'), data, follow=True)

        self.assertEqual(InfoRequest.objects.count(), 1)

        self.assertEqual(len(mail.outbox), 0)

        messages = list(response.context.get('messages', []))
        self.assertTrue(any('No se pudo enviar el email de confirmacion' in str(m) for m in messages))

