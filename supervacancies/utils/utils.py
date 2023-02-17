from contextvars import ContextVar

def set_local_user(user):
    context = ContextVar('local_user', default=None)
    context.set(user)


def get_local_user():
    context = ContextVar('local_user', default=None)
    return context.get()



