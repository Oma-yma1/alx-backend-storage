#!/usr/bin/env python3
""" 101-main """


def top_students(mongo_collection):
    """eturns all students sorted by average score"""
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
