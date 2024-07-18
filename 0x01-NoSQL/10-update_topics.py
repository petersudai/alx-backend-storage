#!/usr/bin/env python3
"""
function that changes all topics of school docmnt based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on name
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
