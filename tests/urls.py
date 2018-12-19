from django.conf.urls import include, url

urlpatterns = [
    url('slack/', include('slack_utils.urls')),
]
