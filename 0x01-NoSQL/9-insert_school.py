#!/usr/bin/env python3
""" 9-main """


def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection based on kwargs"""
    document = mongo_collection.insert_one(kwargs)
    return document.inserted_id
