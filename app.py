from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# 🔐 Google Apps Script Web App URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz6JHGuLX1r_BwBlxKlLt-ER-BUsjL915z1IeEh8UIoOP9lzG0khAGZsQOrZVRyG5hJLQ/exec"


@app.route('/')
def index():
    return render_template('index.html')


# ✅ Accept Invite (RSVP)
@app.route('/accept', methods=['POST'])
def accept():
    try:
        requests.post(SCRIPT_URL, json={
            "type": "accept"
        }, timeout=5)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ✅ Post Wish
@app.route('/post-wish', methods=['POST'])
def post_wish():
    data = request.get_json()
    name = data.get('guestName')
    message = data.get('guestMessage')

    if not name or not message:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    try:
        requests.post(SCRIPT_URL, json={
            "type": "wish",
            "name": name,
            "message": message
        }, timeout=5)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
