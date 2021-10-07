import logging
from datetime import datetime

from django.contrib.auth.models import User
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from social_django.models import UserSocialAuth
from social_django.utils import load_strategy

from event.exceptions import LoadError, AuthError
from event.models import Event


logger = logging.getLogger(__name__)


class GoogleEventsService:

    def __init__(self, service, user):
        self.service = service
        self.user = user

    @classmethod
    def get_service(cls, user: User):
        """
        Возвращает авторизованный объект сервиса
        """

        credentials = Credentials(cls._get_token(user))

        try:
            service = build('calendar', 'v3', credentials=credentials)
        except HttpError as e:
            msg = str(e)
            logger.debug(msg)
            raise AuthError(msg)

        return cls(service=service, user=user)

    @staticmethod
    def _get_token(user: User) -> str:

        try:
            social = user.social_auth.get(provider='google-oauth2')
            token = social.get_access_token(load_strategy())

        except (UserSocialAuth.DoesNotExist, RefreshError) as e:
            msg = str(e)
            logger.debug(msg)
            raise AuthError(msg)

        return token

    def _load_events(self, calendar_id='primary', max_results=1000):
        """
        :param calendar_id: ID календаря в Google Calendar
        :param max_results: количество загружаемых событий

        Возвращает список загруженных данных по событиям в указанном календаре
        """
        return self.service.events().list(
            calendarId=calendar_id, maxResults=max_results, singleEvents=True, orderBy='startTime').execute()

    def _get_parsed_events(self, items: list) -> list:
        """
        Парсинг данных событий
        """

        return [{
            'event_id': event['id'],
            'summary': event.get('summary') or event.get('description', ''),
            'start': datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            if event['start'].get('dateTime') else datetime.strptime(event['start']['date'] + 'Z', '%Y-%m-%d%z'),
            'end': datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            if event['end'].get('dateTime') else datetime.strptime(event['end']['date'] + 'Z', '%Y-%m-%d%z'),
            'event_type': event.get('eventType', ''),
            'html_link': event.get('htmlLink', '')
        } for event in items]

    def get_events(self) -> list:
        """
        Возвращает список событий
        """

        try:
            raw_events = self._load_events()
        except HttpError as e:
            msg = str(e)
            logger.debug(msg)
            raise LoadError(msg)

        return self._get_parsed_events(raw_events.get('items', []))

    def synchronize_with_remote(self) -> None:
        """
        Синхронизация БД с событиями из календаря
        """

        Event.synchronize_with_remote(events=self.get_events(), user=self.user)


