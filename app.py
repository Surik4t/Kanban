from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from sqlalchemy.orm import Session
import sqlalchemy as db
import psycopg2, os
import uuid

DEBUG = True

load_dotenv()
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")

# instantiate the app
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
app.config.from_object(__name__)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=12)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# enable CORS
CORS(app, supports_credentials=True, origins=["http://localhost:8080"])


# connection to DB
path = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = db.create_engine(path)
conn = engine.connect()
metadata = db.MetaData()

columns = db.Table(
    "columns",
    metadata,
    db.Column("pos", db.Integer),
    db.Column("uuid", db.Uuid),
    db.Column("title", db.VARCHAR(30)),
    db.Column("board_id", db.Uuid),
)

cards = db.Table(
    "cards",
    metadata,
    db.Column("id", db.Uuid),
    db.Column("column_id", db.Uuid),
    db.Column("priority", db.VARCHAR),
    db.Column("header", db.VARCHAR),
    db.Column("text", db.VARCHAR),
    db.Column("index", db.Integer),
)


def db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"error connecting to database: {e}")
        return None


# authentication methods
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    token = None
    jti = jwt_payload["jti"]
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT * FROM expired_tokens
            WHERE jti = %s;""",
            (jti,),
        )
        token = cur.fetchone()
    except Exception as e:
        print(f"exception requesting expired tokens database: {e}")
    cur.close()
    conn.close()
    return token is not None


@app.route("/get_session", methods=["GET"])
@jwt_required()
def get_session():
    current_user = get_jwt_identity()
    return jsonify(
        {"message": f"logged in as '{current_user[0]}'", "user": current_user[0]}
    )


@app.route("/get_user_info/<user>", methods=["GET"])
def get_user_info(user):
    print(user)
    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """SELECT bio, mail, phone FROM users
                    WHERE username = %s""",
            (user,),
        )
        keys = ["bio", "mail", "phone"]
        data = dict(zip(keys, cur.fetchone()))
        cur.close()
        conn.close()
        return jsonify(
            {"bio": data["bio"], "mail": data["mail"], "phone": data["phone"]}
        )
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return jsonify({"error": f"database error: {e}"}), 500


@app.route("/upload_user_info", methods=["PUT"])
def upload_user_info():
    data = request.get_json()
    username = data["username"]
    bio = data["bio"]
    mail = data["mail"]
    phone = data["phone"]
    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """UPDATE users
                    SET bio = %s, mail = %s, phone = %s
                    WHERE username = %s""",
            (bio, mail, phone, username),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "user info updated"}), 200
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        return jsonify({"error": f"database error: {e}"}), 500


@app.route("/picture/<username>", methods=["PUT"])
def picture(username):
    path = f"./flask-vue/client/src/imgs/{username}.jpg"
    if os.path.exists(path):
        print("path exists")
        return jsonify({"message": "OK"}), 200
    else:
        print("path does not exist")
        return jsonify({"error": "Picture not found"}), 404


@app.route("/upload_picture/<username>", methods=["POST"])
def upload_picture(username):
    file = request.files["file"]
    binary_data = file.read()
    try:
        with open(f"./flask-vue/client/src/imgs/{username}.jpg", "wb") as image:
            image.write(binary_data)
    except Exception as e:
        return jsonify({"error": f"error uploading the image: {e}"}), 500
    return jsonify({"message": "Profile picture uploaded"})


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user = get_jwt_identity()
    access_token = create_access_token(identity=user)
    return jsonify(
        {
            "message": "access token refreshed",
            "access_token": access_token,
            "user": user[0],
        }
    )


@app.route("/login", methods=["PUT"])
def login():
    credentials = request.get_json("username")
    username = credentials["username"]
    password = credentials["password"]
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT username, password FROM users
                    WHERE username = %s;""",
            (username,),
        )
        user = cur.fetchone()
    except Exception as e:
        print(f"database exception: {e}")
        return jsonify({"error": f"exception raised: {e}"}), 500

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    password_is_valid = bcrypt.check_password_hash(user[1], password)
    if not password_is_valid:
        return jsonify({"error": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    cur.close()
    conn.close()
    return jsonify(
        {
            "message": "login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@app.route("/register", methods=["POST"])
def register():
    credentials = request.get_json("username")
    username = credentials["username"]
    password = credentials["password"]
    hash = bcrypt.generate_password_hash(password.encode("utf8"), 10)
    hash = hash.decode("utf-8")
    print(hash)
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT * FROM users WHERE username = %s;""", (username,))
        username_exists = cur.fetchall()
        print(type(username_exists))
        if username_exists:
            return jsonify({"error": "Username already exists."}), 409
        cur.execute(
            """INSERT INTO users(username, password)
                    values(%s, %s);""",
            (username, hash),
        )
        conn.commit()
    except Exception as e:
        print(f"exception creating user: {e}")
        return jsonify({"error": f"exception creating user: {e}"}), 500
    cur.close()
    conn.close()
    return jsonify({"message": "registration complete"}), 200


@app.route("/revoke_access_token", methods=["POST"])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()["jti"]
    print("jti:", jti)
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO expired_tokens(jti)
                    VALUES(%s);""",
            (jti,),
        )
        conn.commit()
        response = jsonify({"message": "logged out successfully"})
    except Exception as e:
        response = jsonify({"error": f"error logging out: {e}"})
    cur.close()
    conn.close()
    return response


@app.route("/revoke_refresh_token", methods=["POST"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()["jti"]
    print("jti:", jti)
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO expired_tokens(jti)
                    VALUES(%s);""",
            (jti,),
        )
        conn.commit()
        response = jsonify({"message": "logged out successfully"})
    except Exception as e:
        response = jsonify({"error": f"error logging out: {e}"})
    cur.close()
    conn.close()
    return response


BOARDS = [
    {
        "id": uuid.uuid4().hex,
        "title": "kanban test1",
        "description": "kanban description test",
        "user": "testuser",
    },
    {
        "id": uuid.uuid4().hex,
        "title": "2",
        "description": "2222",
        "user": "",
    },
]


# BOARDS
@app.route("/boards/get/<user>", methods=["GET"])
def get_boards(user):
    boards = [board for board in BOARDS if board["user"] == user]
    response = jsonify({"boards": boards})
    return response


@app.route("/boards/add", methods=["POST"])
def create_board():
    data = request.get_json()
    new_kanban = {
        "id": uuid.uuid4().hex,
        "title": data["title"],
        "description": data["description"],
        "user": data["user"],
    }
    BOARDS.append(new_kanban)
    init_columns(new_kanban["id"])
    return jsonify({"message": "kanban created"})


def init_columns(board_id):
    try:
        query = columns.insert().values(
            [
                {
                    "pos": 0,
                    "uuid": uuid.uuid4().hex,
                    "title": "To Do",
                    "board_id": board_id,
                },
                {
                    "pos": 1,
                    "uuid": uuid.uuid4().hex,
                    "title": "In Progress",
                    "board_id": board_id,
                },
                {
                    "pos": 2,
                    "uuid": uuid.uuid4().hex,
                    "title": "Done",
                    "board_id": board_id,
                },
            ]
        )
        conn.execute(query)
        conn.commit()
    except Exception as e:
        print(e)


@app.route("/boards/edit", methods=["PUT"])
def change_boards():
    data = request.get_json()
    for board in BOARDS:
        if board["id"] == data["id"]:
            board["title"] = data["title"]
            board["description"] = data["description"]
            return jsonify({"message": "changes saved"})
        else:
            return jsonify({"error": "board id not found"}, 404)


@app.route("/boards/delete/<id>", methods=["PUT"])
def delete(id):
    delete_board(id)
    with Session(engine) as session:
        query = db.select(columns.c.uuid).where(columns.c.board_id == id)
        selected_columns = conn.execute(query).fetchall()
        for column in selected_columns:
            session.execute(db.delete(cards).where(cards.c.column_id == column.uuid))
        session.execute(db.delete(columns).where(columns.c.board_id == id))
        # add to session: delete board
        session.commit()
    return jsonify({"message": "board removed"})


def delete_board(id):
    global BOARDS
    BOARDS = [board for board in BOARDS if board["id"] != id]
    return


# COLUMN METHODS
@app.route("/kanban/columns/<board_id>", methods=["GET", "POST"])
def all_columns(board_id):
    response_object = {"status": "success"}
    conn = db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        post_data = request.get_json()
        new_column = {
            "pos": post_data.get("pos"),
            "id": uuid.uuid4().hex,
            "title": "New column",
        }
        try:
            cur.execute(
                f"""INSERT INTO columns(pos, uuid, title)
                        VALUES (%s, %s, %s);""",
                (new_column["pos"], new_column["id"], new_column["title"]),
            )
            conn.commit()
        except Exception as e:
            print(f"error adding a column to database: {e}")

    elif request.method == "GET":
        try:
            cur.execute(
                "SELECT * FROM columns WHERE board_id = %s ORDER BY pos ASC;",
                (board_id,),
            )
            columns = cur.fetchall()
            keys = ["pos", "id", "title"]
            COLUMNS = [dict(zip(keys, column)) for column in columns]
            for column in COLUMNS:
                cur.execute(
                    """SELECT * FROM cards WHERE column_id = %s ORDER BY index ASC;""",
                    (column["id"],),
                )
                cards_data = cur.fetchall()
                keys = ["id", "column_id", "priority", "header", "text", "index"]
                column["cards"] = [dict(zip(keys, card)) for card in cards_data]
            response_object["columns"] = COLUMNS
        except Exception as e:
            print(f"error recieving data from database: {e}")
    cur.close()
    conn.close()
    return jsonify(response_object)


@app.route("/kanban/columns/", methods=["DELETE", "PUT"])
def single_column():
    response_object = {"status": "success"}
    conn = db_connection()
    cur = conn.cursor()

    if request.method == "PUT":
        column_id = request.args.get("columnId")
        new_column_title = request.args.get("columnTitle")
        try:
            cur.execute(
                """UPDATE columns
                        SET title = %s
                        WHERE uuid = %s;""",
                (new_column_title, column_id),
            )
            conn.commit()
        except Exception as e:
            print(f"errorr updating a column: {e}")

    if request.method == "DELETE":
        column_id = request.args.get("columnId")
        try:
            cur.execute(
                """SELECT pos FROM columns
                        WHERE uuid = %s;""",
                (column_id,),
            )
            data = cur.fetchone()
            pos = int(data[0])
            cur.execute(
                """DELETE FROM cards
                        WHERE column_id = %s;""",
                (column_id,),
            )
            cur.execute(
                """DELETE FROM columns
                        WHERE uuid = %s;""",
                (column_id,),
            )
            cur.execute(
                """UPDATE columns
                        SET pos = pos - 1
                        WHERE pos > %s;""",
                (pos,),
            )
            conn.commit()
        except Exception as e:
            print(f"error deleting a column from database: {e}")
    cur.close()
    conn.close()
    return jsonify(response_object)


@app.route("/kanban/columns/swap/", methods=["PUT"])
def swap_columns():
    response_object = {"statis": "success"}
    current_pos = int(request.args.get("pos"))
    direction = request.args.get("direction")
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT uuid, title FROM columns
                    WHERE pos = %s;""",
            (current_pos,),
        )
        data = cur.fetchone()
        temp = {"uuid": data[0], "title": data[1]}
        if direction == "left":
            cur.execute(
                """SELECT pos, uuid, title FROM columns
                        WHERE pos = %s - 1;""",
                (current_pos,),
            )
        elif direction == "right":
            cur.execute(
                """SELECT pos, uuid, title FROM columns
                        WHERE pos = %s + 1;""",
                (current_pos,),
            )
        data = cur.fetchone()
        target = {"pos": data[0], "uuid": data[1], "title": data[2]}
        cur.execute(
            """UPDATE columns
                    SET uuid = %s, title = %s
                    WHERE pos = %s;
                    """,
            (temp["uuid"], temp["title"], target["pos"]),
        )
        cur.execute(
            """UPDATE columns
                    SET uuid = %s, title = %s
                    WHERE pos = %s;
                    """,
            (target["uuid"], target["title"], current_pos),
        )
        conn.commit()
    except Exception as e:
        print(f"error swapping columns: {e}")
    cur.close()
    conn.close()
    return jsonify(response_object)


# CARD METHODS
@app.route("/kanban/cards/", methods=["POST", "PUT"])
def all_cards():
    response_object = {"status": "success"}
    conn = db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        post_data = request.get_json()
        new_card = (
            uuid.uuid4().hex,
            post_data.get("columnId"),
            post_data.get("priority"),
            post_data.get("header"),
            post_data.get("text"),
            post_data.get("index"),
        )
        try:
            cur.execute(
                """INSERT INTO cards(id, column_id, priority, header, text, index)
                        VALUES (%s, %s, %s, %s, %s, %s);""",
                new_card,
            )
            conn.commit()
        except Exception as e:
            print(f"error adding a card to database: {e}")

    elif request.method == "PUT":
        new_card_data = request.json
        try:
            cur.execute(
                """UPDATE cards
                        SET priority = %s, header = %s, text = %s
                        WHERE id = %s;
                        """,
                (
                    new_card_data["priority"],
                    new_card_data["header"],
                    new_card_data["text"],
                    new_card_data["id"],
                ),
            )
            conn.commit()
        except Exception as e:
            print(f"error updating a card: {e}")
    cur.close()
    conn.close()
    return jsonify(response_object)


@app.route("/kanban/cards/<card_id>", methods=["DELETE"])
def single_card(card_id):
    response_object = {"status": "success"}
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""DELETE FROM cards WHERE id = %s;""", (card_id,))
    except Exception as e:
        print(f"error deleting a card from database: {e}")
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(response_object)


# Updating kanban on card swap
@app.route("/kanban/updateBoard/", methods=["PUT"])
def updateBoard():
    response_object = {"status": "success"}
    conn = db_connection()
    cur = conn.cursor()
    data = request.json
    try:
        for column in data:
            for card in column["cards"]:
                cur.execute(
                    """UPDATE cards SET column_id = %s, index = %s
                            WHERE id = %s;
                            """,
                    (column["id"], column["cards"].index(card), card["id"]),
                )
    except Exception as e:
        print(f"error updating kanban: {e}")
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(response_object)


if __name__ == "__main__":
    app.run()
