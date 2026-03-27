import json
from models.debt import Debt

def load_debts(path="data/debts.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return [
        Debt(
            d["name"],
            d["balance"],
            d["interest_rate"],
            d["min_payment"]
        )
        for d in data
    ]

def save_debts(debts, path="data/debts.json"):
    data = [
        {
            "name": d.name,
            "balance": d.balance,
            "interest_rate": d.interest_rate,
            "min_payment": d.min_payment
        }
        for d in debts
    ]
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
