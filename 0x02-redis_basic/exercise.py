#!/usr/bin/env python3
""" exercise python """
import uuid
from functools import wraps
from typing import Callable, Optional, Union
import redis


def call_history(method: Callable) -> Callable:
    """method to record its input output history"""

    @wraps(method)
    def wrapr(self, *args, **kwargs):
        """function wrapper"""
        methode_name = method.__qualname__
        self._redis.rpush(methode_name + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(methode_name + ":outputs", output)
        return output

    return wrapr


def replay(method: Callable) -> None:
    """function replay"""
    methode_name = method.__qualname__
    redis_dab = method.__self__._redis
    inputs = redis_dab.lrange(methode_name + ":inputs", 0, -1)
    outputs = redis_dab.lrange(methode_name + ":outputs", 0, -1)

    print(f"{methode_name} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        input = input.decode("utf-8")
        output = output.decode("utf-8")
        print(f"{methode_name}(*{input}) -> {output}")


def count_calls(method: Callable) -> Callable:
    """function count """

    @wraps(method)
    def wrapr(self, *args, **kwargs):
        """funtion wrapper"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapr


class Cache:
    """class cache"""

    def __init__(self) -> None:
        """function init"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """function store"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None,
    ) -> Union[str, bytes, int, float, None]:
        """function get"""
        value = self._redis.get(key)
        if value is not None and fn is not None:
            value = fn(value)
        return value

    def get_int(self, key: str) -> Union[int, None]:
        """function get int"""
        return self.get(key, int)

    def get_str(self, key: str) -> Union[str, None]:
        """function get str"""
        return self.get(key, str)
