#!/usr/bin/env python3
"""A script that that returns all students sorted by average score"""
from collections import OrderedDict


def top_students(mongo_collection):
    """
    returns all students sorted by average score.
    The top must be ordered.
    The average score must be part of each item returns with key=averageScore
    """
    pipeline = [{'$addFields': {'averageScore': {'$avg': '$topics.score'}}},
                {'$project': {'_id': 0, 'name': 1, 'averageScore': 1}},
                {'$sort': {'averageScore': -1, 'name': 1}}]
    return mongo_collection.aggregate(pipeline)
