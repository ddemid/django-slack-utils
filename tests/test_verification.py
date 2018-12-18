import hashlib
import hmac
import time

from django.test import TestCase, RequestFactory
from slack_utils.verification import verify_request


class VerificationTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_no_signature(self):
        request = self.factory.post('/path')
        self.assertFalse(verify_request(request))

    def test_no_timestamp(self):
        request = self.factory.post('/path', HTTP_X_SLACK_SIGNATURE='signature')
        self.assertFalse(verify_request(request))

    def test_invalid(self):
        request = self.factory.post('/path', HTTP_X_SLACK_SIGNATURE='signature', HTTP_X_SLACK_REQUEST_TIMESTAMP='1')
        self.assertFalse(verify_request(request))

    def test_valid(self):
        timestamp = int(time.time())
        basestring = "v0:{}:data=test".format(timestamp).encode('utf-8')

        slack_signing_secret = bytes('secret', 'utf-8')

        signature = 'v0=' + hmac.new(slack_signing_secret, basestring, hashlib.sha256).hexdigest()

        request = self.factory.post('/path', 'data=test', content_type='application/x-www-form-urlencoded',
                                    HTTP_X_SLACK_SIGNATURE=signature, HTTP_X_SLACK_REQUEST_TIMESTAMP=timestamp)

        self.assertTrue(verify_request(request))