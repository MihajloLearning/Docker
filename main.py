from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import add_user, get_all_users, get_user_by_id, delete_user
from logger import logger

app = Flask(__name__)

@app.route('/')
def hub():
    return render_template('hub.html')  # monitoring tools

@app.route('/dashboard')
def landing_page():
    logger.info("Dashboard landing page loaded")
    return render_template('landing.html')

@app.route('/dashboard/add', methods=['GET'])
def home():
    logger.info("Add user form loaded")
    return render_template('index.html')

@app.route('/dashboard/users', methods=['POST'])
def create_user():
    name = request.form.get("name") or request.json.get("name")
    if not name:
        logger.warning("Name field missing in request")
        return jsonify({"error": "Name is required"}), 400

    user_id = add_user(name)
    logger.info(f"User added: {name} (ID: {user_id})")
    return redirect(url_for('fetch_users'))

@app.route('/dashboard/users', methods=['GET'])
def fetch_users():
    users = get_all_users()
    return render_template('users.html', users=users)

@app.route('/dashboard/users/<user_id>', methods=['GET'])
def fetch_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/dashboard/users/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    success = delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"error": "User not found"}), 404

@app.errorhandler(404)
def not_found_error(error):
    logger.warning("404 Not Found")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Server Error: {error}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
