from functools import wraps
from django.http import HttpResponseBadRequest

from slack_utils.verification import verify_request
from slack_utils import signals


def slack_view(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not verify_request(request):
            return HttpResponseBadRequest("`X-Slack-Signature` verification failed")
        return view_func(request, *args, **kwargs)

    wrapped_view.csrf_exempt = True
    return wraps(view_func)(wrapped_view)


def slack_receiver(event_type_):
    def decorator_receiver(receiver_func):
        @wraps(receiver_func)
        def signal_receiver(sender, event_type, event_data, signal, **kwargs):
            if event_type == event_type_:
                return receiver_func(event_data, **kwargs)

        signals.event_received.connect(signal_receiver, weak=False)

    return decorator_receiver
