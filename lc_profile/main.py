from functools import partial
from os import environ
from time import time
import sys

from leancloud import init
from numpy import isnan, nan
from pandas import DataFrame
from requests import Timeout

from .conversation import Conversation
from .message import send_message


OUTPUT = '''
Count: %d
Timeout: %d
Min: %.3f
Avg: %.3f
Max: %.3f
Std: %.3f
'''.strip()


def profile_create_new_convs(n, unique=True):
    for i in range(n):
        start = time()
        try:
            Conversation.create('conv-%s' % time(), unique=unique)  # 时间戳递增，因此每个会话名称都不重复
            yield time() - start
        except Timeout:
            yield nan


profile_create_new_convs_not_unique = partial(profile_create_new_convs, unique=False)
profile_create_new_convs_not_unique.__name__ = 'profile_create_new_convs_not_unique'


def profile_create_existing_convs(n, unique=True):
    names = {}

    for i in range(n):
        try:
            name = 'fixed-conv-%d' % i
            Conversation.create(name, unique=unique)
            names[i] = name
        except Timeout:
            pass

    for i in range(n):
        start = time()

        try:
            Conversation.create(names[i], unique=unique)
            yield time() - start
        except (KeyError, Timeout):
            yield nan


profile_create_existing_convs_not_unique = partial(profile_create_existing_convs, unique=False)
profile_create_existing_convs_not_unique.__name__ = 'profile_create_existing_convs_not_unique'


def profile_update_convs(n):
    convs = {}

    for i in range(n):
        try:
            conv = Conversation.create('conv-for-test-%d' % i, members=[])
            convs[i] = conv
        except Timeout:
            pass

    # not dict iter because we need to check for absent values (Timeout)
    for i in range(n):
        start = time()

        try:
            conv = convs[i]
            conv.ensure_members(['somebody'])
            yield time() - start
        except (KeyError, Timeout):
            yield nan


def profile_send_messages(n, recipients=None):
    conv = Conversation.create('conv-for-msg-test', members=recipients or [])

    for i in range(n):
        start = time()

        try:
            send_message(conv.id, 'lc-profiler', { 'content': time() })
            yield time() - start
        except Timeout:
            yield nan


profile_send_messages_with_members = partial(profile_send_messages, recipients=['lc-profiler-listener'])
profile_send_messages_with_members.__name__ = 'profile_send_messages_with_members'


def profile(func, n=10, repeat=5):
    timing = []
    n_timeout = 0

    for _ in range(repeat):
        for t in func(n):
            timing.append(t)
            if isnan(t):
                n_timeout += 1

    df = DataFrame(timing)
    print('Test: %s' % func.__name__)
    print(OUTPUT % (df.count()[0], n_timeout, df.min()[0], df.mean()[0], df.max()[0], df.std()[0]))
    print('')


def main():
    init(environ.get('LC_APP_ID'), master_key=environ.get('LC_MASTER_KEY'))

    func_name = environ.get('FUNC')
    func = globals().get('profile_%s' % func_name)
    n = int(environ.get('NUMBER', 10))
    repeat = int(environ.get('REPEAT', 5))

    if not func:
        print('Available Tests:')
        print('\n'.join(
            name[len('profile_'):]
            for name in globals().keys()
            if name.startswith('profile_')
        ))
        sys.exit(1)

    profile(func, n, repeat)


if __name__ == "__main__":
    main()
