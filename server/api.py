from models import User, Server, app
from flask import jsonify, request


@app.route('/users', methods = ['POST', 'GET'])
def users():
    if request.method == 'GET':
        return get_all_users()
    elif request.method == 'POST':
        return create_user(**request.form)