#!/usr/bin/env python3
""" 10-main """


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
