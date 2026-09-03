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


def get_transactions(search="", risk_level="", action=""):

    connection = get_connection()

    query = """
        SELECT *
        FROM transactions
        WHERE 1=1
    """

    parameters = []

    # Search recipient, sender or UPI ID
    if search:
        query += """
            AND (
                recipient LIKE ?
                OR sender LIKE ?
                OR upi_id LIKE ?
            )
        """

        search_value = f"%{search}%"

        parameters.extend([
            search_value,
            search_value,
            search_value
        ])

    # Risk filter
    if risk_level:
        query += " AND risk_level = ?"
        parameters.append(risk_level)

    # Action filter
    if action:
        query += " AND action = ?"
        parameters.append(action)

    query += """
        ORDER BY id DESC
    """

    transactions = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return transactions


def get_transaction(transaction_id):

    connection = get_connection()

    transaction = connection.execute(
        """
        SELECT *
        FROM transactions
        WHERE id = ?
        """,
        (transaction_id,)
    ).fetchone()

    connection.close()

    return transaction