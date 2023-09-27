import pytest
import requests

import os
from dotenv import load_dotenv

load_dotenv()


API_URL = os.getenv('API_BASE_URL')

BOOK_JSON_FIELDS = ['_id', 'title', 'isbn', 'authors']
AUTHOR_JSON_FIELDS = ['_id', 'full_name']

GET_SINGLE_BOOK_ID = '650e44a0105c181438237704'
GET_SINGLE_AUTHOR_ID = '650e44a0105c1814382376fb'

BOOK_SEARCH_PARAM = 'android'
AUTHOR_SEARCH_PARAM = 'ableson'

POST_BOOKS_PARAMS = [
    ({
        'title': 'La isla bajo el mar',
        'isbn': '9788467861389',
        'authors': ['650f185e0f18bfbaf05d92f6']
    }),
    ({
        'title': 'La casa de los espiritus',
        'isbn': '9780060951306',
        'authors': ['650f185e0f18bfbaf05d92f6']
    })
]
POST_AUTHORS_PARAMS = [
    ({
        'first_name': 'Sylvia',
        'last_name': 'Plath',
    }),
    ({
        'first_name': 'Paulo',
        'last_name': 'Coelho',
    }),
]

PUT_BOOKS_PARAMS = [
    ('650f8e0e14e3e8f9249f13d7', {'title': 'La casa de los espiritus'}),
]
PUT_AUTHORS_PARAMS = [
    ('650f874a46718410c7687245', {'last_name': 'De Dumas'}),
    (
        '650e44a0105c1814382376fb',
        {'first_name': 'W. Frank', 'last_name': 'W. Frank'}
    ),
]


def check_json_structure(fields, obj):
    return not any([val not in obj for val in fields])


def check_object_vals(original, result):
    def compare(x, y):
        return (x == y or (type(x) == list and type(x) == type(y)))

    return all([compare(original[key], result.get(key)) for key in original.keys()])


def test_get_books():
    res = requests.get(f'{API_URL}/books')
    data = res.json()
    assert res.status_code == 200
    assert len(data) > 0 and check_json_structure(BOOK_JSON_FIELDS, data[0])


def test_search_books():
    res = requests.get(
        f'{API_URL}/books?search_param={BOOK_SEARCH_PARAM}'
    )
    data = res.json()
    assert res.status_code == 200
    assert len(data) > 0 and check_json_structure(BOOK_JSON_FIELDS, data[0])


def test_get_single_book():
    res = requests.get(f'{API_URL}/book/{GET_SINGLE_BOOK_ID}')
    assert res.status_code == 200
    assert check_json_structure(BOOK_JSON_FIELDS, res.json())


def test_get_authors():
    res = requests.get(f'{API_URL}/authors')
    data = res.json()
    assert res.status_code == 200
    assert len(data) > 0 and check_json_structure(AUTHOR_JSON_FIELDS, data[0])


def test_search_authors():
    res = requests.get(
        f'{API_URL}/authors?search_param={AUTHOR_SEARCH_PARAM}'
    )
    data = res.json()
    assert res.status_code == 200
    assert len(data) > 0 and check_json_structure(AUTHOR_JSON_FIELDS, data[0])


def test_get_single_author():
    res = requests.get(f'{API_URL}/author/{GET_SINGLE_AUTHOR_ID}')
    assert res.status_code == 200
    assert check_json_structure(AUTHOR_JSON_FIELDS, res.json())


@pytest.mark.parametrize('payload', POST_BOOKS_PARAMS)
def test_post_book(payload):
    res_post = requests.post(f'{API_URL}/book', json=payload)
    assert res_post.status_code == 201

    res_get = requests.get(f"{API_URL}/book/{res_post.json()['_id']}")
    assert res_get.status_code == 200
    assert check_object_vals(payload, res_get.json())


@pytest.mark.parametrize('payload', POST_AUTHORS_PARAMS)
def test_post_author(payload):
    res_post = requests.post(f'{API_URL}/author', json=payload)
    assert res_post.status_code == 201

    res_get = requests.get(f"{API_URL}/author/{res_post.json()['_id']}")
    assert res_get.status_code == 200
    assert check_object_vals(payload, res_get.json())


@pytest.mark.parametrize('id,payload', PUT_BOOKS_PARAMS)
def test_put_book(id, payload):
    res_put = requests.put(f'{API_URL}/book/{id}', json=payload)
    assert res_put.status_code == 200

    res_get = requests.get(f'{API_URL}/book/{id}')
    assert res_get.status_code == 200
    assert check_object_vals(payload, res_get.json())


@pytest.mark.parametrize('id,payload', PUT_AUTHORS_PARAMS)
def test_put_author(id, payload):
    res_put = requests.put(f'{API_URL}/author/{id}', json=payload)
    assert res_put.status_code == 200

    res_get = requests.get(f'{API_URL}/author/{id}')
    assert res_get.status_code == 200
    assert check_object_vals(payload, res_get.json())
