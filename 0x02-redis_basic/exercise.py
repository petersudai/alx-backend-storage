#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union


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
