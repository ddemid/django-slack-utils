import django.dispatch

event_received = django.dispatch.Signal(providing_args=["event_type", "event_data"])