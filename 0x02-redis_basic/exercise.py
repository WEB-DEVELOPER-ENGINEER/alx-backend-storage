#!/usr/bin/env python3

from typing import Callable, Optional, Union
from uuid import uuid4
import redis
from functools import wraps

'''
    Writing strings to Redis.
'''


def count_calls(method: Callable) -> Callable:
    '''
        Counts the number of times a method is called.
    '''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
            Wrapper function.
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and
    outputs for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):  # sourcery skip: avoid-builtin-shadow
        """ Wrapper for decorator functionality """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def replay(fn: Callable) -> None:
    """
        display the history of calls of a particular function
    """
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    '''
        Cache class
    '''
    def __init__(self):
        '''
            Initialize the cache classs
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
            takes a data argument and returns a string
        '''
        randomKey = str(uuid4())
        self._redis.set(randomKey, data)
        return randomKey

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''
            takes a key string and an optional Callable fn
        '''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''
            parametrize Cache.get with the correct conversion function
        '''
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        '''
            parametrize Cache.get with the correct conversion function
        '''
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
