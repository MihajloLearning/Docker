from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import add_user, get_all_users
from logger import logger

app = Flask(__name__)

@app.route('/')
def hub():
    return render_template('hub.html')

@app.route('/app', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get("name") or request.json.get("name")
    if not name:
        logger.warning("Name field missing in request")
        return jsonify({"error": "Name is required"}), 400

    user_id = add_user(name)
    logger.info(f"User added via form: {name}")
    return redirect(url_for('fetch_users'))

@app.route('/users', methods=['GET'])
def fetch_users():
    users = get_all_users()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
