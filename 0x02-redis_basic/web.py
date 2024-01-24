#!/usr/bin/env python3
"""implementing an expiring web cache and tracker"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""module redis instance"""


def data_cacher(method: Callable) -> Callable:
    """function cahcer data"""
    @wraps(method)
    def wrapper(url) -> str:
        """function wrapper"""
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """function return url"""
    return requests.get(url).text
