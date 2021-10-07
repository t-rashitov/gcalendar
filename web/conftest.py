import uuid

import pytest

from event.tests.mocks import MockSuccessfulService, MockUnsuccessfulService
from event.services import GoogleEventsService


@pytest.fixture
def test_password():
    return 'test-password123'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def successful_event_service(create_user):
    return GoogleEventsService(service=MockSuccessfulService(), user=create_user())


@pytest.fixture
def unsuccessful_event_service(create_user):
    return GoogleEventsService(service=MockUnsuccessfulService(), user=create_user())
