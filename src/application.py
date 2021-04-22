"""
Simple password generator API built with Flask framework.
Uses "secrets" library for generating cryptographically strong passwords or tokens.
"""
from flask import Flask, request, render_template, jsonify, make_response
from src.password_generator import Password

import sys

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    Returns project main page
    """
    return render_template('index.html')


@app.route('/generate', methods=['GET'])
def generate():
    """
    Generates password with given parameters, then returns password as JSON-response
    """
    # Loading password parameters
    parameters = request.args
    if not parameters:
        return make_response(jsonify({'error': 'No parameters for the password were given'}), 400)

    try:
        password = Password(parameters)
    except:
        error = sys.exc_info()[1].__str__()
        return make_response(jsonify({'error': error}), 400)

    return make_response(jsonify({'string': password.value}), 200)

