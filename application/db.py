import json


def read_data(file_name="db.json"):
    with open(file_name, "r") as db:
        return json.load(db)


def save_data(data, file_name="db.json"):
    with open(file_name, "w") as db:
        json.dump(data, db, indent=2)
        #readeable format me arrange karta hai.
