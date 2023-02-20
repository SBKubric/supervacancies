from contextvars import ContextVar

LOCAL_USER = ContextVar("local_user", default=None)


def set_local_user(user):
    LOCAL_USER.set(user)


def get_local_user():
    return LOCAL_USER.get()


def reset_local_user():
    LOCAL_USER.set(None)
