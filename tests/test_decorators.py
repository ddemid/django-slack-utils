from unittest import mock
from unittest.mock import Mock

from django.test import TestCase

from slack_utils.commands import registry
from slack_utils.decorators import slack_view, slack_receiver, slack_command
from slack_utils.signals import event_received


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


class SlackReceiverDecoratorTestCase(TestCase):
    def test_receiver_called(self):
        on_reaction_added = Mock()

        slack_receiver('reaction_added')(on_reaction_added)

        event_received.send(SlackReceiverDecoratorTestCase, event_type='reaction_added', event_data={}, test=1)

        self.assertTrue(on_reaction_added.called)
        self.assertTupleEqual(on_reaction_added.call_args[0], ({},))
        self.assertDictEqual(on_reaction_added.call_args[1], dict(test=1))

    def test_receiver_not_called(self):
        on_reaction_added = Mock()

        slack_receiver('message')(on_reaction_added)

        event_received.send(SlackReceiverDecoratorTestCase, event_type='reaction_added', event_data={}, test=1)

        self.assertFalse(on_reaction_added.called)


class SlackCommandDecoratorTestCase(TestCase):

    def tearDown(self):
        registry.clear()

    def test_registers(self):
        def handler(text, **kwargs):
            pass

        with mock.patch('slack_utils.decorators.registry.register') as register_mock:
            slack_command('/test')(handler)

        self.assertTrue(register_mock.called)
        self.assertTupleEqual(register_mock.call_args[0], ('/test', handler, ))
