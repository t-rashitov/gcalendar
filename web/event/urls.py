from django.contrib.auth.decorators import login_required
from django.urls import path

from event.views import EventListView

app_name = 'event'


urlpatterns = [
    path('', login_required(EventListView.as_view()), name='event-list')
]
