from unittest import mock
from unittest.mock import Mock

from django.http import HttpResponse
from django.test import TestCase, RequestFactory

from slack_utils.views import CommandView


class CommandViewCase(TestCase):
    def test_verification(self):
        with mock.patch('slack_utils.decorators.verify_request') as verify_mock:
            view = CommandView()
            view.dispatch(Mock())
        self.assertTrue(verify_mock.called)

    def test_parses_slack_arguments(self):
        factory = RequestFactory()

        request = factory.post('/path', dict(
            token='token',
            team_id='team_id',
            team_domain='team_domain',
            enterprise_id='enterprise_id',
            enterprise_name='enterprise_name',
            channel_id='channel_id',
            channel_name='channel_name',
            user_id='user_id',
            user_name='user_name',
            command='command',
            text='text',
            response_url='http://responseurl.com/path',
            trigger_id='trigger_id',
        ))

        with mock.patch('slack_utils.decorators.verify_request', return_value=True):
            view = CommandView()
            with mock.patch.object(view, 'handle_command', return_value=HttpResponse()) as handle_command_mock:
                resp = view.post(request)

        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertTrue(handle_command_mock.called)
        self.assertTupleEqual(handle_command_mock.call_args[0], ('command', 'text'))
        self.assertDictEqual(handle_command_mock.call_args[1], dict(
            token='token',
            team_id='team_id',
            team_domain='team_domain',
            enterprise_id='enterprise_id',
            enterprise_name='enterprise_name',
            channel_id='channel_id',
            channel_name='channel_name',
            user_id='user_id',
            user_name='user_name',
            response_url='http://responseurl.com/path',
            trigger_id='trigger_id',
        ))

    def test_validation_failed(self):
        factory = RequestFactory()

        request = factory.post('/path', dict(
            token='token',
            team_id='team_id',
            team_domain='team_domain',
            enterprise_id='enterprise_id',
            enterprise_name='enterprise_name',
            channel_id='channel_id',
            channel_name='channel_name',
            user_id='user_id',
            user_name='user_name',
            command='command',
            text='text',
            response_url='responseurl',
            trigger_id='trigger_id',
        ))

        with mock.patch('slack_utils.decorators.verify_request', return_value=True):
            view = CommandView()
            with mock.patch.object(view, 'handle_command', return_value=HttpResponse()) as handle_command_mock:
                resp = view.post(request)

        self.assertEqual(resp.status_code, 400)
        self.assertFalse(handle_command_mock.called)


