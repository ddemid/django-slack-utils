# django-slack-utils [![Build Status](https://travis-ci.com/startmatter/django-slack-utils.svg?branch=master)](https://travis-ci.com/startmatter/django-slack-utils) [![Coverage Status](https://coveralls.io/repos/github/startmatter/django-slack-utils/badge.svg?branch=master)](https://coveralls.io/github/startmatter/django-slack-utils?branch=master)

Django-slack-utils is helper application to handle Slack requests. 

It supports verification through `HTTP_X_SLACK_SIGNATURE` and `HTTP_X_SLACK_REQUEST_TIMESTAMP`.

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

### View decorator
The `@slack_view` decorator adds CSRF exempt and verification to your function-based django view.

```python
from slack_utils.decorators import slack_view
from django.http import HttpResponse

@slack_view
def sample_view(request, *args, **kwargs):
    # your logic
    return HttpResponse("Hello!")

```


### Class-based view

The `SlackView`  base class adds CSRF exempt and verification to your class-based django view.

```python
from slack_utils.views import SlackView
from django.http import HttpResponse

class SampleView(SlackView):
    def post(self, request, *args, **kwargs):
        # your logic
        return HttpResponse("Hello!")

```


### Slash command
To easily handle [Slack slash commands](https://api.slack.com/slash-commands), use `CommandView` as a base class for your class-based views.


```python
from slack_utils.views import CommandView
from django.http import HttpResponse

class SampleCommandView(CommandView):
    def handle_command(self, command, text, **kwargs):
        return HttpResponse("Hello!")
```

`**kwargs`would get the rest of the data from Slack request

### Events API

To handle [Slack events](https://api.slack.com/events-api) add the following to your `urls.py`
```python
    from django.conf.urls import include
    from django.urls import path
    
    urlpatterns = [
        ...
        path('slack/', include('slack_utils.urls')),
    ]

```

Event handler subscription can be done in two ways:

#### Receiver decorator
Put them into `slack_events.py` of your app or make sure it's loadded once. 

```python
from slack_utils.decorators import slack_receiver

@slack_receiver('reaction_added')
def on_reaction_added(event_data, **kwargs):
    # your logic 
 
```

#### Signal

```python
from slack_utils.signals import event_received
from django.dispatch import receiver

@receiver(event_received)
def on_event_received(sender, event_type, event_data, **kwargs):
    if event_type == 'reaction_added':
        # your logic 

    # your other logic 
 
```
