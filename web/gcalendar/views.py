import logging
from datetime import datetime

from django.shortcuts import redirect
from django.views.generic import TemplateView
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from requests import HTTPError
from social_django.utils import load_strategy

from event.models import Event


logger = logging.getLogger('django')


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.render_to_response({})

        social = request.user.social_auth.get(provider='google-oauth2')

        try:
            token = social.get_access_token(load_strategy())
            credentials = Credentials(token)

            service = build('calendar', 'v3', credentials=credentials)
            events_result = service.events().list(
                calendarId='primary', maxResults=1000, singleEvents=True, orderBy='startTime').execute()
        except (HTTPError, RefreshError) as e:
            logger.info(str(e))
            return redirect('logout')

        events = [{
                'event_id': event['id'],
                'summary': event.get('summary') or event.get('description', ''),
                'start': datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
                if event['start'].get('dateTime') else datetime.strptime(event['start']['date'] + 'Z', '%Y-%m-%d%z'),
                'end': datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
                if event['end'].get('dateTime') else datetime.strptime(event['end']['date'] + 'Z', '%Y-%m-%d%z'),
                'event_type': event.get('eventType', ''),
                'html_link': event.get('htmlLink', '')
            } for event in events_result.get('items', [])]

        Event.synchronize_with_remote(events, request.user)

        return self.render_to_response({'events': Event.objects.filter(author=request.user).order_by('-start')[:1000]})
