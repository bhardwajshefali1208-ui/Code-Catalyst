**Code-Catalyst — BuildBank**

A web-based financial fraud detection system that analyzes transactions and identifies potentially suspicious activity using risk-based scoring.

**Features**

- Transaction fraud analysis
- Risk score calculation
- LOW / MEDIUM / HIGH risk classification
- Transaction blocking based on risk
- Search transactions by sender, recipient, or UPI ID
- Filter transactions by risk and action
- Risk percentage dashboard
- Detailed transaction view
- SQLite transaction history

**Tech Stack**

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite

**Project Structure**

Code-Catalyst/
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│   └── transaction_details.html
├── app.py
├── database.py
├── fraud_engine.py
├── requirements.txt
└── README.md
