import flask
from flask import jsonify, request
from flask import make_response

from data import db_session
from data.rights import Rights
from main2 import app

blueprint = flask.Blueprint(
    'right_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/rights')
def get_rights():
    db_sess = db_session.create_session()
    right = db_sess.query(Rights).all()
    return jsonify(
        {
            'rights':
                [item.to_dict(only='name')
                 for item in right]
        }
    )


@blueprint.route('/api/rights/<int:right_id>', methods=['GET'])
def get_right(right_id):
    db_sess = db_session.create_session()
    right = db_sess.query(Rights).get(right_id)
    if not right:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'right': right.to_dict(only=(
                'name'))
        }
    )


@blueprint.route('/api/rights/', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    right = Rights(
        name=request.json['name'],
    )
    db_sess.add(right)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
