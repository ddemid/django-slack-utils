from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View

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