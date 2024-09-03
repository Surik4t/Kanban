from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2, os
import uuid

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

load_dotenv()
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# connection to DB
def db_connection():
    try: 
        conn = psycopg2.connect(host='localhost',
                              dbname='testdb',
                              user=DB_USERNAME,
                              password=DB_PASSWORD
                              )
        print(conn)
        return conn
    except Exception as e:
        print(f'error connecting to database: {e}')
        return None

BOOKS = [
    {
      'id': uuid.uuid4().hex,
      'title': 'On the Road',
      'author': 'Jack Kerouac',
      'read': True
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
            'title': 'New column',
        }
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO columns(pos, uuid, title)
                    VALUES (%s, %s, %s);''', (new_column['pos'], new_column['id'], new_column['title'])
                    )
        conn.commit()
        cur.close()
        conn.close()
    else:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM columns ORDER BY pos ASC;')
        columns = cur.fetchall()
        cur.close()
        conn.close()

        keys = ['pos', 'id', 'title']
        COLUMNS = [dict(zip(keys, column)) for column in columns]
        for column in COLUMNS:
            column['cards'] = []
        response_object['columns'] = COLUMNS
    return jsonify(response_object)

@app.route('/kanban/columns/', methods=['DELETE', 'PUT'])
def single_column():
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        column_id = request.args.get('columnId')
        new_column_title = request.args.get('columnTitle')
        conn = db_connection()
        cur = conn.cursor()

        cur.execute('''UPDATE columns
                    SET title = %s
                    WHERE uuid = %s;''', (new_column_title, column_id))
        cur.close()
        conn.commit()
        conn.close()
        return jsonify(response_object)
            
    if request.method == 'DELETE':
        column_id = request.args.get('columnId')
        conn = db_connection()
        cur = conn.cursor()

        cur.execute('''SELECT pos FROM columns
                    WHERE uuid = %s;''', (column_id,))
        data = cur.fetchone()
        pos = int(data[0])
        cur.execute('''DELETE FROM cards
                    WHERE column_id = %s;''', (column_id,))
        cur.execute('''DELETE FROM columns
                    WHERE uuid = %s;''', (column_id,))
        cur.execute('''UPDATE columns
                    SET pos = pos - 1
                    WHERE pos > %s;''', (pos,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(response_object)

@app.route('/kanban/columns/swap/', methods=['PUT'])
def swap_columns():
    response_object = {'statis': 'success'}
    current_pos = int(request.args.get('pos'))
    direction = request.args.get('direction')
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''SELECT uuid, title FROM columns
                WHERE pos = %s;''', (current_pos,))
    data = cur.fetchone()
    temp = {'uuid': data[0], 'title': data[1]}
    if direction == 'left':
        cur.execute('''SELECT pos, uuid, title FROM columns
                    WHERE pos = %s - 1;''', (current_pos,))
    elif direction == 'right':
        cur.execute('''SELECT pos, uuid, title FROM columns
                    WHERE pos = %s + 1;''', (current_pos,))
    data = cur.fetchone()
    target = {'pos': data[0], 'uuid': data[1], 'title': data[2]}
    cur.execute('''UPDATE columns
                SET uuid = %s, title = %s
                WHERE pos = %s;
                ''', (temp['uuid'], temp['title'], target['pos'])
                )
    cur.execute('''UPDATE columns
                SET uuid = %s, title = %s
                WHERE pos = %s;
                ''', (target['uuid'], target['title'], current_pos)
                )
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(response_object)

# CARD METHODS
@app.route('/kanban/cards/', methods=['GET', 'POST', 'PUT'])
def all_cards():
    conn = db_connection()
    cur = conn.cursor()
    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        new_card = (
            uuid.uuid4().hex,
            post_data.get('columnId'),
            post_data.get('priority'),
            post_data.get('header'),
            post_data.get('text'),
        )
        cur.execute('''INSERT INTO cards(id, column_id, priority, header, text)
                    VALUES (%s, %s, %s, %s, %s);''', 
                    new_card
                    )
        conn.commit()

    elif request.method == 'PUT':
        new_card_data = request.json
        conn = db_connection()
        cur = conn.cursor()
        cur.execute('''UPDATE cards
                    SET priority = %s, header = %s, text = %s
                    WHERE id = %s;
                    ''',
                    (
                      new_card_data['priority'],
                      new_card_data['header'],
                      new_card_data['text'],
                      new_card_data['id']
                    )
                  )
        conn.commit()

    elif request.method == 'GET':
        cur.execute('''SELECT * FROM cards;''')
        cards = cur.fetchall()
        keys = ['id', 'column_id', 'priority', 'header', 'text']
        CARDS = [dict(zip(keys, card)) for card in cards]
        response_object['cards'] = CARDS
    cur.close()
    conn.close()
    return jsonify(response_object)

@app.route('/kanban/cards/<card_id>', methods=['DELETE'])
def single_card(card_id):
    response_object = {'status': 'success'}
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''DELETE FROM cards WHERE id = %s;''', (card_id,))
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(response_object)

# updating the entire board
@app.route('/kanban/updateBoard/', methods=['PUT'])
def updateBoard():
    response_object = {'status': 'success'}
    data = request.json
    new_card_order = []
    for column in data:
        column_id = column['id']
        for card in column['cards']:
            if card['column_id'] != column_id:
                card['column_Id'] = column_id
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
    