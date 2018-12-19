from django.urls import path

from slack_utils import views

urlpatterns = [
    path('events/', views.EventsView.as_view(), name='slack-events-api'),
]
