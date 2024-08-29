from flask import Flask, jsonify, request
from flask_cors import CORS
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

COLUMNS = [
    {
        'pos': 0,
        'id': uuid.uuid4().hex,
        'title': 'To do',
        'cards': []
    },
    {
        'pos': 1,
        'id': uuid.uuid4().hex,
        'title': 'In progress',
        'cards': []
    },
    {
        'pos': 2,
        'id': uuid.uuid4().hex,
        'title': 'Done',
        'cards': []
    }
]

CARDS = []

# COLUMN METHODS
@app.route('/kanban/columns', methods=['GET', 'POST'])
def all_columns():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_column = {
            'pos': post_data.get('pos'),
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
        }
        app.logger.info(f'column ID: {new_column['id']}')
        COLUMNS.append(new_column)
    else:
        response_object['columns'] = COLUMNS
    return jsonify(response_object)

@app.route('/kanban/columns/', methods=['DELETE', 'PUT'])
def single_column():
    response_object = {'status': 'success'}
    global COLUMNS
    if request.method == 'PUT':
        column_id = request.args.get('columnId')
        new_column_title = request.args.get('columnTitle')
        for column in COLUMNS:
            if column['id'] == column_id:
                column['title'] = new_column_title
                return jsonify(response_object)
    if request.method == 'DELETE':
        column_id = request.args.get('columnId')
        empty_colomn(column_id)
        for column in COLUMNS:
            if column['id'] == column_id:
                deleted_position = column['pos']
                COLUMNS.remove(column)
                break
        for column in COLUMNS:
            if column['pos'] > deleted_position:
                column['pos'] -= 1
        return jsonify(response_object)

@app.route('/kanban/columns/swap/', methods=['PUT'])
def swap_columns():
    response_object = {'statis': 'success'}
    pos = int(request.args.get('pos'))
    direction = request.args.get('direction')
    if direction == 'left':
        COLUMNS[pos], COLUMNS[pos-1] = COLUMNS[pos-1], COLUMNS[pos]
        COLUMNS[pos]['pos'], COLUMNS[pos-1]['pos'] = COLUMNS[pos-1]['pos'], COLUMNS[pos]['pos']
    elif direction == 'right':
        COLUMNS[pos], COLUMNS[pos+1] = COLUMNS[pos+1], COLUMNS[pos]
        COLUMNS[pos]['pos'], COLUMNS[pos+1]['pos'] = COLUMNS[pos+1]['pos'], COLUMNS[pos]['pos']
    return jsonify(response_object)

# CARD METHODS
@app.route('/kanban/cards', methods=['GET', 'POST'])
def all_cards():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_card = {
            'id': uuid.uuid4().hex,
            'columnId': post_data.get('columnId'),
            'status': post_data.get('status'),
            'header': post_data.get('header'),
            'text': post_data.get('text'),
        }
        app.logger.info(f'card ID: {new_card['id']}')
        CARDS.append(new_card)
    else:
        response_object['cards'] = CARDS
    return jsonify(response_object)

@app.route('/kanban/cards/<card_id>', methods=['DELETE', 'PUT'])
def single_card(card_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        return
    if request.method == 'DELETE':
        for card in CARDS:
            if card_id == card['id']:
                CARDS.remove(card)
        return jsonify(response_object)
        
def empty_colomn(column_id):
    global CARDS
    CARDS = [card for card in CARDS if card['columnId'] != column_id]

# updating the entire board
@app.route('/kanban/updateBoard/', methods=['PUT'])
def updateBoard():
    response_object = {'status': 'success'}
    data = request.json
    new_card_order = []
    for column in data:
        column_id = column['id']
        for card in column['cards']:
            if card['columnId'] != column_id:
                card['columnId'] = column_id
            new_card_order.append(card)
    global CARDS
    CARDS = new_card_order
    return jsonify(response_object)

# BOOK METHODS 
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