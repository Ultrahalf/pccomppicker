#!/usr/bin/env python

import sys
import json
import time
from bson.objectid import ObjectId

from pymongo import MongoClient

mc = MongoClient('localhost', 27017)
db = mc['pccomppicker']
products = db['products']
saved_builds = db['saved_builds']


class JSONEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)


def get_products(category: str, direction: int, featdict: dict, vendors: list):
    '''direction 1 = low to high, direction -1 = high to low'''

    if vendors == []:
        vendors = get_category_key_vals('cpu', 'vendor')

    if category == 'cpu':
        if 'brand' not in featdict or len(featdict['brand']) < 1:
            featdict['brand'] = get_category_key_vals('cpu', 'brand')
        if 'series' not in featdict or len(featdict['series']) < 1:
            featdict['series'] = get_category_key_vals('cpu', 'series')
        objects = products.find({
            'category': category, 'brand': {'$in': featdict['brand']},
            'series': {'$in': featdict['series']}, 'vendor': {'$in': vendors}
        }).sort("price", direction)

    elif category == 'gpu':
        if 'brand' not in featdict or len(featdict['brand']) < 1:
            featdict['brand'] = get_category_key_vals('gpu', 'brand')
        if 'series' not in featdict or len(featdict['series']) < 1:
            featdict['series'] = get_category_key_vals('gpu', 'series')
        objects = products.find({
            'category': category, 'brand': {'$in': featdict['brand']},
            'series': {'$in': featdict['series']}, 'vendor': {'$in': vendors}
        }).sort("price", direction)

    elif category == 'memory':
        if 'brand' not in featdict or len(featdict['brand']) < 1:
            featdict['brand'] = get_category_key_vals('memory', 'brand')
        if 'speed' not in featdict or len(featdict['speed']) < 1:
            featdict['speed'] = get_category_key_vals('memory', 'speed')
        if 'type' not in featdict or len(featdict['type']) < 1:
            featdict['type'] = get_category_key_vals('memory', 'type')
        if 'capacity' not in featdict or len(featdict['capacity']) < 1:
            featdict['capacity'] = get_category_key_vals('memory', 'capacity')
        if 'sub category' not in featdict or len(featdict['sub category']) < 1:
            featdict['sub category'] = get_category_key_vals('memory', 'sub category')
        objects = products.find({
            'category': category, 'brand': {'$in': featdict['brand']},
            'speed': {'$in': featdict['speed']},
            'type': {'$in': featdict['type']}, 'capacity': {'$in': featdict['capacity']},
            'vendor': {'$in': vendors}
        }).sort("price", direction)

    elif category == 'monitor':
        if 'brand' not in featdict or len(featdict['brand']) < 1:
            featdict['brand'] = get_category_key_vals('monitor', 'brand')
        if 'panel' not in featdict or len(featdict['panel']) < 1:
            featdict['panel'] = get_category_key_vals('monitor', 'panel')
        objects = products.find({
            'category': category, 'brand': {'$in': featdict['brand']},
            'panel': {'$in': featdict['panel']}, 'vendor': {'$in': vendors}
        }).sort("price", direction)

    elif category == 'storage':
        if 'brand' not in featdict or len(featdict['brand']) < 1:
            featdict['brand'] = get_category_key_vals('storage', 'brand')
        if 'type' not in featdict or len(featdict['type']) < 1:
            featdict['type'] = get_category_key_vals('storage', 'type')
        if 'capacity' not in featdict or len(featdict['capacity']) < 1:
            featdict['capacity'] = get_category_key_vals('storage', 'capacity')
        objects = products.find({
            'category': category, 'brand': {'$in': featdict['brand']},
            'type': {'$in': featdict['type']}, 'capacity': {'$in': featdict['capacity']},
            'vendor': {'$in': vendors}
        }).sort("price", direction)

    else:
        if 'brand' not in featdict or len(featdict['brand']) < 1:
            featdict['brand'] = get_category_key_vals(category, 'brand')
        objects = products.find({
            'category': category, 'brand': {'$in': featdict['brand']}, 'vendor': {'$in': vendors}
        }).sort("price", direction)

    list_of_dicts = list()
    for obj in objects:
        list_of_dicts.append(obj)

    return list_of_dicts


def get_product_from_id(product_id: str):
    product = products.find_one({'_id': ObjectId(product_id)})
    if product == None:
        print("dbops.get_product_from_id: No such product id!")
        sys.exit(1)
    return product


def id_exists(product_id: str):
    product = products.find_one({'_id': ObjectId(product_id)})
    return not product == None


def save_build(build_name: str, build_url: str, products: dict):
    build_genesis_time = int(time.time())
    
    # build is purged 90 days after creation
    build_purge_time = build_genesis_time + 90 * 24 * 60 * 60

    field = {
        'build_name': build_name,
        'build_url': build_url,
        'build_genesis_time': build_genesis_time,
        'build_purge_time': build_purge_time,
        'products': products,
    }

    saved_builds.insert_one(field)


def build_url_exists(build_url: str):
    build = saved_builds.find_one({'build_url': build_url})
    return not build == None


def get_build_from_build_url(build_url: str):
    build = saved_builds.find_one({'build_url': build_url})
    if not build:
        # something gone wrong
        sys.exit(1)
    return build


def get_category_key_vals(category: str, key: str):
    return list(products.distinct(key, {"category": category}))


def search(search_str: str):
    products.create_index([('title', 'text')])
    objects = products.find( { "$text": {"$search": search_str} } )

    list_of_dicts = list()
    for obj in objects:
        list_of_dicts.append(obj)

    return list_of_dicts


if __name__ == '__main__':
    print(get_products('cpu', -1, {'brand': ['amd'], 'series': ['ryzen5']}))
    print(get_category_key_vals('cpu', 'vendor'))
