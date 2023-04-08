from django.urls import include, re_path

from slack_utils import views

urlpatterns = [
    re_path('events/$', views.EventsView.as_view(), name='slack-events-api'),
    re_path('commands/$', views.CommandView.as_view(), name='slack-commands'),
]
