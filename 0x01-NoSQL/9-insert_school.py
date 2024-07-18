#!/usr/bin/env python3
"""
Python function that inserts a new document in ollection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts new document in collection
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
