import random
import uuid

from faker import Faker
from googleapiclient.errors import HttpError

faker = Faker()


class MockSuccessfulEvents:

    def execute(self, *args, **kwargs):
        Faker.seed(0)
        return {
            'items': [
                {
                    'id': str(uuid.uuid4()),
                    'summary': faker.name(),
                    'start': random.choice(({'dateTime': faker.iso8601(tzinfo=faker.pytimezone())},
                                            {'date': faker.iso8601().split('T')[0]})),
                    'end': random.choice(({'dateTime': faker.iso8601(tzinfo=faker.pytimezone())},
                                          {'date': faker.iso8601().split('T')[0]})),
                    'eventType': random.choice(('default', 'non-default')),
                    'htmlLink': faker.uri(),
                } for _ in range(10)
            ]
        }


class MockSuccessfulResource:

    def list(self, *args, **kwargs):
        return MockSuccessfulEvents()


class MockSuccessfulService:

    def events(self):
        return MockSuccessfulResource()


class MockUnsuccessfulEvents:

    def execute(self, *args, **kwargs):
        raise HttpError(resp=type('Reason', (), {'reason': 'test', 'status': 503}), content=b'')


class MockUnsuccessfulResource:

    def list(self, *args, **kwargs):
        return MockUnsuccessfulEvents()


class MockUnsuccessfulService:

    def events(self):
        return MockUnsuccessfulResource()
