import os
import time
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def init_db():
    # La BDD peut mettre quelques secondes à démarrer : on réessaie
    for _ in range(15):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS items ("
                "id SERIAL PRIMARY KEY, name TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT FALSE)"
            )
            cur.execute(
                "ALTER TABLE items ADD COLUMN IF NOT EXISTS done BOOLEAN NOT NULL DEFAULT FALSE"
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except psycopg2.OperationalError:
            print("DB pas prête, nouvel essai dans 2s...")
            time.sleep(2)
    raise RuntimeError("Impossible de se connecter à la BDD")


@app.route("/items", methods=["GET"])
def list_items():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, done FROM items ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "done": r[2]} for r in rows])


@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id", (data["name"],))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "name": data["name"]}), 201


@app.route("/items", methods=["DELETE"])
def delete_items():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM items")
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "All items deleted"}), 200


@app.route("/items/<int:item_id>/toggle", methods=["PUT"])
def toggle_item(item_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE items SET done = NOT done WHERE id = %s RETURNING done",
        (item_id,),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row is None:
        return jsonify({"error": "Item introuvable"}), 404
    return jsonify({"id": item_id, "done": row[0]}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
