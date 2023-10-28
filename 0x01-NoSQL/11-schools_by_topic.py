#!/usr/bin/env python3
"""Get a list of schools having a specific topic from a MongoDB collection"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic"""
    documents = mongo_collection.find({"topics": topic})
    return list(documents)
