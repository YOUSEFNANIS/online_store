from urllib.parse import parse_qs, urlparse

from django.core import mail
from django.core.cache import cache
from django.test import override_settings
from rest_framework.test import APITestCase

from .models import User
from .tests import GOOD_PASSWORD, make_customer


def link_params(message):
    link = next(line for line in message.body.splitlines() if line.startswith('http'))
    return {k: v[0] for k, v in parse_qs(urlparse(link).query).items()}


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class EmailFlowTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.cust = make_customer()

    def test_signup_sends_verification_and_link_verifies(self):
        payload = {'first_name': 'Ali', 'last_name': 'Ahmed', 'email': 'ali@x.com',
                   'password': GOOD_PASSWORD, 'phone_number': '0911111111'}
        with self.captureOnCommitCallbacks(execute=True):
            self.assertEqual(self.client.post('/signup/customer/', payload).status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        user = User.objects.get(email='ali@x.com')
        self.assertFalse(user.email_verified)
        params = link_params(mail.outbox[0])
        self.assertEqual(self.client.post('/signup/verify-email/', params).status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.email_verified)
        # Token is single-use: it stops working once the address is verified.
        self.assertEqual(self.client.post('/signup/verify-email/', params).status_code, 400)

    def test_bad_verification_token(self):
        self.assertEqual(self.client.post('/signup/verify-email/', {'uid': 'abc', 'token': 'nope'}).status_code, 400)

    def test_password_reset_flow(self):
        self.assertEqual(self.client.post('/signup/password-reset/', {'email': self.cust.user.email}).status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        params = link_params(mail.outbox[0])
        weak = self.client.post('/signup/password-reset/confirm/', {**params, 'password': 'weak'})
        self.assertEqual(weak.status_code, 400)
        new_password = 'N3w!password'
        ok = self.client.post('/signup/password-reset/confirm/', {**params, 'password': new_password})
        self.assertEqual(ok.status_code, 200, ok.content)
        self.cust.user.refresh_from_db()
        self.assertTrue(self.cust.user.check_password(new_password))
        # Reusing the link fails because the password hash changed.
        again = self.client.post('/signup/password-reset/confirm/', {**params, 'password': 'An0ther!pass'})
        self.assertEqual(again.status_code, 400)

    def test_unknown_email_gets_same_answer_and_no_mail(self):
        self.assertEqual(self.client.post('/signup/password-reset/', {'email': 'nobody@x.com'}).status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_me_reports_verification_state(self):
        self.client.force_authenticate(self.cust.user)
        self.assertIn('email_verified', self.client.get('/signup/get_id/me/').json())
