from flask import Flask, render_template, request
from fraud_engine import calculate_risk
from database import (
    initialize_database,
    save_transaction,
    get_transactions
)

app = Flask(__name__)

# Create database when application starts
initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check_transaction():

    try:

        transaction = {
            "sender": request.form["sender"],
            "recipient": request.form["recipient"],
            "upi_id": request.form["upi_id"],

            "amount": float(request.form["amount"]),

            "average_amount": float(
                request.form["average_amount"]
            ),

            "new_recipient": (
                request.form.get("new_recipient") == "yes"
            ),

            "suspicious_recipient": (
                request.form.get("suspicious_recipient") == "yes"
            ),

            "unknown_device": (
                request.form.get("unknown_device") == "yes"
            ),

            "unusual_location": (
                request.form.get("unusual_location") == "yes"
            )
        }

    except (ValueError, KeyError):

        return "Invalid transaction data", 400

    risk_result = calculate_risk(transaction)

    save_transaction(transaction, risk_result)

    return render_template(
        "result.html",
        transaction=transaction,
        result=risk_result
    )


@app.route("/dashboard")
def dashboard():

    transactions = get_transactions()

    total = len(transactions)

    high_risk = sum(
        1 for t in transactions
        if t["risk_level"] == "HIGH"
    )

    medium_risk = sum(
        1 for t in transactions
        if t["risk_level"] == "MEDIUM"
    )

    low_risk = sum(
        1 for t in transactions
        if t["risk_level"] == "LOW"
    )

    blocked = sum(
        1 for t in transactions
        if t["action"] == "TRANSACTION BLOCKED"
    )

    return render_template(
        "dashboard.html",
        transactions=transactions,
        total=total,
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
        blocked=blocked
    )


if __name__ == "__main__":
    app.run(debug=True)