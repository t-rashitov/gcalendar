import random
import uuid

import pytest
from faker import Faker

from event.models import Event


faker = Faker()


@pytest.mark.parametrize('event_params', [
    {
        'event_id': str(uuid.uuid4()),
        'summary': faker.city(),
        'start': faker.date_time(tzinfo=faker.pytimezone()),
        'end': faker.date_time(tzinfo=faker.pytimezone()),
        'event_type': random.choice(('default', 'non-default')),
        'html_link': faker.uri()
    } for _ in range(10)
])
@pytest.mark.django_db
def test_remote_sync(event_params, create_user):

    Event.synchronize_with_remote([event_params], create_user())

    event = Event.objects.first()

    event_obj_params = {
        'event_id': event.event_id,
        'summary': event.summary,
        'start': event.start,
        'end': event.end,
        'event_type': event.event_type,
        'html_link': event.html_link
    }

    assert event_obj_params == event_params


