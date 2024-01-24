#!/usr/bin/env python3
"""
This module contains a class that perform basic caching using the reddis libra
ry
"""
from functools import wraps
import redis
from uuid import uuid4
from typing import Callable
from typing import Optional
from typing import Union


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes a single method Callable argument and returns a
    Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapped function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    decorator to store the history of inputs and outputs for a particular
    function
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        input_name = method.__qualname__ + ":inputs"
        self._redis.rpush(input_name, str(args))

        output_name = method.__qualname__ + ":outputs"
        data = method(self, *args, **kwargs)
        self._redis.rpush(output_name, str(data))
        return data

    return wrapper


class Cache():
    """ Cache class """

    def __init__(self) -> None:
        """Initialize an instance of the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[int, str, bytes, float]) -> str:
        """
        A method that stores a data using the redis library

        Args:
            data: The data to be stored
        Return: The key(uuid) linked to the stored data
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[int, bytes, float, int]:
        """
        Retrieve data stored in redis database using
        """
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_int(self, key: str) -> int:
        """
        Use the get method to retrieve an integer variable
        """
        data = self.get(key).decode()
        try:
            value = int(data)
        except Exception as e:
            value = 0
        return value

    def get_str(self, key: str) -> str:
        """
        Use the get method to retrieve a string variable
        """
        data = self.get(key).decode()
        return data


def replay(method: Callable) -> None:
    """
    Function to display the history of calls of a particular function
    """
    qualname = method.__qualname__
    redis_inst = method.__self__._redis
    inputs = redis_inst.lrange("{}:inputs".format(qualname), 0, -1)
    outputs = redis_inst.lrange("{}:outputs".format(qualname), 0, -1)
    print("{} was called {} times:".format(qualname,
                                           method.__self__.get_int(qualname)))
    for k, v in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(qualname, k.decode(), v.decode()))
