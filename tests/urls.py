from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('slack/', include('slack_utils.urls')),
]
