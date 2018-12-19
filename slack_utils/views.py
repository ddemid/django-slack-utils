import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View

from slack_utils import signals
from slack_utils.decorators import slack_view
from slack_utils.forms import CommandForm


class SlackView(View):
    @method_decorator(slack_view)
    def dispatch(self, request, *args, **kwargs):
        return super(SlackView, self).dispatch(request, *args, **kwargs)


class CommandView(SlackView):
    def handle_command(self, command, text, **kwargs):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        form = CommandForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.pop('text')
            command = form.cleaned_data.pop('command')
            return self.handle_command(command, text, **form.cleaned_data)

        return HttpResponseBadRequest('Invalid request')


class EventsView(SlackView):
    def handle_event(self, event_type, event_data=None, **kwargs):
        signals.event_received.send(sender=EventsView, event_type=event_type, event_data=event_data, **kwargs)
        return JsonResponse({})

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))

        try:
            request_type = json_data.pop('type')

            # process url verification handshake
            if request_type == 'url_verification':
                return JsonResponse({'challenge': json_data['challenge']})

            if request_type == 'event_callback':
                event_data = json_data.pop('event')
                event_type = event_data.pop('type')

                return self.handle_event(event_type, event_data, **json_data)

            # process rate limiting
            if request_type == 'app_rate_limited':
                return JsonResponse({})
        except KeyError:
            return HttpResponseBadRequest()
