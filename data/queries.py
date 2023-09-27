from pymongo import MongoClient
from bson.objectid import ObjectId

import datetime
import os
from dotenv import load_dotenv

load_dotenv()


# TODO: implement pagination
# TODO: create base class to implement CRUD methods so entities can inherit it
USERNAME = os.getenv('MONGODB_USER')
PASSWORD = os.getenv('MONGODB_PASSWORD')
MONGODB_CLIENT = MongoClient(
    f'mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.0cvleso.mongodb.net/'
)
MONGODB_DATABASE = MONGODB_CLIENT[os.getenv('MONGODB_DATABASE_NAME')]


def get_books(**kwargs):
    BOOKS = MONGODB_DATABASE.books
    aggregate_operations = [
        {
            '$lookup': {
                'from': 'authors',
                'localField': 'authors',
                'foreignField': '_id',
                'as': 'authors',
            }
        },
        {
            '$project': {
                '_id': {'$toString': '$_id'},
                'title': 1,
                'isbn': 1,
                'pageCount': 1,
                'thumbnailUrl': 1,
                'shortDescription': 1,
                'categories': 1,
                'createdOn': 1,
                'updatedOn': 1,
                'authors': {
                    '_id': 1,
                    'full_name': 1,
                },
            },
        },
        {'$sort': {'createdOn': -1}},
        {'$limit': kwargs.get('limit') or 400},
    ]

    try:
        if kwargs.get('book_id'):
            aggregate_operations.append({
                '$match': {'_id': kwargs.get('book_id')}
            })
            books = BOOKS.aggregate(aggregate_operations)
            return books.next()

        elif kwargs.get('search_param'):
            aggregate_operations.append({
                '$match': {
                    '$or': [
                        {'title': {
                            '$regex': kwargs.get('search_param'), '$options': 'i'
                        }},
                        {'isbn': {
                            '$regex': kwargs.get('search_param'), '$options': 'i'
                        }},
                    ]
                }
            })

        return list(BOOKS.aggregate(aggregate_operations))

    except Exception as ex:
        print(f'Fallo consultando libros. Error: {ex}')


def get_authors(**kwargs):
    AUTHORS = MONGODB_DATABASE.authors
    aggregate_operations = [
        {
            '$project': {
                '_id': {'$toString': '$_id'},
                'first_name': 1,
                'last_name': 1,
                'full_name': 1,
                'created_on': 1,
                'updated_on': 1,
            },
        },
        {'$sort': {'created_on': -1}},
        {'$limit': kwargs.get('limit') or 400},
    ]

    try:
        if kwargs.get('author_id'):
            aggregate_operations.append({
                '$match': {'_id': kwargs.get('author_id')}
            })
            authors = AUTHORS.aggregate(aggregate_operations)
            return authors.next()

        elif kwargs.get('search_param'):
            aggregate_operations.append({
                '$match': {
                    'full_name': {
                        '$regex': kwargs.get('search_param'), '$options': 'i'
                    }
                }
            })

        return list(AUTHORS.aggregate(aggregate_operations))

    except Exception as ex:
        print(f'Fallo consultando autores. Error: {ex}')


def add_book(book_vals):
    BOOKS = MONGODB_DATABASE.books

    try:
        if 'authors' in book_vals.keys() and book_vals['authors']:
            author_ids = [ObjectId(id) for id in book_vals['authors']]
            book_vals.update({
                'pageCount': 0,
                'authors': author_ids,
                'createdOn': datetime.datetime.now(),
                'updatedOn': datetime.datetime.now(),
            })

        return str(BOOKS.insert_one(book_vals).inserted_id)

    except Exception as ex:
        raise Exception(f'Fallo guardando libro. Error: {ex}')
        # MONGODB_CLIENT.close()


def add_author(author_vals):
    AUTHORS = MONGODB_DATABASE.authors

    try:
        full_name = f"{author_vals.get('first_name', '')} {author_vals.get('last_name', '')}"
        author_vals.update({
            'full_name': full_name,
            'created_on': datetime.datetime.now(),
            'updated_on': datetime.datetime.now(),
        })
        return str(AUTHORS.insert_one(author_vals).inserted_id)

    except Exception as ex:
        raise Exception(f'Fallo guardando autor. Error: {ex}')


def update_book(book_id, book_vals):
    BOOKS = MONGODB_DATABASE.books

    try:
        if 'authors' in book_vals.keys() and book_vals['authors']:
            author_ids = [ObjectId(id) for id in book_vals['authors']]
            book_vals.update({
                'authors': author_ids,
                'updatedOn': datetime.datetime.now(),
            })

        BOOKS.update_one(
            {'_id': ObjectId(book_id)},
            {'$set': book_vals},
        )

    except Exception as ex:
        raise Exception(f'Fallo modificando libro. Error: {ex}')


def update_author(author_id, author_vals):
    AUTHORS = MONGODB_DATABASE.authors

    try:
        author_vals.update({
            'updated_on': datetime.datetime.now(),
        })
        AUTHORS.update_one(
            {'_id': ObjectId(author_id)},
            {'$set': author_vals},
        )

    except Exception as ex:
        raise Exception(f'Fallo modificando autor. Error: {ex}')
