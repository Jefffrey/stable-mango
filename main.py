import sqlite3
from flask import Flask, jsonify, render_template

SQLITE3_DB_FILENAME = "raw.db"
DB_TABLE_NAME = "ping_data"

app = Flask(__name__)


@app.route("/_data", methods=["GET"])
def data():
    with sqlite3.connect(SQLITE3_DB_FILENAME) as sqlite_conn:
        limit = 10
        select_sql = f"""
            SELECT id, event_time, event_outcome, event_server
            from {DB_TABLE_NAME}
            ORDER BY id DESC
            LIMIT {limit}
        """
        rows = sqlite_conn.execute(select_sql).fetchall()
        out_rows = [
            {
                "id": r[0],
                "event_time": r[1],
                "event_outcome": r[2],
                "event_server": r[3],
            } for r in rows
        ]
        return jsonify(rows=out_rows)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
