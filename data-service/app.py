from flask import Flask, jsonify, request
import json
from pathlib import Path

app = Flask(__name__)

# Load users data
USERS_FILE = Path(__file__).parent / "users.json"


def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    """Return users, optionally filtered by labels.
    POST body: {"labels": ["ES", "male"]}
    """
    labels = []
    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        labels = body.get('labels', [])

    users = load_users()
    if labels:
        users = [u for u in users if all(lbl in u.get('labels', []) for lbl in labels)]
    return jsonify(users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
