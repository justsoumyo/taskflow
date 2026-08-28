import os
import sqlite3
import hashlib
import datetime
from functools import wraps

import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS


# =========================
# APP
# =========================

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.environ.get(
    "TASKFLOW_SECRET",
    "taskflow_dev_secret_change_in_production"
)

DB_NAME = "taskflow.db"


# =========================
# DATABASE
# =========================

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT UNIQUE,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Support old database
    columns = [
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(users)"
        ).fetchall()
    ]

    if "full_name" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN full_name TEXT"
        )

    if "email" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN email TEXT"
        )

    if "created_at" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN created_at TEXT"
        )

    # BOARDS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS boards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # LISTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        board_id INTEGER NOT NULL,
        position INTEGER DEFAULT 0,
        FOREIGN KEY (board_id) REFERENCES boards(id)
    )
    """)

    # TASKS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        list_id INTEGER NOT NULL,
        position INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (list_id) REFERENCES lists(id)
    )
    """)

    conn.commit()
    conn.close()


# =========================
# PASSWORD
# =========================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================
# JWT AUTH
# =========================

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": (
            datetime.datetime.utcnow()
            + datetime.timedelta(days=7)
        )
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get(
            "Authorization"
        )

        if not auth_header:
            return jsonify({
                "error": "Token is missing"
            }), 401

        try:
            parts = auth_header.split(" ")

            if len(parts) != 2:
                raise ValueError(
                    "Invalid token format"
                )

            token = parts[1]

            data = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            current_user_id = data["user_id"]

        except Exception:
            return jsonify({
                "error": "Invalid or expired token"
            }), 401

        return f(
            current_user_id,
            *args,
            **kwargs
        )

    return decorated


# =========================
# HEALTH
# =========================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "TaskFlow API is running"
    })


# =========================
# REGISTER
# =========================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    full_name = data.get(
        "full_name",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    username = data.get(
        "username",
        ""
    ).strip()

    password = data.get(
        "password",
        ""
    )

    if not full_name:
        return jsonify({
            "error": "Full name is required"
        }), 400

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    if "@" not in email:
        return jsonify({
            "error": "Please enter a valid email address"
        }), 400

    if len(username) < 3:
        return jsonify({
            "error": "Username must be at least 3 characters"
        }), 400

    if len(password) < 4:
        return jsonify({
            "error": "Password must be at least 4 characters"
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                username,
                password
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                full_name,
                email,
                username,
                hash_password(password)
            )
        )

        conn.commit()

        return jsonify({
            "message": "Registration successful",
            "username": username
        }), 201

    except sqlite3.IntegrityError as error:

        error_message = str(error)

        if "email" in error_message.lower():
            return jsonify({
                "error": "Email already exists"
            }), 409

        return jsonify({
            "error": "Username already exists"
        }), 409

    finally:
        conn.close()


# =========================
# LOGIN
# =========================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    username = data.get(
        "username",
        ""
    ).strip()

    password = data.get(
        "password",
        ""
    )

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    conn = get_db()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    conn.close()

    if not user:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    if user["password"] != hash_password(password):
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    token = create_token(
        user["id"]
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "username": user["username"],
        "full_name": user["full_name"]
    })


# =========================
# GET BOARDS
# =========================

@app.route("/api/boards", methods=["GET"])
@token_required
def get_boards(current_user_id):

    conn = get_db()

    boards = conn.execute(
        """
        SELECT id, name, created_at
        FROM boards
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (current_user_id,)
    ).fetchall()

    conn.close()

    return jsonify([
        dict(board)
        for board in boards
    ])


# =========================
# CREATE BOARD
# =========================

@app.route("/api/boards", methods=["POST"])
@token_required
def create_board(current_user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    name = data.get(
        "name",
        ""
    ).strip()

    if not name:
        return jsonify({
            "error": "Board name is required"
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO boards
        (name, user_id)
        VALUES (?, ?)
        """,
        (
            name,
            current_user_id
        )
    )

    board_id = cursor.lastrowid

    default_lists = [
        ("To Do", 0),
        ("In Progress", 1),
        ("Done", 2)
    ]

    for list_name, position in default_lists:

        cursor.execute(
            """
            INSERT INTO lists
            (
                name,
                board_id,
                position
            )
            VALUES (?, ?, ?)
            """,
            (
                list_name,
                board_id,
                position
            )
        )

    conn.commit()
    conn.close()

    return jsonify({
        "id": board_id,
        "name": name
    }), 201


