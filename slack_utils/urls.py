from django.conf.urls import url

from slack_utils import views

urlpatterns = [
    url('events/$', views.EventsView.as_view(), name='slack-events-api'),
]
