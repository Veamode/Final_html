import json

import flask
from flask import jsonify, request
from flask import make_response
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User
from main2 import app

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [(item.name, item.email)
                 for item in user]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': (user.id, user.email)
        }
    )


@blueprint.route('/api/users/', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'email', 'right_id', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User(
        name=request.json['name'],
        email=request.json['email'],
        right_id=request.json['right_id'],
        hashed_password=generate_password_hash(request.json['password'])
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