# =========================
# GET SINGLE BOARD
# =========================

@app.route(
    "/api/boards/<int:board_id>",
    methods=["GET"]
)
@token_required
def get_board(
    current_user_id,
    board_id
):

    conn = get_db()

    board = conn.execute(
        """
        SELECT *
        FROM boards
        WHERE id = ?
        AND user_id = ?
        """,
        (
            board_id,
            current_user_id
        )
    ).fetchone()

    if not board:
        conn.close()

        return jsonify({
            "error": "Board not found"
        }), 404

    lists = conn.execute(
        """
        SELECT *
        FROM lists
        WHERE board_id = ?
        ORDER BY position
        """,
        (board_id,)
    ).fetchall()

    result_lists = []

    for lst in lists:

        tasks = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE list_id = ?
            ORDER BY position
            """,
            (lst["id"],)
        ).fetchall()

        result_lists.append({
            "id": lst["id"],
            "name": lst["name"],
            "position": lst["position"],
            "tasks": [
                dict(task)
                for task in tasks
            ]
        })

    conn.close()

    return jsonify({
        "id": board["id"],
        "name": board["name"],
        "lists": result_lists
    })


# =========================
# DELETE BOARD
# =========================

@app.route(
    "/api/boards/<int:board_id>",
    methods=["DELETE"]
)
@token_required
def delete_board(
    current_user_id,
    board_id
):

    conn = get_db()

    board = conn.execute(
        """
        SELECT id
        FROM boards
        WHERE id = ?
        AND user_id = ?
        """,
        (
            board_id,
            current_user_id
        )
    ).fetchone()

    if not board:
        conn.close()

        return jsonify({
            "error": "Board not found"
        }), 404

    list_ids = conn.execute(
        """
        SELECT id
        FROM lists
        WHERE board_id = ?
        """,
        (board_id,)
    ).fetchall()

    for lst in list_ids:
        conn.execute(
            """
            DELETE FROM tasks
            WHERE list_id = ?
            """,
            (lst["id"],)
        )

    conn.execute(
        """
        DELETE FROM lists
        WHERE board_id = ?
        """,
        (board_id,)
    )

    conn.execute(
        """
        DELETE FROM boards
        WHERE id = ?
        """,
        (board_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Board deleted"
    })


# =========================
# CREATE LIST
# =========================

@app.route(
    "/api/lists",
    methods=["POST"]
)
@token_required
def create_list(current_user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    board_id = data.get(
        "board_id"
    )

    name = data.get(
        "name",
        ""
    ).strip()

    if not board_id or not name:
        return jsonify({
            "error": "Board ID and list name are required"
        }), 400

    conn = get_db()

    board = conn.execute(
        """
        SELECT id
        FROM boards
        WHERE id = ?
        AND user_id = ?
        """,
        (
            board_id,
            current_user_id
        )
    ).fetchone()

    if not board:
        conn.close()

        return jsonify({
            "error": "Board not found"
        }), 404

    position = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM lists
        WHERE board_id = ?
        """,
        (board_id,)
    ).fetchone()["count"]

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO lists
        (
            name,
            board_id,
            position
        )
        VALUES (?, ?, ?)
        """,
        (
            name,
            board_id,
            position
        )
    )

    conn.commit()

    list_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "id": list_id,
        "name": name
    }), 201


# =========================
# UPDATE LIST
# =========================

@app.route(
    "/api/lists/<int:list_id>",
    methods=["PUT"]
)
@token_required
def update_list(
    current_user_id,
    list_id
):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    conn = get_db()

    lst = conn.execute(
        """
        SELECT lists.*
        FROM lists
        JOIN boards
        ON lists.board_id = boards.id
        WHERE lists.id = ?
        AND boards.user_id = ?
        """,
        (
            list_id,
            current_user_id
        )
    ).fetchone()

    if not lst:
        conn.close()

        return jsonify({
            "error": "List not found"
        }), 404

    name = data.get(
        "name",
        lst["name"]
    ).strip()

    position = data.get(
        "position",
        lst["position"]
    )

    if not name:
        conn.close()

        return jsonify({
            "error": "List name is required"
        }), 400

    conn.execute(
        """
        UPDATE lists
        SET name = ?,
            position = ?
        WHERE id = ?
        """,
        (
            name,
            position,
            list_id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "List updated"
    })


# =========================
# DELETE LIST
# =========================

@app.route(
    "/api/lists/<int:list_id>",
    methods=["DELETE"]
)
@token_required
def delete_list(
    current_user_id,
    list_id
):

    conn = get_db()

    lst = conn.execute(
        """
        SELECT lists.*
        FROM lists
        JOIN boards
        ON lists.board_id = boards.id
        WHERE lists.id = ?
        AND boards.user_id = ?
        """,
        (
            list_id,
            current_user_id
        )
    ).fetchone()

    if not lst:
        conn.close()

        return jsonify({
            "error": "List not found"
        }), 404

    conn.execute(
        """
        DELETE FROM tasks
        WHERE list_id = ?
        """,
        (list_id,)
    )

    conn.execute(
        """
        DELETE FROM lists
        WHERE id = ?
        """,
        (list_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "List deleted"
    })


# =========================
# CREATE TASK
# =========================

@app.route(
    "/api/tasks",
    methods=["POST"]
)
@token_required
def create_task(current_user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    list_id = data.get(
        "list_id"
    )

    title = data.get(
        "title",
        ""
    ).strip()

    description = data.get(
        "description",
        ""
    ).strip()

    if not list_id or not title:
        return jsonify({
            "error": "List ID and task title are required"
        }), 400

    conn = get_db()

    lst = conn.execute(
        """
        SELECT lists.*
        FROM lists
        JOIN boards
        ON lists.board_id = boards.id
        WHERE lists.id = ?
        AND boards.user_id = ?
        """,
        (
            list_id,
            current_user_id
        )
    ).fetchone()

    if not lst:
        conn.close()

        return jsonify({
            "error": "List not found"
        }), 404

    position = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tasks
        WHERE list_id = ?
        """,
        (list_id,)
    ).fetchone()["count"]

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks
        (
            title,
            description,
            list_id,
            position
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            title,
            description,
            list_id,
            position
        )
    )

    conn.commit()

    task_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "id": task_id,
        "title": title,
        "description": description,
        "list_id": list_id
    }), 201


