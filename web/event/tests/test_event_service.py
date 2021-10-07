from typing import Callable

import pytest

from event.exceptions import AuthError, LoadError
from event.services import GoogleEventsService


def test_events_parsing(successful_event_service: GoogleEventsService):
    events = successful_event_service.get_events()

    assert len(events) == 10


def test_events_attribute(successful_event_service: GoogleEventsService):
    events = successful_event_service.get_events()

    assert set(events[0].keys()) == {'event_id', 'summary', 'start', 'end', 'event_type', 'html_link'}


def test_mock_user_auth_error(successful_event_service: GoogleEventsService, create_user: Callable):
    with pytest.raises(AuthError):
        successful_event_service._get_token(create_user())


def test_mock_service_load_error(unsuccessful_event_service: GoogleEventsService):
    with pytest.raises(LoadError):
        unsuccessful_event_service.get_events()
