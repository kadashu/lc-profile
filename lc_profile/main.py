from functools import partial
from os import environ
from time import time

from leancloud import init
from numpy import isnan, nan
from pandas import DataFrame
from requests import Timeout

from .conversation import Conversation


OUTPUT = '''
Count: %d
Timeout: %d
Min: %.3f
Avg: %.3f
Max: %.3f
Std: %.3f
'''.strip()


def create_new_convs(n, unique=True):
    for i in range(n):
        start = time()
        try:
            Conversation.create('conv-%s' % time(), unique=unique)  # 时间戳递增，因此每个会话名称都不重复
            yield time() - start
        except Timeout:
            yield nan


create_new_convs_not_unique = partial(create_new_convs, unique=False)
create_new_convs_not_unique.__name__ = 'create_new_convs_not_unique'


def create_existing_convs(n, unique=True):
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


create_existing_convs_not_unique = partial(create_existing_convs, unique=False)
create_existing_convs_not_unique.__name__ = 'create_existing_convs_not_unique'


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

    n = int(environ.get('NUMBER', 10))
    repeat = int(environ.get('REPEAT', 5))

    profile(create_new_convs_not_unique, n, repeat)
    profile(create_new_convs, n, repeat)
    profile(create_existing_convs_not_unique, n, repeat)
    profile(create_existing_convs, n, repeat)


if __name__ == "__main__":
    main()
