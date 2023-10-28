#!/usr/bin/env python3
"""Insert a document in Python"""


def insert_school(mongo_collection, **kwargs):
    """a function to insert a new document in a collection based on kwargs"""
    return mongo_collection.insert(kwargs)
