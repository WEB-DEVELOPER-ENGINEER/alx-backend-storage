#!/usr/bin/env python3
"""List all documents in Python"""


def list_all(mongo_collection):
    """a Python function that lists all documents in a collection
    Return an empty list if no document in the collection"""
    documents = mongo_collection.find()
    if documents.count() == 0:
        return []
    return documents
