#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the count for the method call.

        Args:
            self: The instance of the class.
            *args: Positional arguments to the method.
            **kwargs: Keyword arguments to the method.

        Returns:
            The return value of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper Funtion"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result

    return wrapper
    

class Cache:
    """
    Cache class for storing and retrieving data in Redis.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client.
    """
    def __init__(self):
        """
        Initialize the Cache class.

        This method initializes Redis client instance & flushes the database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key and an optional callable to convert the data.

        Args:
            key (str): The key to retrieve the data from Redis.
            fn (Optional[Callable]): A callable to convert the data back to the desired format.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data
            converted using the callable if provided.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis using the provided key and convert it to a string.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            Optional[str]: The retrieved data as a string, or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis using the provided key and convert it to an integer.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            Optional[int]: The retrieved data as an integer, or None if the key does not exist.
        """
        return self.get(key, int)
