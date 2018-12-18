from unittest import mock
from django.test import TestCase
from slack_utils.decorators import slack_view


class SlackViewDecoratorTestCase(TestCase):
    def test_csrf_exempt(self):
        def test_view(*args, **kwargs):
            pass

        wrapped_view = slack_view(test_view)

        self.assertTrue(wrapped_view.csrf_exempt)

    def test_verification_failed(self):
        def test_view(*args, **kwargs):
            return 'passed'

        wrapped_view = slack_view(test_view)

        request_mock = mock.Mock()

        with mock.patch('slack_utils.decorators.verify_request', return_value=False) as verify_request_mock:
            resp = wrapped_view(request_mock)

        self.assertTrue(verify_request_mock.is_called)
        self.assertTupleEqual(verify_request_mock.call_args[0], (request_mock, ))
        self.assertEqual(resp.status_code, 400)

    def test_verification_passed(self):
        def test_view(*args, **kwargs):
            return 'passed'

        wrapped_view = slack_view(test_view)

        request_mock = mock.Mock()

        with mock.patch('slack_utils.decorators.verify_request', return_value=True) as verify_request_mock:
            resp = wrapped_view(request_mock)

        self.assertTrue(verify_request_mock.is_called)
        self.assertTupleEqual(verify_request_mock.call_args[0], (request_mock, ))
        self.assertEqual(resp, 'passed')