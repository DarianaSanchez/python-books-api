from pymongo import MongoClient

import sys
import json
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('MONGODB_USER')
PASSWORD = os.getenv('MONGODB_PASSWORD')
MONGODB_CLIENT = MongoClient(
    f'mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.0cvleso.mongodb.net/?authSource=admin'
)
MONGODB_DATABASE = MONGODB_CLIENT[os.getenv('MONGODB_DATABASE_NAME')]
BOOK_SCHEMA = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['title'],
        'properties': {
            'title': {'bsonType': 'string'},
            'isbn': {'bsonType': 'string'},
            'pageCount': {'bsonType': 'number'},
            'thumbnailUrl': {'bsonType': 'string'},
            'shortDescription': {'bsonType': 'string'},
            'authors': {
                'bsonType': 'array',
                'items': {'bsonType': 'objectId'}
            },
            'categories':  {
                'bsonType': 'array',
                'items': {'bsonType': 'string'}
            },
        }
    }
}
AUTHOR_SCHEMA = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['first_name'],
        'properties': {
            'first_name': {'bsonType': 'string'},
            'last_name': {'bsonType': 'string'},
            'full_name': {'bsonType': 'string'},
        },
    }
}


def setup_database():
    try:
        collections = MONGODB_DATABASE.list_collection_names()

        if 'books' not in collections:
            MONGODB_DATABASE.create_collection('books')
        if 'authors' not in collections:
            MONGODB_DATABASE.create_collection('authors')

        MONGODB_DATABASE.command('collMod', 'books', validator=BOOK_SCHEMA)
        MONGODB_DATABASE.command('collMod', 'authors', validator=AUTHOR_SCHEMA)

    except Exception as ex:
        print(f'No fue posible la estructura de la base de datos. Error: {ex}')


def insertAuthor(author_names):
    records = []
    author_ids = []

    for name in author_names:
        author = MONGODB_DATABASE.authors.find_one({'full_name': name})

        if author:
            author_ids.append(author['_id'])
        else:
            name_parts = name.split()
            name_half = len(name_parts) // 2
            records.append({
                'first_name': ' '.join(name_parts[:name_half]),
                'last_name': ' '.join(name_parts[name_half:]),
                'full_name': name,
            })

    if len(records):
        new_authors_ids = MONGODB_DATABASE.authors.insert_many(
            records).inserted_ids
        return author_ids + new_authors_ids

    return author_ids


def populate_database():
    records = []

    try:
        with open(r'books.json') as file_content:
            records = json.load(file_content)

            for record in records:
                record.update({'authors': insertAuthor(record.get('authors'))})

        result = MONGODB_DATABASE.books.insert_many(records)

        if not result.inserted_ids:
            raise Exception('Error: Poblamiento de base de datos fallido')

    except Exception as ex:
        print(f'No fue posible poblar la base de datos. Error: {ex}')
    finally:
        MONGODB_CLIENT.close()


def main():
    setup_database()
    populate_database()


if __name__ == '__main__':
    sys.exit(main())
