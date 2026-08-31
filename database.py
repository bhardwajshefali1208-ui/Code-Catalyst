import sqlite3
from datetime import datetime

DATABASE = "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            recipient TEXT,
            upi_id TEXT,
            amount REAL,
            risk_score INTEGER,
            risk_level TEXT,
            action TEXT,
            reasons TEXT,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_transaction(transaction, risk_result):

    connection = get_connection()
    cursor = connection.cursor()

    reasons = "||".join(risk_result["reasons"])

    cursor.execute("""
        INSERT INTO transactions
        (
            sender,
            recipient,
            upi_id,
            amount,
            risk_score,
            risk_level,
            action,
            reasons,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        transaction["sender"],
        transaction["recipient"],
        transaction["upi_id"],
        transaction["amount"],
        risk_result["score"],
        risk_result["level"],
        risk_result["action"],
        reasons,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_transactions():

    connection = get_connection()

    transactions = connection.execute("""
        SELECT *
        FROM transactions
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return transactions