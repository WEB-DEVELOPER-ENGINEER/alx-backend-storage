#!/usr/bin/env python3
"""Change school topics"""


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name.
    Args:
        mongo_collection: The Pymongo collection object
        name (string): The school name to update
        topics (list of strings): The list of topics approached in the school
    """
    query = {"name": name}
    new_values = {"$set": {"topics": topics}}
    mongo_collection.update_many(query, new_values)
