

class EventError(Exception):
    pass


class LoadError(EventError):
    pass


class AuthError(EventError):
    pass
