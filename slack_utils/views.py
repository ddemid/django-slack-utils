from django.utils.decorators import method_decorator
from django.views import View

from slack_utils.decorators import slack_view


class SlackView(View):
    @method_decorator(slack_view)
    def dispatch(self, request, *args, **kwargs):
        return super(SlackView, self).dispatch(request, *args, **kwargs)


