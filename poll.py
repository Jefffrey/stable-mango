import socket
import datetime
import time
import sqlite3


POLLING_INTERVAL = 5  # seconds
SQLITE3_DB_FILENAME = "raw.db"
DB_TABLE_NAME = "ping_data"

PING_SERVER = "8.8.8.8"
PING_PORT = 53  # DNS port


def ping():
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((PING_SERVER, PING_PORT))
        return True
    except Exception:
        return False


def main():
    socket.setdefaulttimeout(3)
    sqlite_conn = sqlite3.connect(SQLITE3_DB_FILENAME)

    with sqlite_conn:
        sqlite_conn.execute("PRAGMA journal_mode=wal")
        table_sql = f"""
            CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_time TEXT,
                event_outcome TEXT,
                event_server TEXT
            );
            """
        sqlite_conn.execute(table_sql)

    while True:
        event_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        event_outcome = "SUCCESS" if ping() else "FAIL"
        event_server = f"{PING_SERVER}:{PING_PORT}"

        insert_args = (event_time, event_outcome, event_server)
        insert_sql = f"""
            INSERT INTO {DB_TABLE_NAME} (event_time, event_outcome, event_server)
            VALUES(?,?,?);
            """

        with sqlite_conn:
            sqlite_conn.execute(insert_sql, insert_args)

        print(f"Inserted: {event_time}, {event_outcome}, {event_server}")

        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    main()
