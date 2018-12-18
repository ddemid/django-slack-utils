from functools import wraps

from django.http import HttpResponseBadRequest

from slack_utils.verification import verify_request


def slack_view(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not verify_request(request):
            return HttpResponseBadRequest("`X-Slack-Signature` verification failed")
        return view_func(request, *args, **kwargs)

    wrapped_view.csrf_exempt = True
    return wraps(view_func)(wrapped_view)