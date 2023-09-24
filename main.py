from flask import Flask, request, jsonify
from data import queries

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def response_error(message):
    return jsonify({'error': message}), 500


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return '<h3>Books API</h3>'


@app.route('/books', methods=['GET'])
def get_books():
    try:
        books = []
        search = request.args.get('search_param', None)

        if search:
            books = queries.get_books(search_param=search)
        else:
            books = queries.get_books()

        return jsonify(books), 200

    except Exception as ex:
        return response_error(str(ex))


@app.route('/book/<string:id>', methods=['GET'])
def get_single_book(id):
    try:
        book = queries.get_books(book_id=id)
        return jsonify(book), 200
    except Exception as ex:
        return response_error(str(ex))


@app.route('/authors', methods=['GET'])
def get_authors():
    try:
        authors = []
        search = request.args.get('search_param', None)

        if search:
            authors = queries.get_authors(search_param=search)
        else:
            authors = queries.get_authors()

        return jsonify(authors), 200

    except Exception as ex:
        return response_error(str(ex))


@app.route('/author/<string:id>', methods=['GET'])
def get_single_author(id):
    try:
        author = queries.get_authors(author_id=id)
        return jsonify(author), 200
    except Exception as ex:
        return response_error(str(ex))


@app.route('/book', methods=['POST'])
def post_book():
    try:
        book_id = queries.add_book(request.json)
        return jsonify({
            '_id': book_id,
            'message': 'Book | POST request successful',
        }), 201
    except Exception as ex:
        return response_error(str(ex))


@app.route('/author', methods=['POST'])
def post_author():
    try:
        author_id = queries.add_author(request.json)
        return jsonify({
            '_id': author_id,
            'message': 'Author | POST request successful',
        }), 201
    except Exception as ex:
        return response_error(str(ex))


@app.route('/book/<string:id>', methods=['PUT'])
def put_book(id):
    try:
        queries.update_book(id, request.json)
        return jsonify({
            '_id': id,
            'message': 'Book | PUT request successful',
        }), 200
    except Exception as ex:
        return response_error(str(ex))


@app.route('/author/<string:id>', methods=['PUT'])
def put_author(id):
    try:
        queries.update_author(id, request.json)
        return jsonify({
            '_id': id,
            'message': 'Author | PUT request successful',
        }), 200
    except Exception as ex:
        return response_error(str(ex))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
