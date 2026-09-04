from flask import Flask, render_template, request
from fraud_engine import calculate_risk

from database import (
    initialize_database,
    save_transaction,
    get_transactions,
    get_transaction
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

            "amount": float(
                request.form["amount"]
            ),

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


    # Calculate fraud risk
    risk_result = calculate_risk(transaction)


    # Save transaction
    save_transaction(
        transaction,
        risk_result
    )


    return render_template(
        "result.html",
        transaction=transaction,
        result=risk_result
    )


@app.route("/dashboard")
def dashboard():

    # Get filter values from URL
    search = request.args.get(
        "search",
        ""
    ).strip()

    risk_filter = request.args.get(
        "risk",
        ""
    ).strip()

    action_filter = request.args.get(
        "action",
        ""
    ).strip()


    # Get filtered transactions
    transactions = get_transactions(
        search=search,
        risk_level=risk_filter,
        action=action_filter
    )


    # Get ALL transactions for statistics
    all_transactions = get_transactions()


    total = len(all_transactions)


    high_risk = sum(
        1
        for t in all_transactions
        if t["risk_level"] == "HIGH"
    )


    medium_risk = sum(
        1
        for t in all_transactions
        if t["risk_level"] == "MEDIUM"
    )


    low_risk = sum(
        1
        for t in all_transactions
        if t["risk_level"] == "LOW"
    )


    blocked = sum(
        1
        for t in all_transactions
        if t["action"] == "TRANSACTION BLOCKED"
    )


    # Calculate percentages
    if total > 0:

        high_percentage = round(
            (high_risk / total) * 100,
            1
        )

        medium_percentage = round(
            (medium_risk / total) * 100,
            1
        )

        low_percentage = round(
            (low_risk / total) * 100,
            1
        )

        blocked_percentage = round(
            (blocked / total) * 100,
            1
        )

    else:

        high_percentage = 0
        medium_percentage = 0
        low_percentage = 0
        blocked_percentage = 0


    return render_template(

        "dashboard.html",

        transactions=transactions,

        total=total,

        high_risk=high_risk,

        medium_risk=medium_risk,

        low_risk=low_risk,

        blocked=blocked,

        high_percentage=high_percentage,

        medium_percentage=medium_percentage,

        low_percentage=low_percentage,

        blocked_percentage=blocked_percentage,

        search=search,

        risk_filter=risk_filter,

        action_filter=action_filter
    )


@app.route("/transaction/<int:transaction_id>")
def transaction_details(transaction_id):

    transaction = get_transaction(
        transaction_id
    )


    if transaction is None:

        return "Transaction not found", 404


    # Convert stored reasons back into a list
    reasons = []

    if transaction["reasons"]:

        reasons = transaction["reasons"].split("||")


    return render_template(

        "transaction_details.html",

        transaction=transaction,

        reasons=reasons
    )


if __name__ == "__main__":

    app.run(debug=True)