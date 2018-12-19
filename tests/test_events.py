import json
from unittest import mock

from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse

from slack_utils import signals


class EventsViewTestCase(TestCase):
    def test_verification(self):
        with mock.patch('slack_utils.decorators.verify_request') as verify_mock:
            resp = self.client.post(reverse('slack-events-api'), "{}", content_type='application/json')
        self.assertTrue(verify_mock.called)

    def test_url_verification_handshake(self):

        with mock.patch('slack_utils.decorators.verify_request', return_value=True):
            resp = self.client.post(reverse('slack-events-api'), json.dumps({
                "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",
                "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",
                "type": "url_verification"
            }), content_type='application/json')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         JsonResponse({"challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"}).content)

    def test_app_rate_limited(self):
        with mock.patch('slack_utils.decorators.verify_request', return_value=True):
            resp = self.client.post(reverse('slack-events-api'), json.dumps({
                "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",
                "type": "app_rate_limited",
                "team_id": "T123456",
                "minute_rate_limited": 1518467820,
                "api_app_id": "A123456"
        }), content_type='application/json')

        self.assertEqual(resp.status_code, 200)

    def test_event(self):

        def handler(sender, event_type, event_data, signal, **kwargs):
            handler.signal_was_called = True
            handler.event_type = event_type
            handler.event_data = event_data
            handler.kwargs = kwargs

        signals.event_received.connect(handler)

        try:
            with mock.patch('slack_utils.decorators.verify_request', return_value=True):
                resp = self.client.post(reverse('slack-events-api'), json.dumps({
                    "token": "z26uFbvR1xHJEdHE1OQiO6t8",
                    "team_id": "T061EG9RZ",
                    "api_app_id": "A0FFV41KK",
                    "event": {
                        "type": "reaction_added",
                        "user": "U061F1EUR",
                        "item": {
                            "type": "message",
                            "channel": "C061EG9SL",
                            "ts": "1464196127.000002"
                        },
                        "reaction": "slightly_smiling_face",
                        "item_user": "U0M4RL1NY",
                        "event_ts": "1465244570.336841"
                    },
                    "type": "event_callback",
                    "authed_users": [
                        "U061F7AUR"
                    ],
                    "event_id": "Ev9UQ52YNA",
                    "event_time": 1234567890
                }), content_type='application/json')
        finally:
            signals.event_received.disconnect(handler)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(handler.signal_was_called)
        self.assertEqual(handler.event_type, 'reaction_added')
        self.assertDictEqual(handler.event_data, {
                "user": "U061F1EUR",
                "item": {
                    "type": "message",
                    "channel": "C061EG9SL",
                    "ts": "1464196127.000002"
                },
                "reaction": "slightly_smiling_face",
                "item_user": "U0M4RL1NY",
                "event_ts": "1465244570.336841"
            })

        self.assertDictEqual(handler.kwargs, {
            "token": "z26uFbvR1xHJEdHE1OQiO6t8",
            "team_id": "T061EG9RZ",
            "api_app_id": "A0FFV41KK",
            "authed_users": [
                "U061F7AUR"
            ],
            "event_id": "Ev9UQ52YNA",
            "event_time": 1234567890
        })