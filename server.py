from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "leaderboard.json"
TOP_LIMIT = 10 # change to None if you want unlimited

# Create file if missing
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


@app.route("/add/<level>/<entry>")
def add(level, entry):
    data = load_data()

    if level not in data:
        data[level] = []

    try:
        username, time = entry.split(",")
        time = float(time)
    except:
        return "Format must be username,time"

    level_data = data[level]

    # Check if user already has a time
    found = False
    for player in level_data:
        if player["username"] == username:
            # Only update if faster
            if time < player["time"]:
                player["time"] = time
            found = True
            break

    if not found:
        level_data.append({"username": username, "time": time})

    # 🔥 SORT LOWEST TIME FIRST
    level_data.sort(key=lambda x: x["time"])

    # Optional top limit
    if TOP_LIMIT:
        level_data = level_data[:TOP_LIMIT]

    data[level] = level_data
    save_data(data)

    return "OK"


@app.route("/ret/<level>")
def ret(level):
    data = load_data()
    if level not in data:
        return jsonify([])
    return jsonify(data[level])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)