# =========================
# UPDATE / MOVE TASK
# =========================

@app.route(
    "/api/tasks/<int:task_id>",
    methods=["PUT"]
)
@token_required
def update_task(
    current_user_id,
    task_id
):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    conn = get_db()

    task = conn.execute(
        """
        SELECT tasks.*
        FROM tasks
        JOIN lists
        ON tasks.list_id = lists.id
        JOIN boards
        ON lists.board_id = boards.id
        WHERE tasks.id = ?
        AND boards.user_id = ?
        """,
        (
            task_id,
            current_user_id
        )
    ).fetchone()

    if not task:
        conn.close()

        return jsonify({
            "error": "Task not found"
        }), 404

    title = data.get(
        "title",
        task["title"]
    ).strip()

    description = data.get(
        "description",
        task["description"]
    ).strip()

    list_id = data.get(
        "list_id",
        task["list_id"]
    )

    position = data.get(
        "position",
        task["position"]
    )

    if not title:
        conn.close()

        return jsonify({
            "error": "Task title is required"
        }), 400

    new_list = conn.execute(
        """
        SELECT lists.*
        FROM lists
        JOIN boards
        ON lists.board_id = boards.id
        WHERE lists.id = ?
        AND boards.user_id = ?
        """,
        (
            list_id,
            current_user_id
        )
    ).fetchone()

    if not new_list:
        conn.close()

        return jsonify({
            "error": "Target list not found"
        }), 404

    conn.execute(
        """
        UPDATE tasks
        SET
            title = ?,
            description = ?,
            list_id = ?,
            position = ?
        WHERE id = ?
        """,
        (
            title,
            description,
            list_id,
            position,
            task_id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task updated"
    })


# =========================
# DELETE TASK
# =========================

@app.route(
    "/api/tasks/<int:task_id>",
    methods=["DELETE"]
)
@token_required
def delete_task(
    current_user_id,
    task_id
):

    conn = get_db()

    task = conn.execute(
        """
        SELECT tasks.*
        FROM tasks
        JOIN lists
        ON tasks.list_id = lists.id
        JOIN boards
        ON lists.board_id = boards.id
        WHERE tasks.id = ?
        AND boards.user_id = ?
        """,
        (
            task_id,
            current_user_id
        )
    ).fetchone()

    if not task:
        conn.close()

        return jsonify({
            "error": "Task not found"
        }), 404

    conn.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task deleted"
    })


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )