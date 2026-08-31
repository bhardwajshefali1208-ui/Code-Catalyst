def calculate_risk(transaction):
    score = 0
    reasons = []

    amount = transaction["amount"]
    average_amount = transaction["average_amount"]

    # 1. Amount anomaly
    if amount >= average_amount * 3:
        score += 30
        reasons.append(
            f"Transaction amount is {amount / average_amount:.1f}× your usual amount"
        )
    elif amount >= average_amount * 2:
        score += 15
        reasons.append(
            f"Transaction amount is {amount / average_amount:.1f}× your usual amount"
        )

    # 2. New recipient
    if transaction["new_recipient"]:
        score += 20
        reasons.append("This is a new recipient")

    # 3. New recipient + large amount
    if transaction["new_recipient"] and amount > 5000:
        score += 15
        reasons.append("Large transfer to a new recipient")

    # 4. Recipient history
    if transaction["suspicious_recipient"]:
        score += 25
        reasons.append("Recipient has suspicious transaction history")

    # 5. Device
    if transaction["unknown_device"]:
        score += 20
        reasons.append("Transaction is coming from an unrecognized device")

    # 6. Location
    if transaction["unusual_location"]:
        score += 15
        reasons.append("Transaction location is unusual for this user")

    # Keep score within 100
    score = min(score, 100)

    # Determine risk level/action
    if score <= 30:
        level = "LOW"
        action = "APPROVED"
    elif score <= 60:
        level = "MEDIUM"
        action = "CONFIRMATION REQUIRED"
    else:
        level = "HIGH"
        action = "TRANSACTION BLOCKED"

    return {
        "score": score,
        "level": level,
        "action": action,
        "reasons": reasons
    }