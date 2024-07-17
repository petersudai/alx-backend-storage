#!/usr/bin/env python3
"""
Web Cache and Access Tracker
"""
import redis
import requests
from typing import Callable
from functools import wraps


redis_client = redis.Redis()

def count_accesses(method: Callable) -> Callable:
    """
    Decorator to count accesses to a particular URL.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        redis_client.incr(f"count:{url}")
        return method(url)
    return wrapper

def cache_result(expiration: int = 10) -> Callable:
    """
    Decorator to cache the result of the URL fetch with expiration.
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            cached_result = redis_client.get(url)
            if cached_result:
                return cached_result.decode('utf-8')

            result = method(url)
            redis_client.setex(url, expiration, result)
            return result
        return wrapper
    return decorator

@count_accesses
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """
    Fetches HTML content of a URL and caches result
    """
    response = requests.get(url)
    return response.text
