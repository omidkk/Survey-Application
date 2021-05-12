from application import application
from flask import jsonify


@application.route('/')
def index():
    return jsonify({'message': 'Hello'})