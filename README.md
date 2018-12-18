# django-slack-utils [![Build Status](https://travis-ci.com/startmatter/django-slack-utils.svg?branch=master)](https://travis-ci.com/startmatter/django-slack-utils) [![Coverage Status](https://coveralls.io/repos/github/startmatter/django-slack-utils/badge.svg?branch=master)](https://coveralls.io/github/startmatter/django-slack-utils?branch=master)

Django-slack-utils is helper application to handle Slack requests. It supports verification through `HTTP_X_SLACK_SIGNATURE` and `HTTP_X_SLACK_REQUEST_TIMESTAMP`.

## Installation
Add the following to your `settings.py`
```python
INSTALLED_APPS = [
    ...
    'slack_utils',
]

SLACK_SIGNING_SECRET = 'your signing secret from Slack'

```

## Usage

###View decorator
```python
from slack_utils.decorators import slack_view
from django.http import HttpResponse

@slack_view
def sample_view(request, *args, **kwargs):
    # your logic
    return HttpResponse("Hello!")

```


###Class-based view
```python
from slack_utils.views import SlackView
from django.http import HttpResponse

class SampleView(SlackView):
    def post(self, request, *args, **kwargs):
        # your logic
        return HttpResponse("Hello!")

```

###Slash command parsing

https://api.slack.com/slash-commands
```python
from slack_utils.views import CommandView
from django.http import HttpResponse

class SampleCommandView(CommandView):
    def handle_command(self, command, text, **kwargs):
        return HttpResponse("Hello!")
```

`**kwargs`would get the rest of the data from Slack request