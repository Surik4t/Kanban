from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import uuid

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

BOOKS = [
    {
      'id': uuid.uuid4().hex,
      'title': 'On the Road',
      'author': 'Jack Kerouac',
      'read': True
	  }
]

CARDS = [
    {
        'id': uuid.uuid4().hex,
        'status': 'To Do',
        'text': 'to do card'
    },
    {
        'id': uuid.uuid4().hex,
        'status': 'In Progress',
        'text': 'in progress card'
    },
    {
        'id': uuid.uuid4().hex,
        'status': 'Done',
        'text': 'done card'
    }
]

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/kanban', methods=['GET', 'POST'])
def all_cards():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_card = {
            'id': uuid.uuid4().hex,
            'status': post_data.get('status'),
            'text': post_data.get('text'),
        }
        app.logger.info(f'card ID: {new_card['id']}')
        CARDS.append(new_card)
        print(CARDS)
    else:
        response_object['cards'] = CARDS
    return jsonify(response_object)

@app.route('/kanban/<card_id>', methods=['DELETE', 'PUT'])
def single_card(card_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        return
    if request.method == 'DELETE':
        for card in CARDS:
            if card_id == card['id']:
                CARDS.remove(card)
        return jsonify(response_object)
        

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'

    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
        
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            BOOKS.remove(book)
    return
    

if __name__ == '__main__':
    app.run()