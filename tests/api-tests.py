import pytest
import requests

import os
from dotenv import load_dotenv

load_dotenv()


API_URL = os.getenv('API_URL')
POST_BOOKS_PARAMS = [
    ({
        'title': 'La isla bajo el mar',
        'isbn': '9788467861389',
        'authors': 'Isabel Allende'
    }),
    ({
        'title': 'La casa de los espiritus',
        'isbn': '9780060951306',
        'authors': 'Isabel Allende'
    })
]
POST_AUTHORS_PARAMS = [
    ({
        'first_name': 'Isabel',
        'last_name': 'Allende',
    }),
    ({
        'first_name': 'Paulo',
        'last_name': 'Coelho',
    }),
]
PUT_BOOKS_PARAMS = [
    (10, {'title': 'El conde de Montecristo'}),
    (10, {'isbn': '9788574922225'}),
]
PUT_AUTHORS_PARAMS = [
    (3, {'first_name': 'Alejandro', 'last_name': 'Dumas'}),
    (5, {'last_name': 'Rowling'}),
]


def check_json_structure(obj):
    json_vals = ['id', 'title', 'isbn', 'authors']
    return not any([val not in obj for val in json_vals])


def check_object_vals(original, result):
    return all([original[key] == result[key] for key in original.keys()])


def test_get_books():
    res = requests.get(f'{API_URL}/posts/')
    data = res.json()
    assert res.status_code == 200
    assert len(data) > 0 and check_json_structure(data[0])


def test_get_single_book():
    res = requests.get(f'{API_URL}/posts/{1}')
    assert res.status_code == 200
    assert check_json_structure(res.json())


def test_get_authors():
    res = requests.get(f'{API_URL}/authors/')
    data = res.json()
    assert res.status_code == 200
    assert len(data) > 0 and check_json_structure(data[0])


def test_get_single_author():
    res = requests.get(f'{API_URL}/author/{1}')
    assert res.status_code == 200
    assert check_json_structure(res.json())


@pytest.mark.parametrize("payload", POST_BOOKS_PARAMS)
def test_post_book(payload):
    res = requests.post(f'{API_URL}/posts/', json=payload)
    data = res.json()
    assert res.status_code == 201
    assert check_json_structure(data)
    assert (data['title'] == payload['title']
            and data['isbn'] == payload['isbn'])


@pytest.mark.parametrize("payload", POST_AUTHORS_PARAMS)
def test_post_author(payload):
    res = requests.post(f'{API_URL}/author/', json=payload)
    data = res.json()
    assert res.status_code == 201
    assert check_json_structure(data)
    assert (data['first_name'] == payload['first_name']
            and data['last_name'] == payload['last_name'])


@pytest.mark.parametrize("id,payload", PUT_BOOKS_PARAMS)
def test_put_book(id, payload):
    res_put = requests.put(f'{API_URL}/book/{id}', json=payload)
    assert res_put.status_code == 200

    res_get = requests.get(f'{API_URL}/book/{id}')
    assert res_get.status_code == 200
    assert check_object_vals(payload, res_get.json())


@pytest.mark.parametrize("id,payload", PUT_AUTHORS_PARAMS)
def test_put_author(id, payload):
    res_put = requests.put(f'{API_URL}/book/{id}', json=payload)
    assert res_put.status_code == 200

    res_get = requests.get(f'{API_URL}/book/{id}')
    assert res_get.status_code == 200
    assert check_object_vals(payload, res_get.json())
